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
from .Relationships import (
    DomoAccessRelationshipController,
    DomoMembershipRelationshipController,
    DomoRelationshipController,
    DomoRelationshipManager,
    EntityType as RelationshipEntityType,
    Relationship,
    RelationshipSummary,
    RelationshipType,
)

# Transitional access control system
from .AccessControl import (
    AccessGrant,
    AccessLevel,
    AccessSummary,
    DomoAccessController,
    DomoAccountAccessController,
    DomoGroupAccessController,
    DomoObjectAccessManager,
    EntityType,
)

# Legacy access and membership classes
from .DomoAccess import (
    Access_Config_Error,
    Access_Entity,
    DomoAccess,
    DomoAccess_Account,
    DomoAccess_OAuth,
)
from .DomoMembership import (
    GroupMembership,
    Membership,
    Membership_Entity,
    UpdateMembership,
)

# Other subentity classes
from .DomoCertification import DomoCertification
from .DomoLineage import DomoLineage
from .DomoTag import DomoTag

__all__ = [
    # New unified relationship system (recommended)
    "RelationshipType",
    "RelationshipEntityType",
    "Relationship",
    "RelationshipSummary",
    "DomoRelationshipController",
    "DomoRelationshipManager",
    "DomoAccessRelationshipController",
    "DomoMembershipRelationshipController",
    # Transitional access control system
    "AccessLevel",
    "EntityType",
    "AccessGrant",
    "AccessSummary",
    "DomoAccessController",
    "DomoObjectAccessManager",
    "DomoAccountAccessController",
    "DomoGroupAccessController",
    # Legacy access classes (deprecated)
    "DomoAccess",
    "DomoAccess_Account",
    "DomoAccess_OAuth",
    "Access_Entity",
    "Access_Config_Error",
    # Legacy membership classes (deprecated)
    "Membership",
    "GroupMembership",
    "Membership_Entity",
    "UpdateMembership",
    # Other subentities
    "DomoCertification",
    "DomoLineage",
    "DomoTag",
]
