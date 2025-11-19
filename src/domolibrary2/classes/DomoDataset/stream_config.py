"""Stream configuration utilities.

UPDATED: This module now supports two patterns:

1. NEW PATTERN (Recommended): Typed Config Classes
   - Import from stream_configs subpackage
   - Type-safe, follows AccountConfig pattern

   from domolibrary2.classes.DomoDataset.stream_configs import (
       StreamConfig_Base,
       Snowflake_StreamConfig,
   )

2. OLD PATTERN (Deprecated): Mapping Classes
   - Still works for backward compatibility
   - Will be removed in future version

   from domolibrary2.classes.DomoDataset.stream_config import (
       StreamConfig_Mapping,
       StreamConfig_Mappings,
   )
"""

# Re-export everything from stream_configs for backward compatibility
from .stream_configs import (
    AdobeAnalyticsV2_StreamConfig,
    AmazonAthenaHighBandwidth_StreamConfig,
    AmazonS3AssumeRole_StreamConfig,
    AWSAthena_StreamConfig,
    DatasetCopy_StreamConfig,
    Default_StreamConfig,
    DomoCSV_StreamConfig,
    GoogleSheets_StreamConfig,
    GoogleSpreadsheets_StreamConfig,
    PostgreSQL_StreamConfig,
    Qualtrics_StreamConfig,
    SharePointOnline_StreamConfig,
    Snowflake_StreamConfig,
    SnowflakeKeyPairAuth_StreamConfig,
    Stream_CRUD_Error,
    Stream_GET_Error,
    StreamConfig,
    StreamConfig_Base,
    StreamConfig_Mapping,
    StreamConfig_Mappings,
    register_mapping,
    register_stream_config,
)

__all__ = [
    # NEW PATTERN (Recommended)
    "StreamConfig_Base",
    "register_stream_config",
    # Snowflake
    "Snowflake_StreamConfig",
    "SnowflakeKeyPairAuth_StreamConfig",
    # AWS
    "AWSAthena_StreamConfig",
    "AmazonAthenaHighBandwidth_StreamConfig",
    "AmazonS3AssumeRole_StreamConfig",
    # Domo
    "DatasetCopy_StreamConfig",
    "DomoCSV_StreamConfig",
    # Google
    "GoogleSheets_StreamConfig",
    "GoogleSpreadsheets_StreamConfig",
    # Other
    "AdobeAnalyticsV2_StreamConfig",
    "PostgreSQL_StreamConfig",
    "Qualtrics_StreamConfig",
    "SharePointOnline_StreamConfig",
    # Default
    "Default_StreamConfig",
    # OLD PATTERN (Deprecated)
    "StreamConfig_Mapping",
    "StreamConfig_Mappings",
    "StreamConfig",
    "register_mapping",
    # Route exceptions
    "Stream_GET_Error",
    "Stream_CRUD_Error",
]
