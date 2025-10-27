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
    "Entity_Relation",
]

# | export


import abc
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Callable, Optional

from ..utils.convert import convert_snake_to_pascal
from . import auth as dmda


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


@dataclass
class DomoBase(abc.ABC):
    """Abstract base class for all Domo objects.

    This class serves as the foundation for all Domo entities and managers,
    providing a common interface and ensuring consistent implementation
    across the inheritance hierarchy.
    """

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

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, auth: "DomoAuth", obj: dict):
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

    @property
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
class Entity_Relation:
    """Represents a relationship between entities in the Domo ecosystem.

    This class models relationships between different entities such as
    user-to-group memberships, entity ownership, or other associations.

    Attributes:
        auth (DomoAuth): Authentication object for API requests (not shown in repr)
        entity: The related entity object
        relation_type (str): Type of relationship (e.g., 'OWNER', 'MEMBER', 'ADMIN')
    """

    auth: dmda.DomoAuth = field(repr=False)
    entity: Any  # DomoUser or DomoGroup
    relation_type: str

    def __eq__(self, other) -> bool:
        """Check equality based on entity ID and relation type.

        Args:
            other: Object to compare with

        Returns:
            bool: True if both have the same entity ID and relation type
        """
        if self.__class__.__name__ != other.__class__.__name__:
            return False

        return (
            self.entity.id == other.entity.id
            and self.relation_type == other.relation_type
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
