"""Base entity classes for Domo objects with inheritance hierarchy and lineage support.

This module provides the foundational classes for all Domo entities including datasets,
cards, pages, users, and groups. It implements a hierarchical structure with support
for entity relationships, lineage tracking, and federation.

Classes:
    DomoEnum: Enhanced enum with case-insensitive lookup
    DomoBase: Abstract base class for all Domo objects
    DomoEntity: Base entity with core functionality
    DomoEntity_w_Lineage: Entity with lineage tracking capabilities
    DomoFederatedEntity: Entity that can be federated across instances
    DomoPublishedEntity: Entity that supports publishing/subscription
    DomoManager: Base class for entity managers
    DomoSubEntity: Entity that belongs to a parent entity
    Entity_Relation: Represents relationships between entities
"""

__all__ = [
    "DomoEnum",
    "DomoEnumMixin",
    "DomoBase",
    "DomoEntity",
    "DomoEntity_w_Lineage",
    "DomoFederatedEntity",
    "DomoPublishedEntity",
    "DomoManager",
    "DomoSubEntity",
    "EntityType",
    "RelationshipType",
    "DomoRelationship",
    "DomoRelationshipSummary",
    "DomoRelationshipController",
    "DomoRelationshipManager",
    # Legacy (deprecated)
    "Entity_Relation",
]

# | export


import abc
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Callable, Optional, TYPE_CHECKING

from ..utils.convert import convert_snake_to_pascal
from ..client import auth as dmda

if TYPE_CHECKING:
    from ..client import auth as dmda


class DomoEnumMixin:
    """Enhanced Enum mixin with case-insensitive lookup and default value support.

    This mixin provides case-insensitive string matching and falls back to a default
    value when no match is found. All subclasses should define a 'default' member.

    Example:
        >>> class Status(DomoEnumMixin, Enum):
        ...     ACTIVE = "active"
        ...     INACTIVE = "inactive"
        ...     default = "UNKNOWN"
        >>> Status.get("ACTIVE")  # Case insensitive
        <Status.ACTIVE: 'active'>
        >>> Status.get("invalid")
        <Status.default: 'UNKNOWN'>
    """

    @classmethod
    def get(cls, value):
        """Get enum member by case-insensitive string lookup.

        Args:
            value: String value to look up (case-insensitive)

        Returns:
            Enum member if found, otherwise the default member
        """
        if not isinstance(value, str):
            return getattr(cls, "default", None)

        # cls should be an Enum subclass at runtime
        for member in cls:  # type: ignore
            if member.name.lower() == value.lower():
                return member

        return getattr(cls, "default", None)

    @classmethod
    def _missing_(cls, value):
        """Handle missing enum values with case-insensitive fallback.

        Args:
            value: The value that wasn't found

        Returns:
            Enum member if case-insensitive match found, otherwise default
        """
        if isinstance(value, str):
            value_lower = value.lower()
            # cls should be an Enum subclass at runtime
            for member in cls:  # type: ignore
                if (
                    hasattr(member, "name")
                    and isinstance(member.name, str)
                    and member.name.lower() == value_lower
                ):
                    return member

        return getattr(cls, "default", None)


class DomoEnum(DomoEnumMixin, Enum):
    """Enhanced Enum class with case-insensitive lookup and default value support.

    This enum provides case-insensitive string matching and falls back to a default
    value when no match is found. All subclasses should define a 'default' member.

    Example:
        >>> class Status(DomoEnum):
        ...     ACTIVE = "active"
        ...     INACTIVE = "inactive"
        ...     default = "UNKNOWN"
        >>> Status.get("ACTIVE")  # Case insensitive
        <Status.ACTIVE: 'active'>
        >>> Status.get("invalid")
        <Status.default: 'UNKNOWN'>
    """

    # Define a default value that all enum subclasses should override
    default = "UNKNOWN"


class EntityType(DomoEnum):
    """Types of entities that can participate in relationships."""

    USER = "USER"
    GROUP = "GROUP"
    ROLE = "ROLE"
    DATASET = "DATASET"
    CARD = "CARD"
    PAGE = "PAGE"
    ACCOUNT = "ACCOUNT"
    TAG = "TAG"
    DATACENTER = "DATACENTER"
    CONNECTOR = "CONNECTOR"
    DATAFLOW = "DATAFLOW"
    STREAM = "STREAM"
    APPLICATION = "APPLICATION"

    default = USER


class RelationshipType(DomoEnum):
    """Types of relationships between entities."""

    # Access relationships (Entity → Object)
    HAS_ACCESS_OWNER = "HAS_ACCESS_OWNER"  # Full control including deletion
    HAS_ACCESS_ADMIN = (
        "HAS_ACCESS_ADMIN"  # Administrative access, can manage permissions
    )
    HAS_ACCESS_EDITOR = "HAS_ACCESS_EDITOR"  # Can modify content but not permissions
    HAS_ACCESS_CONTRIBUTOR = (
        "HAS_ACCESS_CONTRIBUTOR"  # Can add content but not modify existing
    )
    HAS_ACCESS_VIEWER = "HAS_ACCESS_VIEWER"  # Read-only access

    # Group membership relationships (User/Group → Group)
    IS_OWNER_OF = "IS_OWNER_OF"  # Group owner
    IS_MEMBER_OF = "IS_MEMBER_OF"  # Group member
    IS_ADMIN_OF = "IS_ADMIN_OF"  # Group administrator

    # Lineage relationships (Dataset → Dataset, Card → Dataset, etc.)
    IS_DERIVED_FROM = "IS_DERIVED_FROM"  # Dataset created from another dataset
    IS_FEDERATED_FROM = "IS_FEDERATED_FROM"  # Federated dataset relationship
    IS_PUBLISHED_FROM = "IS_PUBLISHED_FROM"  # Published dataset relationship
    USES_DATA_FROM = "USES_DATA_FROM"  # Card uses data from dataset
    IS_INPUT_TO = "IS_INPUT_TO"  # Dataset is input to dataflow
    IS_OUTPUT_FROM = "IS_OUTPUT_FROM"  # Dataset is output from dataflow

    # Certification relationships (Object → User/Group)
    IS_CERTIFIED_BY = "IS_CERTIFIED_BY"  # Content certified by user

    # Tagging relationships (Object → Tag)
    IS_TAGGED_WITH = "IS_TAGGED_WITH"  # Object tagged with tag

    # Account relationships (User/Group → Account)
    HAS_ACCOUNT_ACCESS = "HAS_ACCOUNT_ACCESS"  # Access to credential account

    # Application relationships
    IS_OWNED_BY = "IS_OWNED_BY"  # Application owned by user/group
    HAS_PERMISSION_ON = "HAS_PERMISSION_ON"  # Permission on application/resource

    default = HAS_ACCESS_VIEWER


@dataclass
class DomoBase(abc.ABC):
    """Abstract base class for all Domo objects.

    This class serves as the foundation for all Domo entities and managers,
    providing a common interface and ensuring consistent implementation
    across the inheritance hierarchy.
    """


@dataclass
class DomoEntity(DomoBase):
    """Base class for all Domo entities (datasets, cards, pages, users, etc.).

    This class provides core functionality for Domo entities including authentication,
    unique identification, and data conversion utilities. All concrete entity types
    should inherit from this class or one of its subclasses.

    Attributes:
        auth (DomoAuth): Authentication object for API requests (not shown in repr)
        id (str): Unique identifier for the entity
        raw (dict): Raw API response data for the entity (not shown in repr)

    Example:
        >>> entity = SomeDomoEntity(auth=auth, id="123", raw={})
        >>> entity.display_url()  # Implemented by subclass
        'https://mycompany.domo.com/...'
    """

    auth: dmda.DomoAuth = field(repr=False)
    id: str
    raw: dict = field(repr=False)  # api representation of the class

    # logger: Logger = field(repr=False) ## pass global logger

    @property
    def _name(self) -> str:
        name = getattr(self, "name", None)

        if not name:
            raise NotImplementedError(
                "This property should be implemented by subclasses."
            )
        return name

    def __eq__(self, other) -> bool:
        """Check equality based on entity ID.

        Args:
            other: Object to compare with

        Returns:
            bool: True if both are DomoEntity instances with the same ID
        """
        if isinstance(other, DomoEntity):
            return self.id == other.id

        return False

    def to_dict(self, override_fn: Optional[Callable] = None) -> dict:
        """Convert all dataclass attributes to a dictionary in pascalCase.

        This method is useful for serializing entity data for API requests
        or data export operations.

        Args:
            override_fn (Optional[Callable]): Custom conversion function to override default behavior

        Returns:
            dict: Dictionary with pascalCase keys and corresponding attribute values

        Example:
            >>> entity.to_dict()
            {'entityId': '123', 'displayName': 'My Entity', ...}
        """

        if override_fn:
            return override_fn(self)

        return {
            convert_snake_to_pascal(field.name): getattr(self, field.name)
            for field in fields(self)
        }

    @property
    def entity_type(self) -> EntityType:
        """Get the EntityType for this entity based on its class name."""
        class_name = self.__class__.__name__

        # Map class names to EntityTypes
        type_mapping = {
            "DomoUser": EntityType.USER,
            "DomoGroup": EntityType.GROUP,
            "DomoDataset": EntityType.DATASET,
            "DomoCard": EntityType.CARD,
            "DomoPage": EntityType.PAGE,
            "DomoAccount": EntityType.ACCOUNT,
            "DomoTag": EntityType.TAG,
            "DomoDatacenter": EntityType.DATACENTER,
            "DomoConnector": EntityType.CONNECTOR,
            "DomoDataflow": EntityType.DATAFLOW,
            "DomoStream": EntityType.STREAM,
            "DomoApplication": EntityType.APPLICATION,
        }

        # Handle variations and subclasses
        for class_prefix, entity_type in type_mapping.items():
            if class_name.startswith(class_prefix):
                return entity_type

        # Default fallback
        return EntityType.USER

    def get_relationship_controller(self) -> Optional["DomoRelationshipController"]:
        """Get the relationship controller for this entity type."""
        # This would typically be implemented by a relationship manager
        # For now, return None - subclasses can override
        return None

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, auth: "dmda.DomoAuth", obj: dict):
        """Create an entity instance from a dictionary representation.

        This method should be implemented by subclasses to handle the conversion
        from API response dictionaries to entity objects.

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    @classmethod
    @abc.abstractmethod
    async def get_by_id(cls, auth: dmda.DomoAuth, entity_id: str):
        """Fetch an entity by its unique identifier.

        This method should be implemented by subclasses to handle entity-specific
        retrieval logic from the Domo API.

        Args:
            auth (DomoAuth): Authentication object for API requests
            entity_id (str): Unique identifier of the entity to retrieve

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abc.abstractmethod
    def display_url(self) -> str:
        """Generate the URL to display this entity in the Domo interface.

        This method should return the direct URL to view the entity in Domo's
        web interface, allowing users to navigate directly to the entity.

        Returns:
            str: Complete URL to view the entity in Domo

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoEntity_w_Lineage(DomoEntity):
    """Entity with lineage tracking capabilities.

    This class extends DomoEntity to include lineage tracking functionality,
    allowing entities to track their relationships and dependencies within
    the Domo ecosystem.

    Attributes:
        lineage: Lineage tracking object for dependency management (not shown in repr)
    """

    lineage: Any = field(repr=False, default=None)

    def __post_init__(self):
        """Initialize lineage tracking after entity creation."""
        from ..classes.subentity import DomoLineage as dmdl

        # Using protected method until public interface is available
        self.lineage = dmdl.DomoLineage.from_parent(auth=self.auth, parent=self)

    async def get_lineage_relationships(self) -> list:  # List[DomoRelationship]
        """Get all lineage relationships for this entity."""
        controller = self.get_relationship_controller()
        if not controller:
            return []

        all_relationships = await controller.get_resolved_relationships()
        return [r for r in all_relationships if r.is_lineage_relationship]

    async def get_upstream_entities(self) -> list:  # List[DomoEntity]
        """Get all entities this entity is derived from."""
        lineage_relationships = await self.get_lineage_relationships()

        upstream_relationships = [
            r
            for r in lineage_relationships
            if r.to_entity_id == self.id
            and r.relationship_type
            in [
                RelationshipType.IS_DERIVED_FROM,
                RelationshipType.IS_FEDERATED_FROM,
                RelationshipType.IS_PUBLISHED_FROM,
                RelationshipType.USES_DATA_FROM,
            ]
        ]

        # This would need to be implemented to actually fetch the entities
        # For now, return the relationship info
        return upstream_relationships

    async def get_downstream_entities(self) -> list:  # List[DomoEntity]
        """Get all entities derived from this entity."""
        lineage_relationships = await self.get_lineage_relationships()

        downstream_relationships = [
            r
            for r in lineage_relationships
            if r.from_entity_id == self.id
            and r.relationship_type
            in [
                RelationshipType.IS_DERIVED_FROM,
                RelationshipType.IS_FEDERATED_FROM,
                RelationshipType.IS_PUBLISHED_FROM,
                RelationshipType.USES_DATA_FROM,
            ]
        ]

        # This would need to be implemented to actually fetch the entities
        return downstream_relationships

    @classmethod
    @abc.abstractmethod
    async def _get_entity_by_id(cls, auth: dmda.DomoAuth, entity_id: str):
        """Fetch an entity by its ID with lineage support.

        This method should be implemented by subclasses to fetch the specific
        entity type while ensuring lineage tracking is properly initialized.

        Args:
            auth (DomoAuth): Authentication object for API requests
            entity_id (str): Unique identifier of the entity to retrieve

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoFederatedEntity(DomoEntity_w_Lineage):
    """Entity that can be federated across multiple Domo instances.

    This class extends lineage-enabled entities to support federation,
    allowing entities to maintain relationships across different Domo
    instances in federated environments.
    """

    @abc.abstractmethod
    async def get_federated_parent(
        self, parent_auth=None, parent_auth_retrieval_fn: Optional[Callable] = None
    ):
        """Retrieve the parent entity from a federated Domo instance.

        Args:
            parent_auth: Authentication object for the parent instance
            parent_auth_retrieval_fn (Optional[Callable]): Function to retrieve parent auth

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoPublishedEntity(DomoFederatedEntity):
    """Entity that supports publishing and subscription across instances.

    This class extends federated entities to support Domo's publishing
    and subscription model, allowing entities to be shared and synchronized
    across different Domo instances.

    Attributes:
        subscription: Subscription information for this published entity (not shown in repr)
        parent_publication: Parent publication details (not shown in repr)
    """

    subscription: Any = field(repr=False, default=None)
    parent_publication: Any = field(repr=False, default=None)

    @abc.abstractmethod
    async def get_subscription(self):
        """Retrieve subscription information for this entity.

        This method should fetch and store subscription details for the entity,
        updating the subscription attribute.

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        # self.subscription = ... ## should return one subscription
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abc.abstractmethod
    async def get_parent_publication(
        self, parent_auth=None, parent_auth_retrieval_fn=None
    ):
        """Retrieve parent publication information.

        This method fetches the parent publication details, optionally using
        provided authentication or a retrieval function.

        Args:
            parent_auth: Authentication object for the parent instance
            parent_auth_retrieval_fn: Function to retrieve parent authentication

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        # if not self.subscription:
        #     await self.get_subscription()

        # if not parent_auth:
        #     if not parent_auth_retrieval_fn:
        #         raise ValueError("Either parent_auth or parent_auth_retrieval_fn must be provided.")
        #     parent_auth = parent_auth_retrieval_fn(self.subscription)

        # self.parent_publication = ... (parent_auth) ## should return the parent publication
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abc.abstractmethod
    async def get_parent_content_details(self, parent_auth=None):
        """Retrieve detailed information about the parent content.

        This method fetches comprehensive details about the parent dataset,
        card, page, or other content type.

        Args:
            parent_auth: Authentication object for the parent instance

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        # if not self.parent_publication:
        #     await self.get_parent_publication(parent_auth)
        raise NotImplementedError("This method should be implemented by subclasses.")

    async def get_federated_parent(
        self, parent_auth=None, parent_auth_retrieval_fn: Optional[Callable] = None
    ):
        """Get the federated parent entity.

        Args:
            parent_auth: Authentication object for the parent instance
            parent_auth_retrieval_fn (Optional[Callable]): Function to retrieve parent auth

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoManager(DomoBase):
    """Base class for entity managers that handle collections of entities.

    This class provides the foundation for manager classes that handle
    operations on collections of entities (e.g., DatasetManager, CardManager).

    Attributes:
        auth (DomoAuth): Authentication object for API requests (not shown in repr)
    """

    auth: dmda.DomoAuth = field(repr=False)

    @abc.abstractmethod
    async def get(self, *args, **kwargs):
        """Retrieve entities based on provided criteria.

        This method should be implemented by subclasses to handle entity-specific
        retrieval and filtering logic.

        Args:
            *args: Positional arguments for entity retrieval
            **kwargs: Keyword arguments for filtering and options

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoSubEntity(DomoBase):
    """Base class for entities that belong to a parent entity.

    This class handles entities that are sub-components of other entities,
    such as columns in a dataset or slides in a page. It automatically
    inherits authentication and parent references.

    Attributes:
        auth (DomoAuth): Authentication object (inherited from parent, not shown in repr)
        parent: Reference to the parent entity
        parent_id (str): ID of the parent entity
    """

    auth: dmda.DomoAuth = field(repr=False)
    parent: Any
    parent_id: str

    def __post_init__(self):
        """Initialize sub-entity with parent's authentication and ID."""
        if self.parent:
            self.auth = self.parent.auth
            self.parent_id = self.parent.id

    @classmethod
    def from_parent(cls, parent: DomoEntity):
        """Create a sub-entity instance from a parent entity.

        Args:
            parent (DomoEntity): The parent entity to derive from

        Returns:
            DomoSubEntity: New sub-entity instance with inherited properties
        """
        return cls(auth=parent.auth, parent=parent, parent_id=parent.id)


@dataclass
class DomoRelationship:
    """Represents a directional relationship between two entities in the Domo ecosystem.

    This is the core relationship model that handles all types of connections:
    - Access relationships (user/group → object with permission level)
    - Membership relationships (user → group with role)
    - Lineage relationships (dataset → dataset with derivation type)
    - Certification relationships (object → user with certification type)

    Attributes:
        from_entity_id (str): ID of the source entity
        from_entity_type (EntityType): Type of the source entity
        to_entity_id (str): ID of the target entity
        to_entity_type (EntityType): Type of the target entity
        relationship_type (RelationshipType): Nature of the relationship
        auth (DomoAuth): Authentication object for API requests (not shown in repr)
        created_date (Optional[str]): When the relationship was established
        created_by (Optional[str]): Who established the relationship
        effective_date (Optional[str]): When the relationship becomes effective
        expiry_date (Optional[str]): When the relationship expires
        source_relationship_id (Optional[str]): For derived relationships (e.g., via group membership)
        metadata (Dict[str, Any]): Additional relationship-specific data
    """

    from_entity_id: str
    from_entity_type: EntityType
    to_entity_id: str
    to_entity_type: EntityType
    relationship_type: RelationshipType
    auth: dmda.DomoAuth = field(repr=False)

    # Relationship metadata
    created_date: Optional[str] = None
    created_by: Optional[str] = None
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None

    # For resolved relationships (e.g., inherited through groups)
    source_relationship_id: Optional[str] = None

    # Additional metadata
    metadata: dict = field(default_factory=dict)

    def __eq__(self, other) -> bool:
        """Check equality based on relationship components."""
        if not isinstance(other, DomoRelationship):
            return False

        return (
            self.from_entity_id == other.from_entity_id
            and self.from_entity_type == other.from_entity_type
            and self.to_entity_id == other.to_entity_id
            and self.to_entity_type == other.to_entity_type
            and self.relationship_type == other.relationship_type
        )

    @property
    def is_access_relationship(self) -> bool:
        """Check if this is an access-related relationship."""
        return self.relationship_type.value.startswith("HAS_ACCESS_")

    @property
    def is_membership_relationship(self) -> bool:
        """Check if this is a membership-related relationship."""
        return self.relationship_type in [
            RelationshipType.IS_OWNER_OF,
            RelationshipType.IS_MEMBER_OF,
            RelationshipType.IS_ADMIN_OF,
        ]

    @property
    def is_lineage_relationship(self) -> bool:
        """Check if this is a lineage-related relationship."""
        return self.relationship_type in [
            RelationshipType.IS_DERIVED_FROM,
            RelationshipType.IS_FEDERATED_FROM,
            RelationshipType.IS_PUBLISHED_FROM,
            RelationshipType.USES_DATA_FROM,
            RelationshipType.IS_INPUT_TO,
            RelationshipType.IS_OUTPUT_FROM,
        ]

    def to_dict(self) -> dict:
        """Convert relationship to dictionary representation."""
        return {
            "from_entity_id": self.from_entity_id,
            "from_entity_type": self.from_entity_type.value,
            "to_entity_id": self.to_entity_id,
            "to_entity_type": self.to_entity_type.value,
            "relationship_type": self.relationship_type.value,
            "created_date": self.created_date,
            "created_by": self.created_by,
            "effective_date": self.effective_date,
            "expiry_date": self.expiry_date,
            "source_relationship_id": self.source_relationship_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict, auth: dmda.DomoAuth) -> "DomoRelationship":
        """Create relationship from dictionary representation."""
        return cls(
            from_entity_id=data["from_entity_id"],
            from_entity_type=EntityType.get(data["from_entity_type"]),
            to_entity_id=data["to_entity_id"],
            to_entity_type=EntityType.get(data["to_entity_type"]),
            relationship_type=RelationshipType.get(data["relationship_type"]),
            auth=auth,
            created_date=data.get("created_date"),
            created_by=data.get("created_by"),
            effective_date=data.get("effective_date"),
            expiry_date=data.get("expiry_date"),
            source_relationship_id=data.get("source_relationship_id"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class DomoRelationshipSummary:
    """Summary of all relationships for a specific entity.

    This class aggregates all relationships involving an entity and provides
    convenience methods for analyzing access levels, memberships, and lineage.
    """

    entity_id: str
    entity_type: EntityType
    auth: dmda.DomoAuth = field(repr=False)
    relationships: list = field(default_factory=list)  # List[DomoRelationship]

    def get_relationships_by_type(self, relationship_type: RelationshipType) -> list:
        """Get all relationships of a specific type."""
        return [
            r for r in self.relationships if r.relationship_type == relationship_type
        ]

    def get_access_relationships(self) -> list:
        """Get all access-related relationships."""
        return [r for r in self.relationships if r.is_access_relationship]

    def get_membership_relationships(self) -> list:
        """Get all membership-related relationships."""
        return [r for r in self.relationships if r.is_membership_relationship]

    def get_lineage_relationships(self) -> list:
        """Get all lineage-related relationships."""
        return [r for r in self.relationships if r.is_lineage_relationship]

    @property
    def effective_access_level(self) -> RelationshipType:
        """Get the highest access level from all access relationships."""
        access_rels = self.get_access_relationships()
        if not access_rels:
            return RelationshipType.default

        # Define access hierarchy (highest to lowest)
        access_hierarchy = [
            RelationshipType.HAS_ACCESS_OWNER,
            RelationshipType.HAS_ACCESS_ADMIN,
            RelationshipType.HAS_ACCESS_EDITOR,
            RelationshipType.HAS_ACCESS_CONTRIBUTOR,
            RelationshipType.HAS_ACCESS_VIEWER,
        ]

        for level in access_hierarchy:
            if any(r.relationship_type == level for r in access_rels):
                return level

        return RelationshipType.default


class DomoRelationshipController(abc.ABC):
    """Abstract base controller for managing entity relationships.

    This class provides the foundation for relationship management across
    all Domo entity types. Subclasses implement entity-specific logic
    for creating, reading, updating, and deleting relationships.
    """

    def __init__(self, auth: dmda.DomoAuth, parent_entity: DomoEntity):
        self.auth = auth
        self.parent_entity = parent_entity
        self.parent_id = parent_entity.id

        # Cache for relationship data
        self._relationship_cache: dict = {}  # Dict[str, DomoRelationshipSummary]
        self._cache_valid = False

    @abc.abstractmethod
    async def get_direct_relationships(self) -> list:  # List[DomoRelationship]
        """Get all direct relationships for the parent entity."""
        pass

    @abc.abstractmethod
    async def create_relationship(
        self,
        target_entity_id: str,
        target_entity_type: EntityType,
        relationship_type: RelationshipType,
        **kwargs,
    ) -> bool:
        """Create a new relationship."""
        pass

    @abc.abstractmethod
    async def remove_relationship(
        self,
        target_entity_id: str,
        target_entity_type: EntityType,
        relationship_type: RelationshipType,
        **kwargs,
    ) -> bool:
        """Remove a relationship."""
        pass

    async def get_resolved_relationships(self) -> list:  # List[DomoRelationship]
        """Get resolved relationships (including inherited via groups)."""
        # Base implementation - can be overridden by subclasses
        return await self.get_direct_relationships()

    async def get_relationship_summary(self, entity_id: str) -> DomoRelationshipSummary:
        """Get comprehensive relationship summary for a specific entity."""
        if not self._cache_valid or entity_id not in self._relationship_cache:
            await self._refresh_relationship_cache()

        return self._relationship_cache.get(
            entity_id,
            DomoRelationshipSummary(
                entity_id=entity_id,
                entity_type=EntityType.USER,  # Default
                auth=self.auth,
            ),
        )

    async def get_all_relationship_summaries(
        self,
    ) -> dict:  # Dict[str, DomoRelationshipSummary]
        """Get relationship summaries for all entities."""
        if not self._cache_valid:
            await self._refresh_relationship_cache()

        return self._relationship_cache.copy()

    async def _refresh_relationship_cache(self):
        """Refresh the internal relationship cache."""
        all_relationships = await self.get_resolved_relationships()

        # Group relationships by from_entity
        entity_relationships: dict = {}  # Dict[str, List[DomoRelationship]]
        for rel in all_relationships:
            if rel.from_entity_id not in entity_relationships:
                entity_relationships[rel.from_entity_id] = []
            entity_relationships[rel.from_entity_id].append(rel)

        # Create relationship summaries
        self._relationship_cache = {}
        for entity_id, relationships in entity_relationships.items():
            entity_type = (
                relationships[0].from_entity_type if relationships else EntityType.USER
            )

            summary = DomoRelationshipSummary(
                entity_id=entity_id,
                entity_type=entity_type,
                auth=self.auth,
                relationships=relationships,
            )
            self._relationship_cache[entity_id] = summary

        self._cache_valid = True

    def invalidate_cache(self):
        """Invalidate the relationship cache."""
        self._cache_valid = False


class DomoRelationshipManager:
    """Main manager for unified relationship operations across all Domo objects.

    This class coordinates relationship management across different entity types,
    providing a unified interface for querying and managing relationships
    throughout the Domo ecosystem.
    """

    def __init__(self, auth: dmda.DomoAuth):
        self.auth = auth
        self._controllers: dict = {}  # Dict[str, type]

    def register_controller(self, entity_type: str, controller_class: type):
        """Register a relationship controller for a specific entity type."""
        self._controllers[entity_type] = controller_class

    def get_controller(
        self, entity: DomoEntity
    ) -> Optional[DomoRelationshipController]:
        """Get the appropriate relationship controller for an entity."""
        entity_type_name = type(entity).__name__

        if entity_type_name in self._controllers:
            return self._controllers[entity_type_name](self.auth, entity)

        return None

    async def get_entity_relationships(
        self,
        entity_id: str,
        entity_type: EntityType,
        relationship_types: Optional[list] = None,  # Optional[List[RelationshipType]]
    ) -> list:  # List[DomoRelationship]
        """Get all relationships for an entity across all objects."""
        # This would query relationships across all object types
        # Implementation depends on available APIs and indexing
        pass

    async def create_relationship(
        self,
        from_entity_id: str,
        from_entity_type: EntityType,
        to_entity: DomoEntity,
        relationship_type: RelationshipType,
        **kwargs,
    ) -> bool:
        """Create a relationship using the appropriate controller."""
        controller = self.get_controller(to_entity)
        if not controller:
            raise ValueError(
                f"No controller found for entity type: {type(to_entity).__name__}"
            )

        return await controller.create_relationship(
            target_entity_id=from_entity_id,
            target_entity_type=from_entity_type,
            relationship_type=relationship_type,
            **kwargs,
        )


# Legacy class for backward compatibility (deprecated)
@dataclass
class Entity_Relation:
    """Legacy relationship class - use DomoRelationship instead.

    DEPRECATED: This class is maintained for backward compatibility only.
    New code should use DomoRelationship which provides a more comprehensive
    and unified approach to modeling entity relationships.
    """

    auth: dmda.DomoAuth = field(repr=False)
    entity: Any  # DomoUser or DomoGroup
    relation_type: str

    def __eq__(self, other) -> bool:
        """Check equality based on entity ID and relation type."""
        if self.__class__.__name__ != other.__class__.__name__:
            return False

        return (
            self.entity.id == other.entity.id
            and self.relation_type == other.relation_type
        )

    def to_domo_relationship(
        self, to_entity_id: str, to_entity_type: EntityType
    ) -> DomoRelationship:
        """Convert to new DomoRelationship format."""
        # Determine entity type
        from_entity_type = (
            EntityType.USER if hasattr(self.entity, "email") else EntityType.GROUP
        )

        # Map old relation_type to new RelationshipType
        relationship_type_mapping = {
            "OWNER": RelationshipType.HAS_ACCESS_OWNER,
            "ADMIN": RelationshipType.HAS_ACCESS_ADMIN,
            "EDITOR": RelationshipType.HAS_ACCESS_EDITOR,
            "VIEWER": RelationshipType.HAS_ACCESS_VIEWER,
            "MEMBER": RelationshipType.IS_MEMBER_OF,
        }

        relationship_type = relationship_type_mapping.get(
            self.relation_type, RelationshipType.HAS_ACCESS_VIEWER
        )

        return DomoRelationship(
            from_entity_id=self.entity.id,
            from_entity_type=from_entity_type,
            to_entity_id=to_entity_id,
            to_entity_type=to_entity_type,
            relationship_type=relationship_type,
            auth=self.auth,
        )

    # @classmethod
    # async def _from_user_id(
    #     cls,
    #     user_id: str,
    #     relation_type: str,
    #     auth: dmda.DomoAuth,
    #     session: Optional[httpx.AsyncClient] = None,
    #     debug_api: bool = False,
    #     debug_num_stacks_to_drop: int = 2,
    # ):
    #     """Create an Entity_Relation from a user ID.

    #     Args:
    #         user_id (str): Unique identifier of the user
    #         relation_type (str): Type of relationship (e.g., 'OWNER', 'MEMBER')
    #         auth (DomoAuth): Authentication object for API requests
    #         session (Optional[httpx.AsyncClient]): HTTP client session
    #         debug_api (bool): Enable API debugging
    #         debug_num_stacks_to_drop (int): Stack frames to drop for debugging

    #     Returns:
    #         Entity_Relation: New relation instance with user entity
    #     """

    #     # if entity_type == "USER":
    #     from ..classes import DomoUser as dmdu

    #     # Handle optional session parameter
    #     kwargs = {
    #         "user_id": user_id,
    #         "auth": auth,
    #         "debug_api": debug_api,
    #         "debug_num_stacks_to_drop": debug_num_stacks_to_drop + 1,
    #     }
    #     if session is not None:
    #         kwargs["session"] = session

    #     # Note: DomoUser.get_by_id method should be implemented in the DomoUser class
    #     domo_user = await dmdu.DomoUser.get_by_id(**kwargs)  # type: ignore[attr-defined]

    #     return cls(entity=domo_user, relation_type=relation_type, auth=auth)

    # @classmethod
    # async def _from_group_id(
    #     cls,
    #     group_id: str,
    #     relation_type: str,
    #     auth: dmda.DomoAuth,
    #     session: Optional[httpx.AsyncClient] = None,
    #     debug_api: bool = False,
    #     debug_num_stacks_to_drop: int = 2,
    # ):
    #     """Create an Entity_Relation from a group ID.

    #     Args:
    #         group_id (str): Unique identifier of the group
    #         relation_type (str): Type of relationship (e.g., 'MEMBER', 'ADMIN')
    #         auth (DomoAuth): Authentication object for API requests
    #         session (Optional[httpx.AsyncClient]): HTTP client session
    #         debug_api (bool): Enable API debugging
    #         debug_num_stacks_to_drop (int): Stack frames to drop for debugging

    #     Returns:
    #         Entity_Relation: New relation instance with group entity
    #     """

    #     from ..classes import DomoGroup as dmdg

    #     # Handle optional session parameter
    #     kwargs = {
    #         "group_id": group_id,
    #         "auth": auth,
    #         "debug_api": debug_api,
    #         "debug_num_stacks_to_drop": debug_num_stacks_to_drop + 1,
    #     }
    #     if session is not None:
    #         kwargs["session"] = session

    #     # Note: DomoGroup.get_by_id method should be implemented in the DomoGroup class
    #     domo_group = await dmdg.DomoGroup.get_by_id(**kwargs)  # type: ignore[attr-defined]

    #     return cls(entity=domo_group, relation_type=relation_type, auth=auth)
