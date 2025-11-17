"""
Route Context Module

This module provides the RouteContext dataclass for bundling common route
function parameters into a single context object. This simplifies function
signatures and makes it easier to pass around related configuration.

Classes:
    RouteContext: Context object for route function parameters
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function parameters.

    This class bundles common route function parameters (session, debug flags,
    parent class) into a single context object. This simplifies function signatures
    and makes it easier to add new context fields without changing all function
    signatures.

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
