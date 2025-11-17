"""
RouteContext - Parameter bundling for route functions.

This module provides the RouteContext dataclass which bundles common parameters
passed to route functions, reducing parameter repetition and improving maintainability.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object bundling common route function parameters.
    
    This dataclass encapsulates parameters commonly passed to route functions,
    enabling cleaner function signatures and easier parameter management.
    
    Attributes:
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """
    
    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None
