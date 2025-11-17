"""
Route Context Module

This module provides the RouteContext dataclass for managing common route parameters
in a structured way, reducing parameter duplication across route functions.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function parameters.

    This class encapsulates common parameters passed to route functions,
    providing a cleaner interface and reducing parameter duplication.

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
