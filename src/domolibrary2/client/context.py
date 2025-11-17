"""
Route Context Module

Provides a context object for passing common route parameters
to simplify function signatures and improve maintainability.
"""

__all__ = ["RouteContext"]

from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """
    Context object for route function parameters.

    Encapsulates common parameters passed to route functions to simplify
    signatures and improve code maintainability. This object can be passed
    to get_data() to provide session, debugging, and metadata information.

    Attributes:
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context

    Example:
        >>> context = RouteContext(
        ...     session=my_session,
        ...     debug_api=True,
        ...     parent_class="DomoDataset"
        ... )
        >>> res = await get_data(auth=auth, url=url, context=context)
    """

    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert context to dictionary for unpacking.

        Returns:
            Dictionary with all context attributes

        Example:
            >>> context = RouteContext(debug_api=True)
            >>> params = context.to_dict()
            >>> # Use as **params in function calls
        """
        return {
            "session": self.session,
            "debug_api": self.debug_api,
            "debug_num_stacks_to_drop": self.debug_num_stacks_to_drop,
            "parent_class": self.parent_class,
        }
