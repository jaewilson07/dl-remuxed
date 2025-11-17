"""
Route Context Module

This module provides the RouteContext class for encapsulating common route parameters.

Classes:
    RouteContext: Encapsulates session, debug, and parent class information for route functions
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route functions containing common parameters.

    This class encapsulates the common parameters passed to route functions
    to simplify function signatures and improve consistency across the codebase.

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
        """Convert context to dictionary for unpacking into get_data calls.

        Returns:
            Dictionary with all context parameters
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
