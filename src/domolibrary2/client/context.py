"""
RouteContext Module

This module provides the RouteContext dataclass for encapsulating common
route function parameters like session, debug settings, and parent class context.

Classes:
    RouteContext: Encapsulates common route function parameters
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """
    Encapsulates common route function parameters.

    This class provides a cleaner way to pass common debugging and session
    parameters to route functions, reducing parameter clutter and improving
    maintainability.

    Attributes:
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: httpx.AsyncClient | None = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_get_data_kwargs(self) -> dict:
        """
        Convert RouteContext to kwargs dict for get_data() calls.

        Returns:
            Dictionary with keys: session, debug_api, debug_num_stacks_to_drop, parent_class
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
