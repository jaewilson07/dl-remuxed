"""
Subentity classes for specialized Domo objects.

This module contains specialized entity classes that extend the core functionality
with additional features and behaviors.
"""

from .base import DomoBase, DomoEnum
from .entity import DomoEntity

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


class AccessLevel(DomoEnum):
    """Access levels for Domo entities."""

    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    PARTICIPANT = "participant"
    VIEWER = "viewer"
    default = "viewer"


class ShareType(DomoEnum):
    """Types of sharing for Domo entities."""

    INDIVIDUAL = "individual"
    GROUP = "group"
    DOMAIN = "domain"
    default = "individual"


@dataclass
class DomoSubEntity(DomoEntity):
    """Base class for Domo subentities with enhanced functionality."""

    parent_id: Optional[str] = None
    access_level: Optional[AccessLevel] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert subentity to dictionary representation."""
        return {
            **super().to_dict(),
            "parent_id": self.parent_id,
            "access_level": self.access_level.value if self.access_level else None,
        }


@dataclass
class DomoMembership(DomoSubEntity):
    """Represents membership in a Domo entity."""

    user_id: Optional[str] = None
    group_id: Optional[str] = None
    share_type: Optional[ShareType] = None
    granted_date: Optional[str] = None
    granted_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert membership to dictionary representation."""
        return {
            **super().to_dict(),
            "user_id": self.user_id,
            "group_id": self.group_id,
            "share_type": self.share_type.value if self.share_type else None,
            "granted_date": self.granted_date,
            "granted_by": self.granted_by,
        }


@dataclass
class DomoAccess(DomoSubEntity):
    """Represents access control for a Domo entity."""

    entity_type: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_inherited: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert access to dictionary representation."""
        return {
            **super().to_dict(),
            "entity_type": self.entity_type,
            "permissions": self.permissions,
            "is_inherited": self.is_inherited,
        }


@dataclass
class DomoSubscription(DomoSubEntity):
    """Represents a subscription to a Domo entity."""

    frequency: Optional[str] = None
    notification_type: Optional[str] = None
    is_active: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert subscription to dictionary representation."""
        return {
            **super().to_dict(),
            "frequency": self.frequency,
            "notification_type": self.notification_type,
            "is_active": self.is_active,
        }


@dataclass
class DomoShare(DomoSubEntity):
    """Represents sharing configuration for a Domo entity."""

    recipient_id: Optional[str] = None
    recipient_type: Optional[ShareType] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert share to dictionary representation."""
        return {
            **super().to_dict(),
            "recipient_id": self.recipient_id,
            "recipient_type": (
                self.recipient_type.value if self.recipient_type else None
            ),
            "message": self.message,
        }


__all__ = [
    "AccessLevel",
    "ShareType",
    "DomoSubEntity",
    "DomoMembership",
    "DomoAccess",
    "DomoSubscription",
    "DomoShare",
]
