"""
RouteContext - Context object for route function calls.

This module provides a context object that bundles commonly-passed parameters
(session, debug_api, debug_num_stacks_to_drop, parent_class) into a single
object for cleaner function signatures.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function calls.

    Bundles commonly-passed parameters into a single object for cleaner
    function signatures while maintaining backward compatibility.

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
