"""Base classes and utilities for stream configuration mappings.

This module contains:
- StreamConfig_Mapping: Base class for all provider-specific mappings
- StreamConfig: Individual stream configuration item
- StreamConfig_Mappings: Enum for accessing registered mappings
- register_mapping: Decorator for registering new mappings
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from sqlglot import exp, parse_one

from ....base.base import DomoBase, DomoEnumMixin
from ....routes.stream import Stream_CRUD_Error, Stream_GET_Error

__all__ = [
    "StreamConfig_Mapping",
    "StreamConfig_Mappings",
    "StreamConfig",
    "register_mapping",
    # Route exceptions
    "Stream_GET_Error",
    "Stream_CRUD_Error",
]

# Registry to store mapping classes
_MAPPING_REGISTRY: dict[str, type["StreamConfig_Mapping"]] = {}


def register_mapping(data_provider_type: str):
    """Decorator to register a StreamConfig_Mapping subclass.

    Args:
        data_provider_type: The data provider type identifier (e.g., 'snowflake')

    Example:
        @register_mapping('snowflake')
        @dataclass
        class SnowflakeMapping(StreamConfig_Mapping):
            sql: str = "query"
            warehouse: str = "warehouseName"
            database_name: str = "databaseName"
    """

    def decorator(cls: type[StreamConfig_Mapping]) -> type[StreamConfig_Mapping]:
        _MAPPING_REGISTRY[data_provider_type] = cls
        return cls

    return decorator


@dataclass
class StreamConfig_Mapping(DomoBase):
    """Base class for stream configuration mappings.
    
    Maps Python attribute names to stream configuration parameter names.
    Subclass this for each data provider type.
    """
    
    data_provider_type: str | None = None

    sql: str = None
    warehouse: str = None
    database_name: str = None
    s3_bucket_category: str = None

    is_default: bool = False

    table_name: str = None
    src_url: str = None
    google_sheets_file_name: str = None
    adobe_report_suite_id: str = None
    qualtrics_survey_id: str = None

    def search_keys_by_value(
        self,
        value_to_search: str,
    ) -> StreamConfig_Mapping | None:
        """Search for Python attribute name by stream config parameter name.
        
        Args:
            value_to_search: Stream config parameter name to search for
            
        Returns:
            Python attribute name if found, None otherwise
        """
        if self.is_default:
            if value_to_search in ["enteredCustomQuery", "query", "customQuery"]:
                return "sql"

        return next(
            (key for key, value in asdict(self).items() if value == value_to_search),
            None,
        )


# ============================================================================
# StreamConfig and StreamConfig_Mappings must be defined before platform imports
# ============================================================================


@dataclass
class StreamConfig:
    """Individual stream configuration parameter.
    
    Represents a single configuration parameter in a stream execution,
    such as a SQL query, database name, warehouse, etc.
    """
    
    stream_category: str
    name: str
    type: str
    value: str
    value_clean: str = None
    parent: Any = field(repr=False, default=None)

    def __post_init__(self):
        # self.value_clean = self.value.replace("\n", " ")
        # sc.value_clean = re.sub(" +", " ", sc.value_clean)

        if self.stream_category == "sql" and self.parent:
            self.process_sql()

    def process_sql(self):
        """Extract table names from SQL query using sqlglot parser."""
        if not self.parent:
            return None

        self.parent.configuration_query = self.value

        try:
            for table in parse_one(self.value).find_all(exp.Table):
                self.parent.configuration_tables.append(table.name.lower())
                self.parent.configuration_tables = sorted(
                    list(set(self.parent.configuration_tables))
                )
        except Exception:
            return None

        return self.parent.configuration_tables

    @classmethod
    def from_json(cls, obj: dict, data_provider_type: str, parent_stream: Any = None):
        """Create StreamConfig from API JSON response.
        
        Args:
            obj: JSON object with 'name', 'type', 'value' keys
            data_provider_type: Data provider type (e.g., 'snowflake')
            parent_stream: Parent stream object
            
        Returns:
            StreamConfig instance
        """
        config_name = obj["name"]

        # Use standard enum access - triggers _missing_ if not found
        mapping_enum = StreamConfig_Mappings.get(data_provider_type)

        stream_category = "default"
        if mapping_enum and mapping_enum.value:
            stream_category = mapping_enum.value.search_keys_by_value(config_name)

            if parent_stream:
                parent_stream.has_mapping = True

        return cls(
            stream_category=stream_category,
            name=config_name,
            type=obj["type"],
            value=obj["value"],
            parent=parent_stream,
        )

    def to_dict(self):
        """Convert to dictionary for API submission.
        
        Returns:
            Dict with 'field', 'key', 'value' keys
        """
        return {"field": self.stream_category, "key": self.name, "value": self.value}


# ============================================================================
# Import platform-specific mappings to trigger registration
# ============================================================================

# Import all mappings from the stream_configs submodules
# This triggers the @register_mapping decorators and populates _MAPPING_REGISTRY
from . import _default, aws, domo, google, other, snowflake  # noqa: E402, F401

# ============================================================================
# StreamConfig_Mappings Enum (Auto-generated from registry)
# ============================================================================


class StreamConfig_Mappings(DomoEnumMixin, Enum):
    """Enum of all registered stream config mappings.

    This enum is automatically populated from the registry created by
    @register_mapping decorators. To add a new mapping, simply create a
    new subclass with the @register_mapping decorator in the appropriate
    platform file.
    
    Usage:
        mapping = StreamConfig_Mappings.get('snowflake')
        sql_param = mapping.value.sql  # "query"
    """

    # Explicit default member to prevent AttributeError
    default = None  # Will be set dynamically via _missing_

    @classmethod
    def _missing_(cls, value):
        """Handle missing enum values by searching the registry."""
        alt_search = value.lower().replace("-", "_")

        # Try direct registry lookup
        if value in _MAPPING_REGISTRY:
            mapping_cls = _MAPPING_REGISTRY[value]
            return cls._create_pseudo_member(value, mapping_cls())

        # Try normalized search
        for key, mapping_cls in _MAPPING_REGISTRY.items():
            if key.lower().replace("-", "_") == alt_search:
                return cls._create_pseudo_member(key, mapping_cls())

        # Return default
        return cls.default
