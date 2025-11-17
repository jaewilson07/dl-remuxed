"""
RouteContext Module

Provides a context object to consolidate common route function parameters.
This reduces boilerplate and makes route function signatures cleaner.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function calls.

    Consolidates common parameters like session, debugging flags, and metadata
    that are typically passed to most route functions.

    Attributes:
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: httpx.AsyncClient | None = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_get_data_kwargs(self) -> dict:
        """Convert context to keyword arguments for get_data() calls.

        Returns:
            Dictionary with keys suitable for get_data() function
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
