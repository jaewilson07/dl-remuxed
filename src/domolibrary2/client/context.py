"""
RouteContext - Encapsulates common routing parameters.

This module provides a context object that bundles common parameters passed to route
functions, simplifying function signatures and improving maintainability.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """
    Context object for route function parameters.

    Encapsulates common parameters that are passed to most route functions,
    allowing for cleaner function signatures and easier parameter management.

    Attributes:
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert context to dictionary for unpacking into function calls.

        Returns:
            Dictionary representation of context attributes
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
