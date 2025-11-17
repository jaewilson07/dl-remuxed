"""
Route Context Module

This module provides a RouteContext dataclass that bundles common route function
parameters for cleaner function signatures and easier parameter passing.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass, field
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """
    Context object for route functions that bundles common parameters.

    This class provides a way to pass multiple common route parameters as a single
    object, making function signatures cleaner and parameter passing more consistent.

    Attributes:
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
    """

    session: Optional[httpx.AsyncClient] = field(default=None)
    debug_api: bool = field(default=False)
    debug_num_stacks_to_drop: int = field(default=1)
    parent_class: Optional[str] = field(default=None)

    def to_dict(self) -> dict:
        """
        Convert RouteContext to dictionary for passing to get_data().

        Returns:
            Dictionary with all context parameters suitable for get_data() calls
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }

    @classmethod
    def from_legacy_params(
        cls,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 1,
        parent_class: Optional[str] = None,
    ) -> "RouteContext":
        """
        Create RouteContext from legacy individual parameters.

        This factory method supports backward compatibility by allowing creation
        of RouteContext from the traditional parameter style.

        Args:
            session: Optional HTTP client session for connection reuse
            debug_api: Enable detailed API request/response logging
            debug_num_stacks_to_drop: Number of stack frames to omit in debug output
            parent_class: Name of calling class for debugging context

        Returns:
            RouteContext instance with the specified parameters
        """
        return cls(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )
