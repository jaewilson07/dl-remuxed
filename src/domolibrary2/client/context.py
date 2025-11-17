"""
Route Context Module

This module provides the RouteContext class for bundling common route parameters.

Classes:
    RouteContext: Container for route execution context parameters
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """
    Container for route execution context parameters.

    This class bundles together common parameters that are passed to route functions
    and get_data() calls, providing a cleaner interface and reducing parameter clutter.

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
        """Convert context to dictionary for passing to get_data()."""
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
