"""
Route Context Module

This module provides the RouteContext dataclass for consolidating common
route function parameters into a single context object.

Classes:
    RouteContext: Container for session, debug, and metadata parameters
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function execution.

    Consolidates common parameters (session, debug settings, metadata) into a single
    object that can be passed to route functions and get_data calls.

    Attributes:
        session: Optional httpx.AsyncClient session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None
