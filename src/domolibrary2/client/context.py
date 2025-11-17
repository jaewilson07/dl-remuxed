"""Route context for API request configuration.

This module provides the RouteContext dataclass for consolidating
debug and session parameters across route functions.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import httpx


@dataclass
class RouteContext:
    """Context object for route function execution.

    Consolidates debugging and session parameters that are commonly
    passed to route functions and get_data calls.

    Attributes:
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: "httpx.AsyncClient | None" = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None
