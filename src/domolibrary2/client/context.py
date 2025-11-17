"""
RouteContext for managing common parameters across route functions.

This module provides the RouteContext class which bundles common parameters
passed to route functions, making the function signatures cleaner and more maintainable.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function execution.

    Bundles common parameters used across route functions to simplify
    function signatures and provide consistent parameter handling.

    Attributes:
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_get_data_kwargs(self) -> dict:
        """Convert RouteContext to kwargs for get_data function.

        Returns:
            Dictionary with keys matching get_data parameters
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
