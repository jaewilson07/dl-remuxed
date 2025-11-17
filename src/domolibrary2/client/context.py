"""
RouteContext - Context object for route function parameters.

This module provides a dataclass to group common parameters used across route functions,
reducing parameter repetition and improving maintainability.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object that encapsulates common route function parameters.

    This class groups together parameters that are commonly passed to route functions,
    providing a cleaner interface and easier parameter management.

    Attributes:
        session: Optional httpx AsyncClient for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: httpx.AsyncClient | None = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    @classmethod
    def from_kwargs(
        cls,
        session: httpx.AsyncClient | None = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 1,
        parent_class: Optional[str] = None,
    ) -> "RouteContext":
        """Create a RouteContext from individual parameters.

        This is a convenience factory method for creating a context object
        from the traditional parameter list.

        Args:
            session: Optional httpx client session for connection reuse
            debug_api: Enable detailed API request/response logging
            debug_num_stacks_to_drop: Number of stack frames to drop in debug output
            parent_class: Optional parent class name for debugging context

        Returns:
            A new RouteContext instance
        """
        return cls(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )
