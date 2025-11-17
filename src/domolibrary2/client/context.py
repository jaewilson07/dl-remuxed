"""
RouteContext - Context object for route function parameters.

This module provides a context object that bundles common route function parameters
like session, debug flags, and parent class information. This simplifies function
signatures and makes it easier to pass around these related parameters.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function parameters.
    
    Bundles common parameters used across route functions to simplify
    function signatures and provide a consistent way to pass debugging
    and session information.
    
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
    
    def to_dict(self) -> dict:
        """Convert context to dictionary for unpacking into function calls.
        
        Returns:
            Dictionary with context parameters
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
