"""
RouteContext - Context object for route function calls.

This module provides the RouteContext class that encapsulates common parameters
passed to API route functions, simplifying function signatures and improving
maintainability.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass, field
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object that encapsulates common route function parameters.

    This class consolidates session management, debugging, and parent class tracking
    into a single object that can be passed to route functions and get_data calls.

    Attributes:
        session: Optional httpx.AsyncClient for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    @classmethod
    def from_kwargs(
        cls,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 1,
        parent_class: Optional[str] = None,
    ) -> "RouteContext":
        """Create a RouteContext from individual keyword arguments.

        This is a convenience method for creating a RouteContext when you have
        the individual parameters rather than an existing context object.

        Args:
            session: Optional httpx.AsyncClient for connection reuse
            debug_api: Enable detailed API request/response logging
            debug_num_stacks_to_drop: Number of stack frames to drop in debug output
            parent_class: Optional parent class name for debugging context

        Returns:
            RouteContext: New context object with the provided parameters
        """
        return cls(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    def with_parent_class(self, parent_class: str) -> "RouteContext":
        """Create a new RouteContext with a different parent_class.

        This is useful for passing context down through layers while tracking
        the call chain.

        Args:
            parent_class: New parent class name

        Returns:
            RouteContext: New context object with updated parent_class
        """
        return RouteContext(
            session=self.session,
            debug_api=self.debug_api,
            debug_num_stacks_to_drop=self.debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    def to_dict(self) -> dict:
        """Convert RouteContext to a dictionary of parameters.

        Returns:
            dict: Dictionary with keys matching get_data parameter names
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
