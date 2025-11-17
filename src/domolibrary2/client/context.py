"""Route context for standardizing common route parameters."""

__all__ = ["RouteContext"]

from dataclasses import dataclass, field
from typing import Optional

import httpx


@dataclass
class RouteContext:
    """Container for common route function parameters.

    This class standardizes how route functions handle common parameters like
    session management, debugging, and parent class tracking. It allows for
    cleaner function signatures and easier parameter passing.

    Attributes:
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
    """

    session: httpx.AsyncClient | None = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None
