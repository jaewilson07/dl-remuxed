"""
Unified relationship system for Domo entities.

This module provides a comprehensive relationship modeling system that unifies
all types of entity interactions including access control, membership, sharing,
and other relationship types within the Domo ecosystem.
"""

from .base import DomoBase, DomoEnum
from .entity import DomoEntity

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class RelationshipType(DomoEnum):
    """Types of relationships between Domo entities."""

    # Access and Permission Relationships
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    PARTICIPANT = "participant"
    VIEWER = "viewer"

    # Membership Relationships
    MEMBER = "member"
    GROUP_MEMBER = "group_member"
    DOMAIN_MEMBER = "domain_member"

    # Sharing Relationships
    SHARED_WITH = "shared_with"
    SHARED_BY = "shared_by"

    # Subscription Relationships
    SUBSCRIBER = "subscriber"
    SUBSCRIPTION_OWNER = "subscription_owner"

    # Organizational Relationships
    PARENT = "parent"
    CHILD = "child"
    SIBLING = "sibling"

    # Dependency Relationships
    DEPENDS_ON = "depends_on"
    DEPENDENCY_OF = "dependency_of"

    # Content Relationships
    CONTAINS = "contains"
    CONTAINED_IN = "contained_in"

    default = "viewer"


class RelationshipStatus(DomoEnum):
    """Status of a relationship."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    EXPIRED = "expired"
    REVOKED = "revoked"

    default = "active"


@dataclass
class DomoRelationship(DomoBase):
    """Represents a relationship between two Domo entities.

    This unified relationship model can represent any type of connection
    between Domo entities including access control, membership, sharing,
    subscriptions, and organizational structures.

    Attributes:
        id: Unique identifier for this relationship
        source_entity_id: ID of the source entity in the relationship
        source_entity_type: Type of the source entity (user, group, dataset, etc.)
        target_entity_id: ID of the target entity in the relationship
        target_entity_type: Type of the target entity
        relationship_type: The type of relationship (owner, member, viewer, etc.)
        relationship_status: Current status of the relationship
        permissions: List of specific permissions granted through this relationship
        metadata: Additional relationship-specific data
        created_date: When the relationship was established
        modified_date: When the relationship was last modified
        created_by: ID of the user who created the relationship
        modified_by: ID of the user who last modified the relationship
        expires_date: Optional expiration date for temporary relationships
        is_inherited: Whether this relationship is inherited from a parent entity
        inheritance_path: Path showing how the relationship was inherited
    """

    # Core relationship identifiers
    id: Optional[str] = None
    source_entity_id: Optional[str] = None
    source_entity_type: Optional[str] = None
    target_entity_id: Optional[str] = None
    target_entity_type: Optional[str] = None

    # Relationship properties
    relationship_type: Optional[RelationshipType] = None
    relationship_status: Optional[RelationshipStatus] = None
    permissions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Audit information
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    expires_date: Optional[datetime] = None

    # Inheritance properties
    is_inherited: bool = False
    inheritance_path: List[str] = field(default_factory=list)

    def is_active(self) -> bool:
        """Check if the relationship is currently active."""
        if self.relationship_status != RelationshipStatus.ACTIVE:
            return False

        if self.expires_date and self.expires_date < datetime.now():
            return False

        return True

    def has_permission(self, permission: str) -> bool:
        """Check if the relationship grants a specific permission."""
        return permission in self.permissions

    def add_permission(self, permission: str) -> None:
        """Add a permission to the relationship."""
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission: str) -> None:
        """Remove a permission from the relationship."""
        if permission in self.permissions:
            self.permissions.remove(permission)

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get a metadata value by key."""
        return self.metadata.get(key, default)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set a metadata value."""
        self.metadata[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary representation."""
        return {
            "id": self.id,
            "source_entity_id": self.source_entity_id,
            "source_entity_type": self.source_entity_type,
            "target_entity_id": self.target_entity_id,
            "target_entity_type": self.target_entity_type,
            "relationship_type": (
                self.relationship_type.value if self.relationship_type else None
            ),
            "relationship_status": (
                self.relationship_status.value if self.relationship_status else None
            ),
            "permissions": self.permissions,
            "metadata": self.metadata,
            "created_date": (
                self.created_date.isoformat() if self.created_date else None
            ),
            "modified_date": (
                self.modified_date.isoformat() if self.modified_date else None
            ),
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "expires_date": (
                self.expires_date.isoformat() if self.expires_date else None
            ),
            "is_inherited": self.is_inherited,
            "inheritance_path": self.inheritance_path,
        }

    def to_json(self) -> str:
        """Convert relationship to JSON string."""
        return json.dumps(self.to_dict(), default=str)


@dataclass
class DomoRelationshipController(DomoBase):
    """Controller for managing Domo entity relationships.

    This class provides high-level operations for creating, managing, and
    querying relationships between Domo entities. It serves as the primary
    interface for relationship operations.
    """

    relationships: List[DomoRelationship] = field(default_factory=list)

    def create_relationship(
        self,
        source_entity_id: str,
        source_entity_type: str,
        target_entity_id: str,
        target_entity_type: str,
        relationship_type: RelationshipType,
        permissions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
    ) -> DomoRelationship:
        """Create a new relationship between entities."""
        relationship = DomoRelationship(
            source_entity_id=source_entity_id,
            source_entity_type=source_entity_type,
            target_entity_id=target_entity_id,
            target_entity_type=target_entity_type,
            relationship_type=relationship_type,
            relationship_status=RelationshipStatus.ACTIVE,
            permissions=permissions or [],
            metadata=metadata or {},
            created_date=datetime.now(),
            created_by=created_by,
        )

        self.relationships.append(relationship)
        return relationship

    def find_relationships(
        self,
        source_entity_id: Optional[str] = None,
        target_entity_id: Optional[str] = None,
        relationship_type: Optional[RelationshipType] = None,
        relationship_status: Optional[RelationshipStatus] = None,
        active_only: bool = True,
    ) -> List[DomoRelationship]:
        """Find relationships matching the specified criteria."""
        results = []

        for relationship in self.relationships:
            # Filter by active status if requested
            if active_only and not relationship.is_active():
                continue

            # Filter by source entity
            if source_entity_id and relationship.source_entity_id != source_entity_id:
                continue

            # Filter by target entity
            if target_entity_id and relationship.target_entity_id != target_entity_id:
                continue

            # Filter by relationship type
            if (
                relationship_type
                and relationship.relationship_type != relationship_type
            ):
                continue

            # Filter by relationship status
            if (
                relationship_status
                and relationship.relationship_status != relationship_status
            ):
                continue

            results.append(relationship)

        return results

    def get_entity_permissions(
        self, source_entity_id: str, target_entity_id: str
    ) -> List[str]:
        """Get all permissions a source entity has on a target entity."""
        permissions = []
        relationships = self.find_relationships(
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            active_only=True,
        )

        for relationship in relationships:
            permissions.extend(relationship.permissions)

        return list(set(permissions))  # Remove duplicates

    def has_relationship(
        self,
        source_entity_id: str,
        target_entity_id: str,
        relationship_type: RelationshipType,
    ) -> bool:
        """Check if a specific relationship exists between entities."""
        relationships = self.find_relationships(
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            relationship_type=relationship_type,
            active_only=True,
        )

        return len(relationships) > 0

    def revoke_relationship(
        self,
        source_entity_id: str,
        target_entity_id: str,
        relationship_type: Optional[RelationshipType] = None,
    ) -> List[DomoRelationship]:
        """Revoke relationships between entities."""
        relationships = self.find_relationships(
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            relationship_type=relationship_type,
            active_only=True,
        )

        for relationship in relationships:
            relationship.relationship_status = RelationshipStatus.REVOKED
            relationship.modified_date = datetime.now()

        return relationships

    def get_entity_relationships(
        self, entity_id: str, as_source: bool = True, as_target: bool = True
    ) -> List[DomoRelationship]:
        """Get all relationships for an entity (as source and/or target)."""
        results = []

        if as_source:
            results.extend(self.find_relationships(source_entity_id=entity_id))

        if as_target:
            results.extend(self.find_relationships(target_entity_id=entity_id))

        return results


__all__ = [
    "RelationshipType",
    "RelationshipStatus",
    "DomoRelationship",
    "DomoRelationshipController",
]
