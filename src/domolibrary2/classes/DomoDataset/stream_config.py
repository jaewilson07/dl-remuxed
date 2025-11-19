"""Stream configuration utilities.

DEPRECATED: This module is kept for backward compatibility.
All functionality has been moved to the stream_configs subpackage.

New imports should use:
    from domolibrary2.classes.DomoDataset.stream_configs import (
        StreamConfig,
        StreamConfig_Mapping,
        StreamConfig_Mappings,
        register_mapping,
    )
"""

# Re-export everything from stream_configs for backward compatibility
from .stream_configs import (
    Stream_CRUD_Error,
    Stream_GET_Error,
    StreamConfig,
    StreamConfig_Mapping,
    StreamConfig_Mappings,
    register_mapping,
)

__all__ = [
    "StreamConfig_Mapping",
    "StreamConfig_Mappings",
    "StreamConfig",
    "register_mapping",
    # Route exceptions
    "Stream_GET_Error",
    "Stream_CRUD_Error",
]
