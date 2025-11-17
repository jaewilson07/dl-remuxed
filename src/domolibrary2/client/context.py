"""Route context management for Domo API calls.

This module provides the RouteContext class for consolidating common
parameters used across route functions and get_data calls.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass, field
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function calls.

    Consolidates debugging and control parameters for cleaner function signatures.

    Attributes:
        session: Optional httpx AsyncClient for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert context to dictionary for unpacking.

        Returns:
            Dictionary containing all context parameters
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }

    @classmethod
    def from_params(
        cls,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 1,
        parent_class: Optional[str] = None,
    ) -> "RouteContext":
        """Create RouteContext from individual parameters.

        Args:
            session: Optional httpx client session for connection reuse
            debug_api: Enable detailed API request/response logging
            debug_num_stacks_to_drop: Number of stack frames to drop in debug output
            parent_class: Optional parent class name for debugging context

        Returns:
            New RouteContext instance
        """
        return cls(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )
