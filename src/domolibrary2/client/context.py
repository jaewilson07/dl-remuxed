"""
RouteContext - Context object for route function parameters

This module provides the RouteContext class which encapsulates common
parameters passed to route functions, making function signatures cleaner
and more maintainable.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function parameters.

    Encapsulates common debugging and execution context parameters that are
    passed to most route functions. This simplifies function signatures and
    makes it easier to add new context parameters in the future.

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

    def to_dict(self) -> dict:
        """Convert context to dictionary for passing to get_data.

        Returns:
            Dictionary with context parameters suitable for get_data function.
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
