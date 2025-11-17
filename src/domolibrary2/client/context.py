"""
Route Context Module

This module provides the RouteContext class for managing request context
parameters in a unified way across route functions.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Context object for route function calls.

    Consolidates common parameters (session, debug flags, parent class info)
    into a single object that can be passed through the call chain.

    This pattern:
    - Reduces parameter repetition in function signatures
    - Makes it easier to add new context fields without changing all signatures
    - Provides a clear separation between business logic params and context params
    - Maintains backward compatibility through optional parameters

    Attributes:
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context

    Example:
        >>> context = RouteContext(debug_api=True, session=my_session)
        >>> res = await some_route_function(auth=auth, entity_id="123", context=context)
    """

    session: httpx.AsyncClient | None = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert context to dictionary format for legacy compatibility.

        Returns:
            Dictionary with context parameters suitable for passing to get_data
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
