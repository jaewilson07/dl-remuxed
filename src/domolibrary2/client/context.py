"""RouteContext for managing common route parameters.

This module provides a context object that encapsulates common parameters
used across route functions, making function signatures cleaner and more
maintainable.
"""

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function parameters.

    Encapsulates common parameters passed to route functions to simplify
    function signatures and provide a consistent pattern across the codebase.

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

    def to_get_data_kwargs(self) -> dict:
        """Convert context to kwargs for get_data function.

        Returns:
            Dictionary of parameters for get_data function
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
