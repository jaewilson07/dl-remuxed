__all__ = [
    "Access_Config_Error",
    "Access_Relation",
    "DomoAccess",
]

from dataclasses import dataclass, field

from domolibrary2.entities.relationships import DomoRelationshipController

from ..client.exceptions import ClassError
from . import DomoEntity, DomoEnumMixin, DomoRelationship, DomoSubEntity

# from .. import DomoUser as dmdu

EntityType = DomoEnumMixin
RelationshipType = DomoEnumMixin


class Access_Config_Error(ClassError):
    def __init__(self, cls_instance=None, account_id=None, message=None):
        super().__init__(
            cls_instance=cls_instance,
            entity_id=account_id,
            message=message,
        )


@dataclass
class Access_Relation(DomoRelationship):
    """Represents an entity with access to an object."""

    entity: DomoEntity

    async def grant_access(
        self,
        entity: DomoEntity,
        relationship_type: RelationshipType,
        **kwargs,
    ) -> bool:
        """Grant access to an entity."""
        raise NotImplementedError("DomoAccess.grant_access not implemented")

    async def revoke_access(
        self,
        entity: DomoEntity,
        relationship_type: RelationshipType,
        **kwargs,
    ) -> bool:
        """Revoke access from an entity."""
        raise NotImplementedError("DomoAccess.revoke_access not implemented")


@dataclass
class DomoAccess(DomoRelationshipController, DomoSubEntity):
    """
    Describes concept of content access

    This class provides a consistent interface for managing access relationships
    across all Domo objects including accounts, datasets, cards, pages, etc.
    """

    share_enum: RelationshipType = field(repr=False, default=None)

    def __post_init__(self):
        # super().__post_init__()

        if self.share_enum and not issubclass(self.share_enum, RelationshipType):
            print(self.share_enum)
            raise Access_Config_Error(
                cls_instance=self,
                account_id=self.parent_id,
                message="Share enum must be a subclass of ShareAccount.",
            )

    async def get(self) -> list[Access_Relation]:
        """Get all access relationships for this object."""
        raise NotImplementedError("DomoAccess.get not implemented")
