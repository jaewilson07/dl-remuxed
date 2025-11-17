"""RouteContext for encapsulating common route parameters.

This module provides the RouteContext class which bundles commonly-used
parameters across route functions, simplifying function signatures and
enabling cleaner parameter passing.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function calls.

    Encapsulates common parameters passed to route functions and get_data(),
    providing a cleaner API and reducing parameter duplication.

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
