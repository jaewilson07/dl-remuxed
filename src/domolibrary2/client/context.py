"""
Route Context Module

This module provides the RouteContext class for consolidating common route function
parameters into a single object, making function signatures cleaner and more maintainable.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function parameters.

    Consolidates common parameters passed to route functions and get_data calls
    to simplify function signatures and improve maintainability.

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
