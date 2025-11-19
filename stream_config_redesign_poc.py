"""
Proof of concept: Redesigning StreamConfig to follow AccountConfig pattern.

This demonstrates how StreamConfig classes would work similar to AccountConfig classes.
"""

from dataclasses import dataclass, field
from typing import Any

# ============================================================================
# Base Class (like DomoAccount_Config)
# ============================================================================

@dataclass
class StreamConfig_Base:
    """Base class for stream configurations.
    
    Similar to DomoAccount_Config, this provides a consistent interface
    for handling stream execution parameters across different data providers.
    """
    
    data_provider_type: str = None
    parent: Any = field(repr=False, default=None)
    raw: dict = field(default_factory=dict, repr=False)
    
    # Internal fields
    _field_map: dict = field(default_factory=dict, repr=False, init=False)
    _fields_for_export: list[str] = field(default_factory=list, repr=False, init=False)
    
    @classmethod
    def from_dict(cls, obj: dict, parent: Any = None):
        """Create StreamConfig from dictionary of config parameters.
        
        Args:
            obj: Dict with config parameter names as keys
            parent: Parent stream object
            
        Returns:
            StreamConfig instance
        """
        # Get field map
        field_map = {}
        if "_field_map" in cls.__dataclass_fields__:
            field_map_field = cls.__dataclass_fields__["_field_map"]
            if hasattr(field_map_field, "default_factory"):
                field_map = field_map_field.default_factory()
        
        # Convert keys using field_map
        init_kwargs = {}
        for api_key, api_value in obj.items():
            # Check if there's a mapping
            python_attr = field_map.get(api_key)
            if not python_attr:
                # Auto-convert camelCase to snake_case
                python_attr = _camel_to_snake(api_key)
            
            # Only set if it's a field on the class
            if python_attr in cls.__dataclass_fields__:
                init_kwargs[python_attr] = api_value
        
        return cls(parent=parent, raw=obj, **init_kwargs)
    
    def to_dict(self) -> list[dict]:
        """Convert to list of config dictionaries for API submission.
        
        Returns:
            List of dicts with 'name', 'type', 'value' keys
        """
        result = []
        
        # Get reverse field map
        reverse_map = {v: k for k, v in self._field_map.items()}
        
        # Get fields to export
        export_fields = self._fields_for_export or [
            f for f in self.__dataclass_fields__.keys()
            if not f.startswith('_') and f not in ['data_provider_type', 'parent', 'raw']
        ]
        
        for attr_name in export_fields:
            value = getattr(self, attr_name, None)
            if value is not None:
                # Get API key name
                api_key = reverse_map.get(attr_name, _snake_to_camel(attr_name))
                result.append({
                    "name": api_key,
                    "type": "string",
                    "value": str(value)
                })
        
        return result


def _camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    import re
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def _snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


# ============================================================================
# Platform-Specific Configs (like DomoAccount_Config_Snowflake)
# ============================================================================

@dataclass
class Snowflake_StreamConfig(StreamConfig_Base):
    """Snowflake stream configuration."""
    
    data_provider_type: str = "snowflake"
    
    # Stream configuration parameters
    query: str = None
    database_name: str = None
    warehouse: str = None
    schema_name: str = None
    report_type: str = None
    
    _fields_for_export: list[str] = field(
        default_factory=lambda: [
            "query",
            "database_name",
            "warehouse",
            "schema_name",
            "report_type",
        ],
        repr=False,
        init=False,
    )


@dataclass
class SnowflakeKeyPair_StreamConfig(StreamConfig_Base):
    """Snowflake keypair authentication stream configuration."""
    
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


# ============================================================================
# Demo Usage
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("StreamConfig Redesign - Proof of Concept")
    print("=" * 70)
    print()
    
    # Simulate API response (list of config parameters)
    api_configs = [
        {"name": "query", "type": "string", "value": "SELECT * FROM table"},
        {"name": "databaseName", "type": "string", "value": "SA_PRD_01_ODS"},
        {"name": "schemaName", "type": "string", "value": "GAME_SALES"},
        {"name": "warehouseName", "type": "string", "value": "COMPUTE_WH"},
        {"name": "reportType", "type": "string", "value": "tables"},
        {"name": "queryTag", "type": "string", "value": "domoD2C6581a6584c1e"},
        {"name": "fetchSize", "type": "string", "value": "1000"},
        {"name": "updatemode.mode", "type": "string", "value": "REPLACE"},
        {"name": "convertTimeZone", "type": "string", "value": "UTC"},
        {"name": "cloud", "type": "string", "value": "domo"},
    ]
    
    # Convert list to dict
    config_dict = {c["name"]: c["value"] for c in api_configs}
    
    # Create stream config object
    stream_config = SnowflakeKeyPair_StreamConfig.from_dict(config_dict)
    
    print("Created StreamConfig from API response:")
    print(f"  Data Provider: {stream_config.data_provider_type}")
    print(f"  Query: {stream_config.query[:50]}...")
    print(f"  Database: {stream_config.database_name}")
    print(f"  Schema: {stream_config.schema_name}")
    print(f"  Warehouse: {stream_config.warehouse}")
    print(f"  Report Type: {stream_config.report_type}")
    print(f"  Query Tag: {stream_config.query_tag}")
    print(f"  Fetch Size: {stream_config.fetch_size}")
    print(f"  Update Mode: {stream_config.update_mode}")
    print(f"  Timezone: {stream_config.convert_timezone}")
    print(f"  Cloud: {stream_config.cloud}")
    print()
    
    # Convert back to API format
    api_output = stream_config.to_dict()
    print("Converted back to API format:")
    for config in api_output[:3]:
        print(f"  {config}")
    print(f"  ... ({len(api_output)} total)")
    print()
    
    print("=" * 70)
    print("Benefits of this approach:")
    print("=" * 70)
    print("1. ✅ Type-safe attribute access: stream_config.query")
    print("2. ✅ IDE autocomplete works")
    print("3. ✅ Follows AccountConfig pattern (familiar)")
    print("4. ✅ Can add validation, computed properties")
    print("5. ✅ Single object instead of list of configs")
    print("6. ✅ Easier to work with in code")
