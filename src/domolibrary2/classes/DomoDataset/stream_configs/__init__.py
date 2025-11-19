"""Stream configuration mappings organized by platform.

This package contains stream configuration mapping subclasses organized by
major platform (Snowflake, AWS, Domo, Google, etc.). Each mapping is
automatically registered using the @register_mapping decorator.

To add a new mapping:
1. Choose the appropriate platform file (or create a new one)
2. Define a subclass of StreamConfig_Mapping
3. Decorate it with @register_mapping("provider-name")
4. The mapping will be automatically registered

Example:
    from ._base import StreamConfig_Mapping, register_mapping
    from dataclasses import dataclass

    @register_mapping("my-provider")
    @dataclass
    class MyProviderMapping(StreamConfig_Mapping):
        data_provider_type: str = "my-provider"
        sql: str = "query"
"""

# Import and re-export base classes and utilities
from ._base import (
    StreamConfig,
    StreamConfig_Mapping,
    StreamConfig_Mappings,
    register_mapping,
    Stream_CRUD_Error,
    Stream_GET_Error,
)

__all__ = [
    # Base classes
    "StreamConfig_Mapping",
    "StreamConfig_Mappings",
    "StreamConfig",
    "register_mapping",
    # Route exceptions
    "Stream_GET_Error",
    "Stream_CRUD_Error",
]
