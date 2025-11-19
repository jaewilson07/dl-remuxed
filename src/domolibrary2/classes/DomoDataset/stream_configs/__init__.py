"""Stream configuration mappings organized by platform.

This package contains stream configuration classes organized by major platform
(Snowflake, AWS, Domo, Google, etc.).

TWO PATTERNS AVAILABLE:

1. NEW PATTERN (Recommended): Typed Config Classes
   - Follows AccountConfig pattern
   - Type-safe attribute access: config.query
   - IDE autocomplete works
   - Single config object per stream

   Example:
       from domolibrary2.classes.DomoDataset.stream_configs import StreamConfig_Base
       from domolibrary2.classes.DomoDataset.stream_configs.snowflake import Snowflake_StreamConfig

       config = Snowflake_StreamConfig.from_dict({"query": "SELECT *", "databaseName": "SA_PRD"})
       query = config.query  # Type-safe, autocomplete works!

2. OLD PATTERN (Deprecated): Mapping Classes
   - Maps field names to config parameters
   - Search through list of StreamConfig objects
   - Kept for backward compatibility

   Example:
       from domolibrary2.classes.DomoDataset.stream_configs import StreamConfig_Mapping

       mapping = StreamConfig_Mappings('snowflake')
       sql_param = mapping.value.sql  # "query"
"""

# Import and re-export base classes and utilities
from ._base import (
    Stream_CRUD_Error,
    Stream_GET_Error,
    StreamConfig,
    StreamConfig_Base,
    StreamConfig_Mapping,
    StreamConfig_Mappings,
    register_mapping,
    register_stream_config,
)

# Import new typed config classes
from .snowflake import (
    Snowflake_StreamConfig,
    SnowflakeKeyPairAuth_StreamConfig,
)

__all__ = [
    # NEW PATTERN (Recommended)
    "StreamConfig_Base",
    "register_stream_config",
    # NEW: Snowflake configs
    "Snowflake_StreamConfig",
    "SnowflakeKeyPairAuth_StreamConfig",
    # OLD PATTERN (Deprecated but kept for compatibility)
    "StreamConfig_Mapping",
    "StreamConfig_Mappings",
    "StreamConfig",
    "register_mapping",
    # Route exceptions
    "Stream_GET_Error",
    "Stream_CRUD_Error",
]
