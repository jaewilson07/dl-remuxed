__all__ = [
    "Access_Config_Error",
    "Access_Entity",
    "DomoAccess",
    "DomoAccess_Account",
    "DomoAccess_OAuth",
]

from dataclasses import dataclass, field
from typing import Any, List

import httpx

from .. import DomoUser as dmdu


from ...client import exceptions as dmde
from ...client.auth import DomoAuth
from ...entities.entities import DomoSubEntity, Entity_Relation

# Import unified access control system
try:
    from .AccessControl import (
        AccessLevel,
        EntityType,
        AccessGrant,
        DomoAccountAccessController,
        DomoObjectAccessManager,
    )

    UNIFIED_ACCESS_AVAILABLE = True
except ImportError:
    UNIFIED_ACCESS_AVAILABLE = False
from ...routes import account as account_routes
from ...routes.account import (
    ShareAccount,
    ShareAccount_AccessLevel,
    ShareAccount_V1_AccessLevel,
)
from ...utils import chunk_execution as dmce


class Access_Config_Error(dmde.ClassError):
    def __init__(self, cls_instance, account_id, message):
        super().__init__(
            cls_instance=cls_instance, message=message, entity_id=account_id
        )


@dataclass
class Access_Entity(Entity_Relation):
    relation_type: ShareAccount = None


@dataclass
class DomoAccess(DomoSubEntity):
    auth: DomoAuth = field(repr=False)

    share_enum: ShareAccount = field(repr=False)

    accesslist: List[Access_Entity] = field(
        default_factory=lambda: []
    )  # can include users or groups

    accesslist_all_users: List[Any] = field(default_factory=lambda: [])  # DomoUser

    def __post_init__(self):
        super().__post_init__()

        if not issubclass(self.share_enum, ShareAccount):
            raise Access_Config_Error(
                cls_instance=self,
                account_id=self.parent_id,
                message="Share enum must be a subclass of ShareAccount.",
            )

    async def get(self, *args, **kwargs):
        raise NotImplementedError(
            f"{self.__class__.__name__}.get() must be implemented in a subclass."
        )

    async def get_all_users(
        self,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 1,
        session: httpx.AsyncClient = None,
    ):
        from .. import DomoGroup as dmdg

        await self.get(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        for access in self.accesslist:
            entity = access.entity

            if isinstance(entity, dmdu.DomoUser):
                if entity not in self.accesslist_all_users:
                    self.accesslist_all_users.append(entity)

            if isinstance(entity, dmdg.DomoGroup):
                domo_users = await access.entity.Membership.get_members()

                [
                    self.accesslist_all_users.append(user)
                    for user in domo_users
                    if user not in self.accesslist_all_users
                ]

        return self.accesslist_all_users

    async def get_unified_access_summary(self):
        """Get access summary using the unified access control system."""
        if not UNIFIED_ACCESS_AVAILABLE:
            raise NotImplementedError("Unified access control system not available")

        # Create a mock parent object for the access controller
        from ...entities.entities import DomoEntity

        @dataclass
        class MockParent(DomoEntity):
            def display_url(self) -> str:
                return f"https://{self.auth.domo_instance}.domo.com/accounts/{self.id}"

            @classmethod
            def from_dict(cls, auth, obj: dict):
                return cls(auth=auth, id=obj.get("id"), raw=obj)

            @classmethod
            async def get_by_id(cls, auth, entity_id: str):
                return cls(auth=auth, id=entity_id, raw={})

        mock_parent = MockParent(auth=self.auth, id=self.parent_id, raw={})
        controller = DomoAccountAccessController(self.auth, mock_parent)

        return await controller.get_all_access_summaries()

    async def get_access_grants(self) -> List:
        """Get access grants in unified format."""
        if not UNIFIED_ACCESS_AVAILABLE:
            return []

        # Convert existing access list to unified format
        grants = []
        for access_entity in self.accesslist:
            entity_type = (
                EntityType.USER
                if hasattr(access_entity.entity, "email")
                else EntityType.GROUP
            )

            # Map relation_type to AccessLevel
            access_level = self._map_relation_type_to_access_level(
                access_entity.relation_type
            )

            grant = AccessGrant(
                entity_id=access_entity.entity.id,
                entity_type=entity_type,
                access_level=access_level,
            )
            grants.append(grant)

        return grants

    def _map_relation_type_to_access_level(self, relation_type) -> "AccessLevel":
        """Map ShareAccount relation type to unified AccessLevel."""
        if not UNIFIED_ACCESS_AVAILABLE:
            return None

        # This mapping depends on your ShareAccount enum values
        # Adjust based on actual ShareAccount_AccessLevel values
        mapping = {
            "OWNER": AccessLevel.OWNER,
            "ADMIN": AccessLevel.ADMIN,
            "EDIT": AccessLevel.EDITOR,
            "VIEW": AccessLevel.VIEWER,
        }

        # Get string representation of relation_type
        relation_str = getattr(relation_type, "value", str(relation_type))
        return mapping.get(relation_str, AccessLevel.VIEWER)

    async def share(
        self,
        user_id=None,
        group_id=None,
        domo_group=None,
        domo_user=None,
        relation_type: ShareAccount = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        relation_type = relation_type or self.share_enum.default

        user_id = user_id or domo_user and domo_user.id
        group_id = group_id or domo_group and domo_group.id

        if not user_id and not group_id:
            raise Access_Config_Error(
                cls_instance=self,
                account_id=self.parent_id,
                message="Either user_id or group_id must be provided.",
            )

        share_payload = relation_type.generate_payload(
            user_id=user_id, group_id=group_id
        )

        res = await relation_type.share(
            auth=self.auth,
            account_id=self.parent_id,
            share_payload=share_payload,
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        return res

    async def upsert_share(
        self,
        user_id=None,
        group_id=None,
        domo_group=None,
        domo_user=None,
        relation_type: ShareAccount = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        user_id = user_id or (domo_user and domo_user.id)
        group_id = group_id or (domo_group and domo_group.id)

        await self.get(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        is_already_exists = all(
            [
                (member.entity.id == user_id or member.entity.id == group_id)
                and relation_type == member.relation_type
                for member in self.accesslist
            ]
        )

        if is_already_exists:
            return False

        return await self.share(
            user_id=user_id,
            group_id=group_id,
            relation_type=relation_type,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            session=session,
        )


@dataclass
class DomoAccess_Account(DomoAccess):
    """
    Account access management with unified access control integration.

    This class provides backward compatibility while integrating with
    the new unified access control system. Use get_unified_access_summary()
    for access to the standardized access control interface.
    """

    version: int = None  # api version - aligns to feature switch

    share_enum: ShareAccount = field(repr=False, default=ShareAccount_AccessLevel)

    def __post_init__(self):
        super().__post_init__()

        if isinstance(self.share_enum, ShareAccount_AccessLevel):
            self.version = 2
        elif isinstance(self.share_enum, ShareAccount_V1_AccessLevel):
            self.version = 1

        return True

    async def get(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        """assumes v2 access api"""

        res = await account_routes.get_account_accesslist(
            auth=self.auth,
            account_id=self.parent_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        self.accesslist = await dmce.gather_with_concurrency(
            *[
                Access_Entity._from_user_id(
                    user_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "USER"
            ],
            *[
                Access_Entity._from_group_id(
                    group_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "GROUP"
            ],
            n=10,
        )
        return self.accesslist


@dataclass
class DomoAccess_OAuth(DomoAccess):
    share_enum: ShareAccount = field(repr=False, default=ShareAccount_AccessLevel)

    async def get(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        """assumes v2 access api"""

        res = await account_routes.get_oauth_account_accesslist(
            auth=self.auth,
            account_id=self.parent_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        self.accesslist = await dmce.gather_with_concurrency(
            *[
                Access_Entity._from_user_id(
                    user_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "USER"
            ],
            *[
                Access_Entity._from_group_id(
                    group_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "GROUP"
            ],
            n=10,
        )
        return self.accesslist
