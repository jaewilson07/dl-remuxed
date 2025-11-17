"""Route Context Module

This module provides the RouteContext class for consolidating route function parameters.

Classes:
    RouteContext: Container for route execution context (session, debugging, etc.)
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Container for route execution context parameters.

    This class consolidates common route parameters like session, debugging flags,
    and parent class information into a single object for cleaner function signatures.

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
        """Convert RouteContext to dictionary for get_data calls.

        Returns:
            Dictionary with context parameters for get_data function
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
