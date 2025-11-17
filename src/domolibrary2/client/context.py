"""
RouteContext - A context object for route functions.

This module provides a context object that bundles common parameters
passed to route functions, reducing parameter clutter and making
function signatures cleaner.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function calls.

    Bundles common parameters that are passed through route functions
    to get_data() calls, including session management, debugging flags,
    and parent class information.

    Attributes:
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert context to dictionary for passing to get_data().

        Returns:
            Dictionary with context parameters suitable for get_data() calls
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
