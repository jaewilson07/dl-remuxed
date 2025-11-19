# StreamConfig Redesign - Implementation Plan

> Branch: `feature/stream-config-redesign`
> Started: 2025-11-19

## Overview

Redesign StreamConfig to follow the AccountConfig pattern for better type safety, IDE support, and consistency across the codebase.

## Goals

1. **Type-safe config access**: `stream_config.query` instead of searching through list
2. **IDE autocomplete**: Direct property access with type hints
3. **Consistent pattern**: Match AccountConfig design
4. **Backward compatible**: Don't break existing code
5. **Easier to use**: Single config object per stream

## Current Design Problems

- Mapping objects separate from config values
- Need to search through `list[StreamConfig]` to find specific parameters
- No type safety - everything is strings
- Hard to use in IDE (no autocomplete for config keys)
- Different pattern from AccountConfig

## Proposed Design

### Base Class Structure

```python
@dataclass
class StreamConfig_Base:
    """Base class for stream configurations (similar to DomoAccount_Config)"""

    data_provider_type: str
    parent: Any = field(repr=False, default=None)
    raw: dict = field(default_factory=dict, repr=False)

    _field_map: dict = field(default_factory=dict, repr=False, init=False)
    _fields_for_export: list[str] = field(default_factory=list, repr=False, init=False)

    @classmethod
    def from_dict(cls, obj: dict, parent: Any = None) -> "StreamConfig_Base":
        """Create from dictionary of config parameters"""

    def to_dict(self) -> list[dict]:
        """Convert to list of config dicts for API submission"""
```

### Provider-Specific Classes

```python
@dataclass
class Snowflake_StreamConfig(StreamConfig_Base):
    data_provider_type: str = "snowflake"

    query: str = None
    database_name: str = None
    warehouse: str = None
    schema_name: str = None

    _fields_for_export: list[str] = field(
        default_factory=lambda: ["query", "database_name", "warehouse", "schema_name"]
    )
```

## Implementation Steps

### Phase 1: Core Infrastructure
- [x] Create proof of concept (stream_config_redesign_poc.py)
- [ ] Move base class to `stream_configs/_base.py`
- [ ] Add utility functions (`_camel_to_snake`, `_snake_to_camel`)
- [ ] Implement `from_dict()` with _field_map support
- [ ] Implement `to_dict()` with reverse mapping

### Phase 2: Provider Classes
- [ ] Convert Snowflake mappings to config classes
- [ ] Convert AWS mappings to config classes
- [ ] Convert Domo mappings to config classes
- [ ] Convert Google mappings to config classes
- [ ] Convert Other mappings to config classes
- [ ] Create default config class

### Phase 3: Integration
- [ ] Add registry for config classes (similar to account configs)
- [ ] Update stream.py to use new config objects
- [ ] Add `get_config()` method to return typed config
- [ ] Update `get_configs()` to support both old and new

### Phase 4: Testing & Documentation
- [ ] Write unit tests for base class
- [ ] Write tests for each provider class
- [ ] Test backward compatibility
- [ ] Update documentation
- [ ] Create migration guide

### Phase 5: Backward Compatibility
- [ ] Keep old StreamConfig class
- [ ] Keep old Mapping classes with deprecation warnings
- [ ] Ensure old code continues to work
- [ ] Add deprecation timeline

## File Structure

```
stream_configs/
├── _base.py              # Base classes (both old and new)
├── __init__.py           # Re-exports
├── snowflake.py          # Snowflake config classes
├── aws.py                # AWS config classes
├── domo.py               # Domo config classes
├── google.py             # Google config classes
├── other.py              # Other config classes
└── _default.py           # Default config class
```

## Benefits

1. ✅ Type-safe attribute access
2. ✅ IDE autocomplete works
3. ✅ Follows AccountConfig pattern
4. ✅ Can add validation, computed properties
5. ✅ Single object instead of list of configs
6. ✅ Easier to work with in code
7. ✅ Better error messages

## Migration Example

**Before:**
```python
configs = stream.get_configs()
query = next(c.value for c in configs if c.name == "query")
```

**After:**
```python
config = stream.get_config()  # Returns Snowflake_StreamConfig
query = config.query  # Direct access, type-safe
```

## Rollout Strategy

1. Implement new classes alongside old ones
2. Add new `get_config()` method (returns new style)
3. Keep old `get_configs()` method (returns old style)
4. Document migration path
5. Add deprecation warnings in v2.1
6. Remove old classes in v3.0

## Testing Checklist

- [ ] Base class `from_dict()` works
- [ ] Base class `to_dict()` works
- [ ] Field mapping works correctly
- [ ] All provider classes can be instantiated
- [ ] Round-trip (API → object → API) preserves data
- [ ] Backward compatibility maintained
- [ ] Old imports still work
- [ ] New imports work

## Success Criteria

- All existing tests pass
- New tests pass
- Documentation updated
- No breaking changes
- Performance equivalent or better
- Code is cleaner and more maintainable
