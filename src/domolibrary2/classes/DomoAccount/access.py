"""DomoAccess re-export for DomoAccount package.

This module re-exports DomoAccess classes from the subentity package
to resolve import dependencies within the DomoAccount package.
"""

from dataclasses import dataclass, field

import httpx

from ...client.response import ResponseGetData
from ...entities.relationships_access import Access_Relation, DomoAccess
from ...routes import account as account_routes
from ...routes.account import (
    ShareAccount,
    ShareAccount_AccessLevel,
    ShareAccount_V1_AccessLevel,
)
from ...utils import chunk_execution as dmce


@dataclass
class DomoAccess_Relation(Access_Relation):
    def to_dict(self):
        return {"id": self.entity.id, "type": self.entity.entity_type}

    async def update(self):
        raise NotImplementedError("DomoAccount_Access.update not implemented")

    @classmethod
    async def from_user_id(cls, parent_entity, user_id, auth, access_level):
        from ..DomoUser import DomoUser

        return cls(
            entity=await DomoUser.get_by_id(auth=auth, user_id=user_id),
            relationship_type=access_level,
            parent_entity=parent_entity,
        )

    @classmethod
    async def from_group_id(cls, parent_entity, group_id, auth, access_level):
        from ..DomoGroup import DomoGroup

        return cls(
            entity=await DomoGroup.get_by_id(auth=auth, group_id=group_id),
            relationship_type=access_level,
            parent_entity=parent_entity,
        )

    @classmethod
    async def from_entity_id(
        cls, parent_entity, entity_id, auth, access_level, entity_type
    ):
        if entity_type == "USER":
            return await cls.from_user_id(parent_entity, entity_id, auth, access_level)
        elif entity_type == "GROUP":
            return await cls.from_group_id(parent_entity, entity_id, auth, access_level)
        else:
            raise ValueError(f"Unknown entity_type: {entity_type}")


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

    async def add_relationship(self):
        raise NotImplementedError("DomoAccount_Access.add_relation not implemented")

    async def _get_relations_from_response(self, res: ResponseGetData):
        self.relationships = await dmce.gather_with_concurrency(
            *[
                DomoAccess_Relation.from_entity_id(
                    parent_entity=self.parent,
                    entity_id=obj["id"],
                    auth=self.auth,
                    access_level=obj["accessLevel"],
                    entity_type=obj["type"],
                )
                for obj in res.response
            ],
            n=10,
        )

        return self.relationships

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

        return await self._get_relations_from_response(res)


@dataclass
class DomoAccess_OAuth(DomoAccess_Account):
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

        return await self._get_relations_from_response(res)


__all__ = ["DomoAccess_Account", "DomoAccess_OAuth", "DomoAccess_Relation"]
