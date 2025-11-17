"""
RouteContext - Encapsulates common routing parameters

This module provides a dataclass to encapsulate common parameters passed to route functions,
reducing parameter duplication and improving maintainability.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function parameters.
    
    Encapsulates common parameters used across route functions including
    session management, debugging options, and parent class tracking.
    
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
