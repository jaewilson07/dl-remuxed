"""
RouteContext - Context object for route function execution.

This module provides the RouteContext class which encapsulates common
parameters passed to route functions, making function signatures cleaner
and enabling easier parameter management.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function execution.

    Encapsulates common parameters used across route functions including
    session management, debugging flags, and parent class information.

    Attributes:
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Name of calling class for debugging context
    """

    session: httpx.AsyncClient | None = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert RouteContext to dictionary for get_data() calls.

        Returns:
            Dictionary containing context parameters for get_data()
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
