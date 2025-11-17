"""
RouteContext Module

This module provides a context class for encapsulating common parameters
used in route function calls, simplifying function signatures and improving
maintainability.

Classes:
    RouteContext: Encapsulates session, debug, and parent class information
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function calls.

    Encapsulates common parameters that are passed through route functions
    to the underlying get_data() calls. This simplifies function signatures
    and makes it easier to add new context-related parameters in the future.

    Attributes:
        session: Optional httpx AsyncClient session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None
