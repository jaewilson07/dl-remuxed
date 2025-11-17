# Register Pattern Design Guide

> Last updated: 2025-11-17

## Overview

The **register pattern** is a design pattern that uses decorators and runtime registration to build dynamic type systems without hardcoding enumerations. This pattern is particularly useful when you need extensibility, plugin architectures, or when the set of possible types is unknown at compile time.

## Register Pattern vs Enums

### When to Use Enums

Use `DomoEnumMixin` + `Enum` when:

1. **Fixed, known set of values** - The complete list is defined at design time
2. **Validation is primary goal** - You need type safety and compile-time checking
3. **Simple value mapping** - Direct string/value correspondence with no complex behavior
4. **API contract enforcement** - The enum represents official API values

**Example (Good Use):**
```python
class Collection_Permission_Enum(DomoEnumMixin, Enum):
    READ_CONTENT = "READ_CONTENT"
    ADMIN = "ADMIN"
    UPDATE_CONTENT = "UPDATE_CONTENT"
```

✅ **Why this is good:** These are the only 3 permission values the API accepts. They're stable and well-defined.

### When to Use Register Pattern

Use the register pattern when:

1. **Extensibility is required** - New types can be added without modifying core code
2. **Type-specific behavior** - Each registered type has its own implementation class
3. **Plugin architecture** - Third parties or future modules need to add types
4. **Discovery and factory creation** - You need to look up and instantiate types dynamically
5. **Open/Closed Principle** - Code should be open for extension, closed for modification

**Example (Good Use):**
```python
# Registry pattern for stream config mappings
_MAPPING_REGISTRY: dict[str, type["StreamConfig_Mapping"]] = {}

@register_mapping("snowflake")
@dataclass
class SnowflakeMapping(StreamConfig_Mapping):
    sql: str = "query"
    warehouse: str = "warehouseName"
    database_name: str = "databaseName"
```

✅ **Why this is good:** New data provider types can be added by creating new classes with the decorator. The core `StreamConfig` code doesn't need to change.

## Architecture Comparison

### Enum Architecture
```
Route Function → Enum Validation → API Call
                 ↓ (compile time)
            Fixed set of values
```

**Characteristics:**
- Type safety at design time
- No runtime discovery
- Modification requires code changes in enum definition
- Simple value → string mapping

### Register Pattern Architecture
```
Decorator → Registry → Factory → Instance Creation
    ↓          ↓          ↓
(module load)(lookup)(dynamic)
```

**Characteristics:**
- Types discovered at runtime
- Extensible without core code changes
- Complex type-specific behavior
- Dynamic instantiation from registry

## Implementation Guide

### Basic Register Pattern Setup

```python
# 1. Define the registry
_CONTROLLER_REGISTRY: dict[str, type["AccessController"]] = {}

# 2. Create the decorator
def register_controller(object_type: str):
    """Register an access controller for a specific object type."""
    def decorator(cls: type[AccessController]) -> type[AccessController]:
        _CONTROLLER_REGISTRY[object_type] = cls
        return cls
    return decorator

# 3. Define base class
@dataclass
class AccessController(ABC):
    auth: DomoAuth
    parent_object: DomoEntity
    
    @abstractmethod
    async def grant_access(self, entity_id: str, access_level: str) -> bool:
        pass

# 4. Register implementations
@register_controller("dataset")
class DatasetAccessController(AccessController):
    async def grant_access(self, entity_id: str, access_level: str) -> bool:
        # Dataset-specific implementation
        return await dataset_routes.share_dataset(...)

@register_controller("page")
class PageAccessController(AccessController):
    async def grant_access(self, entity_id: str, access_level: str) -> bool:
        # Page-specific implementation
        return await page_routes.share_page(...)

# 5. Factory function for retrieval
def get_controller(object_type: str) -> type[AccessController] | None:
    return _CONTROLLER_REGISTRY.get(object_type)
```

### Auto-Generating Enum from Registry

You can combine both patterns when you need both extensibility AND an enum interface:

```python
class StreamConfig_Mappings(DomoEnumMixin, Enum):
    """Auto-generated enum from registry."""
    
    default = None
    
    @classmethod
    def _missing_(cls, value):
        """Handle missing values by searching registry."""
        if value in _MAPPING_REGISTRY:
            mapping_cls = _MAPPING_REGISTRY[value]
            return cls._create_pseudo_member_(value, mapping_cls())
        return cls.default
    
    @classmethod
    def search(cls, value, debug_api: bool = False) -> StreamConfig_Mapping:
        """Search for a mapping by data provider type."""
        if value in _MAPPING_REGISTRY:
            return _MAPPING_REGISTRY[value]()
        
        if debug_api:
            print(f"{value} not in registry, using default")
        
        return _MAPPING_REGISTRY.get("default", StreamConfig_Mapping)()
```

✅ **Benefits:** Provides enum-like interface while maintaining extensibility through registry.

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Enum for Extensible Types

**Bad:**
```python
class DataProvider_Enum(DomoEnumMixin, Enum):
    SNOWFLAKE = "snowflake"
    POSTGRESQL = "postgresql"
    ADOBE = "adobe-analytics-v2"
    QUALTRICS = "qualtrics"
    # ... 50+ more providers
    
    # What happens when Domo adds a new connector?
    # → Must modify this file
    # → Breaks Open/Closed Principle
```

**Good (Register Pattern):**
```python
@register_mapping("new-connector")
@dataclass
class NewConnectorMapping(StreamConfig_Mapping):
    custom_field: str = "customFieldName"
```

### ❌ Anti-Pattern 2: Register Pattern for Simple Values

**Bad:**
```python
# Overkill for simple permission values
@register_permission("READ")
class ReadPermission:
    value = "READ_CONTENT"

@register_permission("ADMIN")
class AdminPermission:
    value = "ADMIN"
```

**Good (Enum):**
```python
class Permission(DomoEnumMixin, Enum):
    READ = "READ_CONTENT"
    ADMIN = "ADMIN"
```

### ❌ Anti-Pattern 3: Manual isinstance() Checks

**Problem in current codebase:**
```python
# Appears in multiple route functions
if isinstance(group_type, GroupType_Enum):
    group_type = group_type.value

# Repetitive pattern across 9+ locations
if isinstance(permission, Collection_Permission_Enum):
    permission = permission.value
```

**Better Design:**
```python
# Option 1: Handle at function boundary
@gd.route_function
async def create_group(
    auth: DomoAuth,
    group_type: Union[GroupType_Enum, str] = "open",
    ...
):
    # Normalize once at the top
    group_type = group_type.value if isinstance(group_type, GroupType_Enum) else group_type
    
    # Rest of function uses normalized value

# Option 2: Utility function
def normalize_enum(value: Enum | str) -> str:
    """Convert enum to string value, or pass through string."""
    return value.value if isinstance(value, Enum) else value

# Usage
group_type = normalize_enum(group_type)
```

**Best Design (if using enums):**
```python
# Accept only enum, convert internally
@gd.route_function  
async def create_group(
    auth: DomoAuth,
    group_type: GroupType_Enum = GroupType_Enum.OPEN,
    ...
):
    # Always use .value, no isinstance checks needed
    body = {"type": group_type.value}
```

## Migration Strategy

### Identifying Conversion Candidates

**Enums that should become Register Pattern:**

1. ✅ `StreamConfig_Mappings` - Already migrated
   - 10+ data provider types
   - Each has unique field mappings
   - New connectors added frequently

2. ✅ Access Controllers - Already using register pattern
   - Different object types (dataset, page, card, account)
   - Type-specific implementation
   - Extensible for new object types

3. ⚠️ **Consider:** `Datacenter_Enum`
   ```python
   class Datacenter_Enum(DomoEnumMixin, Enum):
       DATASET = "DATASET"
       CARD = "CARD"
       PAGE = "PAGE"
       DATAFLOW = "DATAFLOW"
       # ... 10+ more entity types
   ```
   - **Analysis:** Could use register pattern if each entity type needs specific handling
   - **Decision:** Keep as enum if just used for type identification
   - **Convert if:** Need entity-specific behavior (e.g., different search implementations)

**Enums that should stay as Enums:**

1. ✅ `Collection_Permission_Enum` - Simple, fixed API values
2. ✅ `GroupType_Enum` - Fixed set defined by API
3. ✅ `UserProperty_Type` - Stable API property names
4. ✅ `OutputStyleEnum` - AI output format options

## Testing Register Pattern

### Unit Tests for Registry

```python
async def test_register_pattern():
    """Test that decorator populates registry correctly."""
    
    # Verify registration
    assert "snowflake" in _MAPPING_REGISTRY
    assert "postgresql" in _MAPPING_REGISTRY
    
    # Verify factory creation
    mapping = StreamConfig_Mappings.search("snowflake")
    assert isinstance(mapping, SnowflakeMapping)
    assert mapping.sql == "query"
    
    # Verify fallback behavior
    mapping = StreamConfig_Mappings.search("unknown-type", debug_api=False)
    assert isinstance(mapping, StreamConfig_Mapping)  # Default
    
    # Verify case-insensitive search
    mapping = StreamConfig_Mappings.search("SNOWFLAKE")
    assert isinstance(mapping, SnowflakeMapping)
```

### Integration Tests

```python
async def test_end_to_end_stream_config():
    """Test register pattern in real usage."""
    
    # Create stream with registered type
    stream = await DomoStream.get_by_id(auth=auth, stream_id="test-id")
    
    # Verify mapping was found via registry
    assert stream.has_mapping is True
    assert "snowflake" in stream.configuration_query
```

## Best Practices

### 1. Clear Registration Point

```python
# ✅ Explicit import statement to trigger registration
import domolibrary2.classes.DomoDataset.stream_configs  # noqa: F401

# Document why the import exists
# This triggers @register_mapping decorators
```

### 2. Defensive Registry Lookups

```python
# ✅ Always provide fallback
mapping = _MAPPING_REGISTRY.get(provider_type, DefaultMapping)

# ✅ Log when fallback is used
if debug_api and provider_type not in _MAPPING_REGISTRY:
    print(f"Provider {provider_type} not registered, using default")
```

### 3. Type Hints on Registry

```python
# ✅ Type the registry for IDE support
_MAPPING_REGISTRY: dict[str, type[StreamConfig_Mapping]] = {}
```

### 4. Documentation of Registered Types

```python
class StreamConfig_Mappings(DomoEnumMixin, Enum):
    """Enum of all registered stream config mappings.
    
    Currently registered types:
    - snowflake
    - snowflake_federated
    - snowflake-internal-unload
    - postgresql
    - adobe-analytics-v2
    - qualtrics
    - sharepointonline
    
    To add a new mapping, create a subclass with @register_mapping decorator
    in the stream_configs subfolder.
    """
```

## Performance Considerations

### Registry Initialization

- Registration happens at module import time
- One-time cost, cached for application lifetime
- Minimal overhead compared to enum

### Lookup Performance

```python
# O(1) dictionary lookup - same as enum
controller_class = _REGISTRY[object_type]

# Instantiation cost - only when needed
controller = controller_class(auth, object)
```

### Memory Usage

- Registry holds class references, not instances
- Instances created on-demand
- More memory efficient than pre-instantiated enum values with complex objects

## Conclusion

**Use the register pattern when:**
- You need extensibility without modifying core code
- Each type has unique behavior or implementation
- Types may be added by plugins or future modules
- You need dynamic type discovery and factory creation

**Use enums when:**
- The set of values is fixed and known
- You need simple value validation
- Type safety at compile time is valuable
- No type-specific behavior required

The register pattern is already successfully used in domolibrary2 for:
1. `StreamConfig_Mapping` - Data provider configurations
2. `DomoAccessController` - Object type-specific access control
3. `DomoRelationshipController` - Object type-specific relationships

Consider adopting it for other extensible type systems in the future.
