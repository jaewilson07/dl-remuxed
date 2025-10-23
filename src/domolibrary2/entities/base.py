"""
Base classes and enums for the Domo entity system.

This module provides foundational classes and enhanced enums that serve as
the building blocks for all Domo entities and relationships.
"""

import abc
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Optional, Callable, List, TYPE_CHECKING


from ..utils.convert import convert_snake_to_pascal
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
    default = "UNKNOWN"


@dataclass
class DomoBase(abc.ABC):
    """Abstract base class for all Domo objects.

    This class serves as the foundation for all Domo entities and managers,
    providing a common interface and ensuring consistent implementation
    across the inheritance hierarchy.
    """

    def to_dict(self):
        """Convert dataclass to dictionary, excluding fields with repr=False.

        Recursively converts nested dataclasses by calling their to_dict() method.
        """
        result = {}
        for fld in fields(self):
            if not fld.repr:
                continue

            value = getattr(self, fld.name)

            # Handle nested dataclasses
            if hasattr(value, "__dataclass_fields__") and hasattr(value, "to_dict"):
                result[fld.name] = value.to_dict()
            # Handle lists/tuples that might contain dataclasses
            elif isinstance(value, (list, tuple)):
                result[fld.name] = [
                    (
                        item.to_dict()
                        if (
                            hasattr(item, "__dataclass_fields__")
                            and hasattr(item, "to_dict")
                        )
                        else item
                    )
                    for item in value
                ]
            else:
                result[fld.name] = value

        return result


__all__ = [
    "DomoEnum",
    "DomoEnumMixin",
    "DomoBase",
]
