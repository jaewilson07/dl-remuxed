"""Snowflake stream configuration mappings."""

from dataclasses import dataclass, field

from ._base import (
    StreamConfig_Base,
    StreamConfig_Mapping,
    register_mapping,
    register_stream_config,
)

__all__ = [
    # Old pattern (mappings - deprecated but kept for compatibility)
    "SnowflakeMapping",
    "SnowflakeFederatedMapping",
    "SnowflakeInternalUnloadMapping",
    "SnowflakeKeypairAuthMapping",
    "SnowflakeKeypairInternalManagedUnloadMapping",
    "SnowflakeUnloadV2Mapping",
    "SnowflakeWritebackMapping",
    # New pattern (typed configs - recommended)
    "Snowflake_StreamConfig",
    "SnowflakeKeyPairAuth_StreamConfig",
]


@register_mapping("snowflake")
@dataclass
class SnowflakeMapping(StreamConfig_Mapping):
    """Snowflake data provider mapping."""

    data_provider_type: str = "snowflake"
    sql: str = "query"
    warehouse: str = "warehouseName"
    database_name: str = "databaseName"


@register_mapping("snowflake_federated")
@dataclass
class SnowflakeFederatedMapping(StreamConfig_Mapping):
    """Snowflake federated data provider mapping."""

    data_provider_type: str = "snowflake_federated"


@register_mapping("snowflake-internal-unload")
@dataclass
class SnowflakeInternalUnloadMapping(StreamConfig_Mapping):
    """Snowflake internal unload data provider mapping."""

    data_provider_type: str = "snowflake-internal-unload"
    sql: str = "customQuery"
    database_name: str = "databaseName"
    warehouse: str = "warehouseName"


@register_mapping("snowflakekeypairauthentication")
@dataclass
class SnowflakeKeypairAuthMapping(StreamConfig_Mapping):
    """Snowflake keypair authentication data provider mapping."""

    data_provider_type: str = "snowflakekeypairauthentication"
    sql: str = "query"
    database_name: str = "databaseName"
    schema_name: str = "schemaName"
    warehouse: str = "warehouseName"
    report_type: str = "reportType"
    query_tag: str = "queryTag"
    fetch_size: str = "fetchSize"
    update_mode: str = "updatemode.mode"
    convert_timezone: str = "convertTimeZone"
    cloud: str = "cloud"


@register_mapping("snowflake-keypair-internal-managed-unload")
@dataclass
class SnowflakeKeypairInternalManagedUnloadMapping(StreamConfig_Mapping):
    """Snowflake keypair internal managed unload data provider mapping."""

    data_provider_type: str = "snowflake-keypair-internal-managed-unload"
    sql: str = "customQuery"
    database_name: str = "databaseName"
    warehouse: str = "warehouseName"


@register_mapping("snowflake_unload_v2")
@dataclass
class SnowflakeUnloadV2Mapping(StreamConfig_Mapping):
    """Snowflake unload v2 data provider mapping."""

    data_provider_type: str = "snowflake_unload_v2"
    sql: str = "query"
    warehouse: str = "warehouseName"
    database_name: str = "databaseName"


@register_mapping("snowflake-writeback")
@dataclass
class SnowflakeWritebackMapping(StreamConfig_Mapping):
    """Snowflake writeback data provider mapping."""

    data_provider_type: str = "snowflake-writeback"
    table_name: str = "enterTableName"
    database_name: str = "databaseName"
    warehouse: str = "warehouseName"


# ============================================================================
# NEW PATTERN: Typed Stream Config Classes (Recommended)
# ============================================================================


@register_stream_config("snowflake")
@dataclass
class Snowflake_StreamConfig(StreamConfig_Base):
    """Snowflake stream configuration (typed, follows AccountConfig pattern).

    Provides type-safe access to Snowflake stream parameters.

    Example:
        >>> config = Snowflake_StreamConfig.from_dict({
        ...     "query": "SELECT * FROM table",
        ...     "databaseName": "SA_PRD",
        ...     "warehouseName": "COMPUTE_WH"
        ... })
        >>> config.query  # Type-safe attribute access
        "SELECT * FROM table"
        >>> config.database_name
        "SA_PRD"
    """

    data_provider_type: str = "snowflake"

    # Stream configuration parameters
    query: str = None
    database_name: str = None
    warehouse: str = None
    schema_name: str = None

    _field_map: dict = field(
        default_factory=lambda: {
            "warehouseName": "warehouse",  # Special case - avoid warehouse_name
        },
        repr=False,
        init=False,
    )

    _fields_for_export: list[str] = field(
        default_factory=lambda: [
            "query",
            "database_name",
            "warehouse",
            "schema_name",
        ],
        repr=False,
        init=False,
    )


@register_stream_config("snowflakekeypairauthentication")
@dataclass
class SnowflakeKeyPairAuth_StreamConfig(StreamConfig_Base):
    """Snowflake keypair authentication stream configuration.

    Includes additional fields for keypair auth (query tags, fetch size, etc.).

    Example:
        >>> config = SnowflakeKeyPairAuth_StreamConfig.from_dict({
        ...     "query": "SELECT * FROM table",
        ...     "databaseName": "SA_PRD",
        ...     "queryTag": "domoD2C123",
        ...     "fetchSize": "1000"
        ... })
        >>> config.query_tag
        "domoD2C123"
    """

    data_provider_type: str = "snowflakekeypairauthentication"

    # Stream configuration parameters
    query: str = None
    database_name: str = None
    schema_name: str = None
    warehouse: str = None
    report_type: str = None
    query_tag: str = None
    fetch_size: str = None
    update_mode: str = None
    convert_timezone: str = None
    cloud: str = None

    _field_map: dict = field(
        default_factory=lambda: {
            "warehouseName": "warehouse",  # Special case - avoid warehouse_name
            "updatemode.mode": "update_mode",  # Special case with dot notation
        },
        repr=False,
        init=False,
    )

    _fields_for_export: list[str] = field(
        default_factory=lambda: [
            "query",
            "database_name",
            "schema_name",
            "warehouse",
            "report_type",
            "query_tag",
            "fetch_size",
            "update_mode",
            "convert_timezone",
            "cloud",
        ],
        repr=False,
        init=False,
    )
