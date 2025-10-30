"""
Unified relationship system for Domo entities.

This module provides a comprehensive relationship modeling framework that unifies
all types of entity interactions within the Domo ecosystem. It standardizes how
entities relate to each other, whether through access control, membership,
sharing permissions, organizational hierarchies, or data lineage connections.

The relationship system enables:
- Consistent access control across all Domo objects (datasets, cards, pages, etc.)
- Unified membership management for groups, roles, and organizations
- Standardized sharing and permission models
- Hierarchical relationships and organizational structures
- Data lineage and dependency tracking
- Extensible relationship types for future needs

Key Design Principles:
- Entity-agnostic: Works with any Domo entity type
- Relationship-centric: Focus on connections rather than entity-specific logic
- Bidirectional awareness: Relationships are navigable in both directions
- Metadata support: Rich context and properties for each relationship
- Async-first: Built for scalable concurrent operations

Classes:
    DomoRelationship: Represents a relationship between two entities with metadata
    DomoRelationshipController: Manages and orchestrates relationship operations

Usage:
    # Create relationships between entities
    relationship = DomoRelationship(
        relative_id="user123",
        relative_class=DomoUser,
        relationship_type=RelationshipType.OWNER,
        parent_entity=dataset,
        relative_entity=user
    )

    # Manage relationships through controller
    controller = DomoRelationshipController()
    await controller.add_relationship("user123", RelationshipType.VIEWER)
    relationships = await controller.get()
"""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .base import DomoBase, DomoEnum

RelationshipType = DomoEnum
"""Types of relationships between Domo entities."""

# Access and Permission Relationships
# OWNER = "owner"
# ADMIN = "admin"
# EDITOR = "editor"
# PARTICIPANT = "participant"
# VIEWER = "viewer"

# # Membership Relationships
# MEMBER = "member"
# OWNER = "owner"

# # LIneage
# PARENT = "parent"
# CHILD = "child"


@dataclass
class DomoRelationship(DomoBase):
    """Represents a relationship between two Domo entities.

    This unified relationship model can represent any type of connection
    between Domo entities including access control, membership, sharing,
    subscriptions, and organizational structures. Each relationship captures
    the nature of the connection and provides bidirectional navigation.

    The relationship model is designed to be:
    - Lightweight: Minimal required fields for efficiency
    - Extensible: Metadata dictionary for custom properties
    - Navigable: Easy traversal between related entities
    - Comparable: Built-in equality for deduplication

    Attributes:
        relative_id (str): ID of the entity this relationship points to
        relative_class (DomoEntity): Class type of the related entity for instantiation
        relationship_type (RelationshipType): Nature of the relationship (owner, member, viewer, etc.)
        parent_entity (DomoEntity): The entity that owns this relationship (optional for standalone use)
        relative_entity (DomoEntity): Cached instance of the related entity (optional for performance)
        metadata (Dict[str, Any]): Additional properties and context for the relationship

    Examples:
        # User has viewer access to a dataset
        viewer_relationship = DomoRelationship(
            relative_id="user123",
            relative_class=DomoUser,
            relationship_type=RelationshipType.VIEWER,
            parent_entity=dataset
        )

        # Dataset is a child of another dataset (lineage)
        lineage_relationship = DomoRelationship(
            relative_id="parent_dataset_456",
            relative_class=DomoDataset,
            relationship_type=RelationshipType.PARENT,
            metadata={"lineage_type": "transformation", "created_date": "2023-01-01"}
        )

        # Group membership relationship
        member_relationship = DomoRelationship(
            relative_id="group789",
            relative_class=DomoGroup,
            relationship_type=RelationshipType.MEMBER
        )

    Note:
        Relationships are considered equal if they have the same parent_id,
        relationship_type, and relative_id. This enables efficient deduplication
        when working with large sets of relationships.
    """

    relationship_type: RelationshipType

    # Core relationship identifiers
    parent_entity: Any = field(repr=False, default=None)  # DomoEntity instance
    entity: Any = field(repr=False, default=None)  # DomoEntity instance

    def __eq__(self, other):
        return (
            self.parent_entity.id == other.parent_entity.id
            and self.relationship_type == other.relationship_type
            and self.entity.id == other.entity.id
        )

    @property
    def parent_id(self):
        return self.parent_entity.id

    metadata: dict[str, Any] = field(default_factory=dict)

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert relationship to dictionary."""
        raise NotImplementedError("Subclasses must implement to_dict method.")

    @abstractmethod
    async def update(self):
        """Update relationship metadata or properties."""
        raise NotImplementedError("Subclasses must implement update method.")


@dataclass
class DomoRelationshipController(DomoBase):
    """Controller for managing Domo entity relationships.

    This class provides high-level operations for creating, managing, and
    querying relationships between Domo entities. It serves as the primary
    interface for relationship operations and acts as a centralized manager
    for all relationship-based interactions.

    The controller is designed to be:
    - Entity-agnostic: Works with any Domo entity type
    - Batch-aware: Efficient bulk operations for large relationship sets
    - Async-optimized: Concurrent operations for performance
    - Cache-friendly: Intelligent caching of frequently accessed relationships
    - Extensible: Easy to subclass for specialized relationship types

    Architecture:
        The controller will typically be implemented as a property of Domo entities:
        - DomoDataset.relationships -> DatasetRelationshipController
        - DomoUser.relationships -> UserRelationshipController
        - DomoGroup.relationships -> GroupRelationshipController

        Each specialized controller provides domain-specific methods:
        - dataset.relationships.get_owners() -> list[DomoUser]
        - dataset.relationships.add_viewers([user1, user2])
        - user.relationships.get_groups() -> list[DomoGroup]
        - group.relationships.get_members() -> list[DomoUser]

    Attributes:
        relationships (list[DomoRelationship]): Collection of managed relationships

    Abstract Methods:
        add_relationship: Create new relationships between entities
        get: Retrieve relationships matching specified criteria

    Concrete Methods:
        get_relative_entities: Fetch and cache related entity instances

    Examples:
        # Basic usage through entity
        dataset = await DomoDataset.get_by_id(auth, "dataset123")
        owners = await dataset.relationships.get_owners()
        await dataset.relationships.add_viewer("user456")

        # Direct controller usage
        controller = DatasetRelationshipController()
        relationships = await controller.get()
        await controller.add_relationship("user789", RelationshipType.EDITOR)

        # Batch operations
        new_viewers = ["user1", "user2", "user3"]
        await controller.add_relationships(new_viewers, RelationshipType.VIEWER)

    Performance Considerations:
        - Uses concurrent operations (gather_with_concurrency) for bulk fetching
        - Implements lazy loading of related entities
        - Supports relationship caching to reduce API calls
        - Batches similar operations when possible

    Note:
        This is an abstract base class. Concrete implementations should be
        created for specific entity types and relationship scenarios.
    """

    relationships: list[DomoRelationship] = field(default_factory=list)

    @abstractmethod
    def add_relationship(
        self,
        relative_id,
        relationship_type: RelationshipType,
    ) -> DomoRelationship:
        """Create a new relationship between entities.

        Abstract method that must be implemented by concrete controller
        classes to handle the creation of new relationships. The implementation
        should handle both the local relationship creation and any necessary
        API calls to persist the relationship in Domo.

        Args:
            relative_id (str): ID of the entity to create a relationship with
            relationship_type (RelationshipType): Type of relationship to create
                                                 (owner, viewer, member, etc.)

        Returns:
            DomoRelationship: The newly created relationship instance

        Implementation Requirements:
            - Validate the relative_id exists and is accessible
            - Create the DomoRelationship instance
            - Make necessary API calls to establish the relationship in Domo
            - Add the relationship to the controller's relationships collection
            - Handle any errors gracefully with appropriate exceptions

        Example Implementation:
            async def add_relationship(self, relative_id, relationship_type):
                # Validate entity exists
                entity = await self.relative_class.get_by_id(self.auth, relative_id)

                # Create relationship
                relationship = DomoRelationship(
                    relative_id=relative_id,
                    relative_class=self.relative_class,
                    relationship_type=relationship_type,
                    parent_entity=self.parent_entity
                )

                # Persist in Domo via API
                await self._api_create_relationship(relationship)

                # Add to local collection
                self.relationships.append(relationship)

                return relationship
        """

    @abstractmethod
    async def get(
        self,
    ) -> list[DomoRelationship]:
        """Find and retrieve relationships matching the specified criteria.

        Abstract method that must be implemented by concrete controller classes
        to handle the retrieval of relationships from Domo. This method serves
        as the primary interface for querying relationships and should support
        filtering, sorting, and pagination as needed.

        Returns:
            list[DomoRelationship]: Collection of relationships that match
                                   the controller's criteria

        Implementation Requirements:
            - Query the appropriate Domo API endpoints for relationship data
            - Convert API responses to DomoRelationship instances
            - Apply any filtering logic specific to the entity type
            - Handle pagination for large result sets
            - Cache results appropriately for performance
            - Handle API errors gracefully

        Example Implementation:
            async def get(self) -> list[DomoRelationship]:
                # Query Domo API for relationships
                api_response = await self._api_get_relationships()

                # Convert to DomoRelationship instances
                relationships = []
                for item in api_response.data:
                    rel = DomoRelationship(
                        relative_id=item['user_id'],
                        relative_class=DomoUser,
                        relationship_type=RelationshipType(item['access_level']),
                        parent_entity=self.parent_entity
                    )
                    relationships.append(rel)

                # Cache and return
                self.relationships = relationships
                return relationships

        Usage Patterns:
            # Get all relationships
            all_rels = await controller.get()

            # Implementations may support filtering
            owners = await controller.get(relationship_type=RelationshipType.OWNER)
            viewers = await controller.get(relationship_type=RelationshipType.VIEWER)
        """
        raise NotImplementedError("Subclasses must implement get method.")


__all__ = [
    "RelationshipType",
    "DomoRelationship",
    "DomoRelationshipController",
]
