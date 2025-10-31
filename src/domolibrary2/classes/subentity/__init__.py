"""
Subentity Package - Unified Relationship Management and Entity Control

This package provides subentities and relationship management systems for Domo objects.
It includes legacy access/membership classes and new unified relationship systems.

Unified Relationship System (Recommended):
    Relationships: Comprehensive relationship modeling across all Domo entity types
    - Access relationships (HAS_ACCESS_OWNER, HAS_ACCESS_EDITOR, etc.)
    - Membership relationships (IS_MEMBER_OF, IS_OWNER_OF, etc.)
    - Lineage relationships (IS_DERIVED_FROM, USES_DATA_FROM, etc.)
    - Certification relationships (IS_CERTIFIED_BY, IS_TAGGED_WITH, etc.)
    - Unified API across all relationship types and object types

Legacy Access Control System:
    AccessControl: Simplified access management for migration purposes
    - Standardized access levels (OWNER, ADMIN, EDITOR, VIEWER, etc.)
    - Basic access grant tracking
    - Unified API across Domo object types

Legacy Classes (being phased out):
    DomoAccess: Account-specific access management
    DomoMembership: Group membership management

Other Subentities:
    DomoCertification: Content certification management
    DomoLineage: Entity relationship and lineage tracking
    DomoTag: Content tagging and categorization

Migration Path:
    Legacy → AccessControl → Relationships
    The new Relationships system is the most comprehensive and can model
    all types of entity relationships in Domo, not just access control.
"""

# New unified relationship system (recommended)
# Import relationship types from entities module
try:
    from ...entities.relationships import (
        DomoRelationship as Relationship,
        DomoRelationshipController,
        RelationshipType,
    )
except ImportError:
    # Fallback if relationships module not available
    DomoRelationshipController = None
    Relationship = None
    RelationshipType = None

# Transitional access control system
# AccessControl module not yet implemented
# from .AccessControl import (...)

# Other subentity classes
from .certification import DomoCertification
from .lineage import DomoLineage
from .membership import (
    DomoMembership,
    DomoMembership_Group,
    Membership_Entity,
    UpdateMembership,
)
from .schedule import DomoSchedule_Base
from .tags import DomoTags

__all__ = [
    # New unified relationship system (recommended)
    "RelationshipType",
    "Relationship",
    "DomoRelationshipController",
    # Legacy membership classes (deprecated)
    "DomoMembership",
    "DomoMembership_Group",
    "Membership_Entity",
    "UpdateMembership",
    # Other subentities
    "DomoCertification",
    "DomoLineage",
    "DomoSchedule_Base",
    "DomoTags",
]
