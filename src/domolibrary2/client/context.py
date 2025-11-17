"""
RouteContext - Context object for route function calls.

This module provides a dataclass to encapsulate common parameters passed to
route functions, reducing parameter clutter and improving maintainability.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object that bundles common route function parameters.

    This class consolidates parameters that are frequently passed through
    route functions to the underlying get_data calls.

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
