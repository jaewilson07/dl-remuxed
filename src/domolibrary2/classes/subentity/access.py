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

from domolibrary2.entities.relationships import DomoRelationshipController

from ...client import exceptions as dmde
from ...entities import DomoEntity, DomoEnum, DomoRelationship, DomoSubEntity
from ...routes import account as account_routes
from ...routes.account import (
    ShareAccount,
    ShareAccount_AccessLevel,
    ShareAccount_V1_AccessLevel,
)

# from .. import DomoUser as dmdu


class Access_Config_Error(dmde.ClassError):
    def __init__(self, cls_instance, account_id, message):
        super().__init__(
            cls_instance=cls_instance, message=message, entity_id=account_id
        )


EntityType = DomoEnum
RelationshipType = DomoEnum


@dataclass
class Access_Entity(DomoRelationship):
    """Represents an entity with access to an object."""

    entity: DomoEntity

    @property
    def relation_type(self) -> ShareAccount:
        """Backward compatibility property."""
        return self.relationship_type

    async def grant_access(
        self,
        entity_id: str,
        entity_type: EntityType,
        relationship_type: RelationshipType,
        **kwargs,
    ) -> bool:
        """Grant access to an entity."""
        raise NotImplementedError("DomoAccess.grant_access not implemented")

    async def revoke_access(
        self,
        entity_id: str,
        entity_type: EntityType,
        relationship_type: RelationshipType,
        **kwargs,
    ) -> bool:
        """Revoke access from an entity."""
        raise NotImplementedError("DomoAccess.revoke_access not implemented")


@dataclass
class DomoAccess(DomoRelationshipController, DomoSubEntity):
    """
    Unified access management using the relationship system.

    This class provides a consistent interface for managing access relationships
    across all Domo objects including accounts, datasets, cards, pages, etc.
    """

    share_enum: RelationshipType = field(repr=False, default=None)
    # Legacy compatibility
    accesslist: List[Access_Entity] = field(default_factory=list)
    accesslist_all_users: List[Any] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()

        if self.share_enum and not issubclass(self.share_enum, ShareAccount):
            raise Access_Config_Error(
                cls_instance=self,
                account_id=self.parent_id,
                message="Share enum must be a subclass of ShareAccount.",
            )

    async def get(self) -> List[Access_Entity]:
        """Get all access relationships for this object."""
        raise NotImplementedError("DomoAccess.get not implemented")

    async def get_users(self) -> List[DomoEntity]:
        """Get all users with access (including through groups)."""

        raise NotImplementedError("DomoAccess.get_users not implemented")

    async def share(
        self,
        entity: DomoEntity,
        relation_type: ShareAccount = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        raise NotImplementedError("DomoAccess.share not implemented")


@dataclass
class DomoAccess_Account(DomoAccess):
    """
    Account access management using unified relationship system.

    This class provides backward compatibility while using the new
    unified relationship framework internally.
    """

    share_enum: ShareAccount = field(repr=False, default=ShareAccount_AccessLevel)

    @property
    def version(self) -> int:
        """API version - aligns to feature switch."""

        if isinstance(self.share_enum, ShareAccount_AccessLevel):
            return 2

        elif isinstance(self.share_enum, ShareAccount_V1_AccessLevel):
            return 1

    async def get(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        """Get account access using unified relationship system."""

        res = await account_routes.get_account_accesslist(
            auth=self.auth,
            account_id=self.parent_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return res


@dataclass
class DomoAccess_OAuth(DomoAccess):
    """
    OAuth access management using unified relationship system.

    This class provides backward compatibility while using the new
    unified relationship framework internally.
    """

    share_enum: ShareAccount = field(repr=False, default=ShareAccount_AccessLevel)

    async def get(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        """Get OAuth account access using unified relationship system."""
        res = await account_routes.get_oauth_account_accesslist(
            auth=self.auth,
            account_id=self.parent_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return res
