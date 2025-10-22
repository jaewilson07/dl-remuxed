"""
Modular Domo entity system.

This package provides a refactored entity architecture organized into focused modules:

- base: Foundational classes and enhanced enums
- entity: Core Domo entity classes (users, groups, datasets, cards, pages)
- subentity: Specialized entity classes with enhanced functionality
- relationships: Unified relationship system for entity interactions

The modular design improves maintainability, reduces coupling, and provides
clear separation of concerns for different aspects of the entity system.
"""

# Import base classes and enums
from .base import DomoEnum, DomoEnumMixin, DomoBase

# Import core entity classes
from .entity import (
    DomoEntity,
    DomoUser,
    DomoGroup,
    DomoDataset,
    DomoCard,
    DomoPage,
)

# Import subentity classes
from .subentity import (
    AccessLevel,
    ShareType,
    DomoSubEntity,
    DomoMembership,
    DomoAccess,
    DomoSubscription,
    DomoShare,
)

# Import relationship system
from .relationships import (
    RelationshipType,
    RelationshipStatus,
    DomoRelationship,
    DomoRelationshipController,
)

__all__ = [
    # Base classes and enums
    "DomoEnum",
    "DomoEnumMixin",
    "DomoBase",
    # Core entities
    "DomoEntity",
    "DomoUser",
    "DomoGroup",
    "DomoDataset",
    "DomoCard",
    "DomoPage",
    # Subentities
    "AccessLevel",
    "ShareType",
    "DomoSubEntity",
    "DomoMembership",
    "DomoAccess",
    "DomoSubscription",
    "DomoShare",
    # Relationships
    "RelationshipType",
    "RelationshipStatus",
    "DomoRelationship",
    "DomoRelationshipController",
]
