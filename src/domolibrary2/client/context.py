"""Route context for API request configuration.

This module provides the RouteContext dataclass for consolidating
debug and session parameters across route functions.
"""

from dataclasses import dataclass

import httpx
from dc_logger import LogLevel


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
        log_level: Optional log level for the request
    """

    session: httpx.AsyncClient | None = None
    debug_num_stacks_to_drop: int = 1
    parent_class: str | None = None
    log_level: LogLevel | str | None = LogLevel.INFO
    debug_api: bool = False

    @classmethod
    def build_context(
        cls,
        context: "RouteContext | None" = None,
        **kwargs,
    ) -> "RouteContext":
        """Build RouteContext from either existing context or individual parameters.

        This helper allows route functions to accept either a pre-built context
        or individual parameters, enabling clean signatures while maintaining
        backward compatibility.

        Args:
            context: Optional pre-built RouteContext
            **kwargs: Individual context parameters (session, debug_api, debug_num_stacks_to_drop,
                    parent_class, log_level)

        Returns:
            RouteContext built from provided parameters

        Example:
            >>> # In a route function
            >>> def my_route(auth, *, context=None, **context_kwargs):
            ...     context = build_context(context, **context_kwargs)
            ...     res = await get_data(auth=auth, url=url, context=context)
        """
        if context is not None:
            return context

        return RouteContext(
            session=kwargs.get("session"),
            debug_api=kwargs.get("debug_api", False),
            debug_num_stacks_to_drop=kwargs.get("debug_num_stacks_to_drop", 1),
            parent_class=kwargs.get("parent_class"),
            log_level=kwargs.get("log_level", LogLevel.INFO),
        )
