"""
RouteContext - Context object for route function execution.

This module provides a context object that encapsulates common parameters
passed to route functions, making the API cleaner and more maintainable.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function execution.
    
    Consolidates common debugging and session parameters into a single object,
    making route function signatures cleaner and more maintainable.
    
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
