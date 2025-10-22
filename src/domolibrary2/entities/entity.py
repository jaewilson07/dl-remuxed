"""
Core Domo entity classes.

This module contains the main entity classes that represent Domo objects
and their management functionality.
"""

from .base import DomoBase

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DomoEntity(DomoBase):
    """Base class for all Domo entities.

    Represents a Domo entity with common properties and methods.
    All specific entity types (datasets, cards, etc.) inherit from this class.
    """

    id: Optional[str] = None
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary representation."""
        return {"id": self.id, "name": self.name}

    def to_json(self) -> str:
        """Convert entity to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class DomoUser(DomoEntity):
    """Represents a Domo user entity."""

    email: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary representation."""
        return {
            **super().to_dict(),
            "email": self.email,
            "display_name": self.display_name,
            "role": self.role,
        }


@dataclass
class DomoGroup(DomoEntity):
    """Represents a Domo group entity."""

    description: Optional[str] = None
    member_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert group to dictionary representation."""
        return {
            **super().to_dict(),
            "description": self.description,
            "member_count": self.member_count,
        }


@dataclass
class DomoDataset(DomoEntity):
    """Represents a Domo dataset entity."""

    description: Optional[str] = None
    owner_id: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataset to dictionary representation."""
        return {
            **super().to_dict(),
            "description": self.description,
            "owner_id": self.owner_id,
            "row_count": self.row_count,
            "column_count": self.column_count,
        }


@dataclass
class DomoCard(DomoEntity):
    """Represents a Domo card entity."""

    description: Optional[str] = None
    owner_id: Optional[str] = None
    dataset_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary representation."""
        return {
            **super().to_dict(),
            "description": self.description,
            "owner_id": self.owner_id,
            "dataset_id": self.dataset_id,
        }


@dataclass
class DomoPage(DomoEntity):
    """Represents a Domo page entity."""

    description: Optional[str] = None
    owner_id: Optional[str] = None
    card_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert page to dictionary representation."""
        return {
            **super().to_dict(),
            "description": self.description,
            "owner_id": self.owner_id,
            "card_count": self.card_count,
        }


__all__ = [
    "DomoEntity",
    "DomoUser",
    "DomoGroup",
    "DomoDataset",
    "DomoCard",
    "DomoPage",
]
