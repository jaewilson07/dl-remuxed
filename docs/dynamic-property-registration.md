# Dynamic Property Registration for Conformed Properties

## Overview

Instead of manually defining each conformed property as a `@property` method on `DomoStream`, we can **dynamically register** them from the `CONFORMED_PROPERTIES` registry.

## Benefits of Dynamic Registration

✅ **DRY (Don't Repeat Yourself)** - Define properties once in registry
✅ **Maintainable** - Add new properties without touching DomoStream class
✅ **Consistent** - All properties follow same pattern
✅ **Scalable** - Easy to add 50+ properties if needed
✅ **Discoverable** - Properties still show up in IDE autocomplete

## Comparison: Manual vs Dynamic

### Current Approach (Manual)

```python
# DomoStream class has 12 manually defined properties
@property
def sql(self) -> str | None:
    """Get SQL query..."""
    return self._get_conformed_value("query")

@property
def database(self) -> str | None:
    """Get database name..."""
    return self._get_conformed_value("database")

# ... 10 more properties
```

**Pros:**
- ✅ Explicit and clear
- ✅ Custom docstrings
- ✅ Full control over each property

**Cons:**
- ❌ Repetitive code (12 nearly identical properties)
- ❌ Must edit DomoStream class to add new properties
- ❌ Hard to maintain consistency

### Dynamic Approach

```python
# Define properties once in registry, auto-register on class
from stream_configs._register import register_conformed_properties

@dataclass
class DomoStream(DomoEntity):
    # ... existing fields ...

    def _get_conformed_value(self, name): ...

# Auto-register all properties from CONFORMED_PROPERTIES
register_conformed_properties(DomoStream, CONFORMED_PROPERTIES)
```

**Pros:**
- ✅ No repetitive code
- ✅ Add properties by just updating registry
- ✅ Automatic consistency
- ✅ Less code to maintain

**Cons:**
- ❌ Less explicit (properties defined elsewhere)
- ❌ Generated docstrings (less detailed)
- ❌ Slightly harder to debug

## Implementation Approaches

### Approach 1: Function-Based (Recommended)

**Simple and explicit** - Call after class definition:

```python
# In stream.py
class DomoStream(DomoEntity):
    def _get_conformed_value(self, name):
        ...

# Register at module level
from .stream_configs._register import register_conformed_properties
from .stream_configs._conformed import CONFORMED_PROPERTIES

register_conformed_properties(DomoStream, CONFORMED_PROPERTIES)
```

**Pros:**
- Simple to understand
- Works with dataclasses
- No magic
- Easy to debug

**Cons:**
- Must remember to call registration function
- Happens at import time

### Approach 2: Class Decorator

**Pythonic and declarative**:

```python
from .stream_configs._register import with_conformed_properties

@with_conformed_properties()
@dataclass
class DomoStream(DomoEntity):
    def _get_conformed_value(self, name):
        ...
```

**Pros:**
- Pythonic decorator pattern
- Clear intent (decorator on class)
- Self-contained

**Cons:**
- Decorator order matters (must be before @dataclass)
- Slightly more complex

### Approach 3: Metaclass

**Most powerful** - Controls class creation:

```python
class ConformedPropertyMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if '_conformed_properties' in namespace:
            register_conformed_properties(cls, namespace['_conformed_properties'])
        return cls

@dataclass
class DomoStream(DomoEntity, metaclass=ConformedPropertyMeta):
    _conformed_properties = CONFORMED_PROPERTIES
    ...
```

**Pros:**
- Most flexible
- Can control class creation
- Can add validation

**Cons:**
- Complex (metaclasses are advanced Python)
- Harder to debug
- May conflict with other metaclasses

### Approach 4: Lazy Properties (Descriptors)

**Explicit with caching**:

```python
class LazyConformedProperty:
    def __init__(self, conf_name):
        self.conf_name = conf_name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj._get_conformed_value(self.conf_name)

class DomoStream(DomoEntity):
    sql = LazyConformedProperty("query")
    database = LazyConformedProperty("database")
    # ... explicit for each property
```

**Pros:**
- Explicit property definitions
- Can add caching
- Full control per property

**Cons:**
- Still repetitive (define each property)
- More complex than simple @property

## Recommended Implementation

**Hybrid Approach**: Keep manual properties for most common ones (sql, database, warehouse) and use dynamic registration for less common ones.

```python
@dataclass
class DomoStream(DomoEntity):
    # Manually define key properties with detailed docstrings
    @property
    def sql(self) -> str | None:
        """Get SQL query from stream configuration (cross-platform).

        Works across providers that use SQL queries:
        - Snowflake (all variants)
        - AWS Athena
        - PostgreSQL

        Returns:
            SQL query string or None
        """
        result = self._get_conformed_value("query")
        if result:
            return result
        return self._get_conformed_value("custom_query")

    @property
    def database(self) -> str | None:
        """Get database name (cross-platform)."""
        return self._get_conformed_value("database")

    @property
    def warehouse(self) -> str | None:
        """Get compute warehouse (Snowflake-specific)."""
        return self._get_conformed_value("warehouse")

# Dynamically register less common properties
from .stream_configs._register import register_conformed_properties
from .stream_configs._conformed import CONFORMED_PROPERTIES

_dynamic_props = {k: v for k, v in CONFORMED_PROPERTIES.items()
                  if k not in ["query", "custom_query", "database", "warehouse"]}
register_conformed_properties(DomoStream, _dynamic_props)
```

**Benefits:**
- ✅ Best of both worlds
- ✅ Detailed docs for common properties
- ✅ Automatic registration for long-tail properties
- ✅ Easy to add new properties

## Migration Strategy

### Phase 1: Add Registration Function (Non-Breaking)

Add `_register.py` with registration utilities. Don't use it yet.

### Phase 2: Test with New Properties (Additive)

Use dynamic registration for NEW properties only:

```python
# Manually keep existing 12 properties
# Dynamically add new properties:
CONFORMED_PROPERTIES["role"] = ConformedProperty(...)
register_conformed_properties(DomoStream, {"role": CONFORMED_PROPERTIES["role"]})
```

### Phase 3: Migrate Common Properties (Optional)

If dynamic registration works well, migrate existing properties:

1. Remove manual property definitions
2. Add to dynamic registration
3. Update tests

### Phase 4: Full Dynamic (Future)

Once proven stable, use dynamic registration for all properties.

## Performance Considerations

### Property Creation Time

Dynamic registration happens once at **import time**:

```python
# Import time (one-time cost)
import stream  # registers properties

# Runtime (no overhead)
stream.sql  # Just a normal property access
```

**Impact:** Negligible (< 1ms for 50 properties)

### Runtime Performance

No difference between manual and dynamic properties:

```python
# Manual property
@property
def sql(self): return self._get_conformed_value("query")

# Dynamic property (after registration)
# Internally becomes the same as manual
```

**Impact:** Zero runtime overhead

### Memory Impact

Each property adds ~1KB to the class. For 50 properties:

- Manual: 50 KB
- Dynamic: 50 KB (same)

**Impact:** No memory difference

## Testing Dynamic Registration

```python
def test_dynamic_registration():
    """Test that dynamically registered properties work."""
    from stream_configs._register import register_conformed_properties

    # Create test class
    class TestStream:
        def _get_conformed_value(self, name):
            return f"value_{name}"

    # Register properties
    test_props = {
        "query": ConformedProperty(
            name="query",
            mappings={"test": "sql"},
            description="SQL query"
        )
    }
    register_conformed_properties(TestStream, test_props)

    # Verify property exists
    assert hasattr(TestStream, "sql")

    # Verify property works
    stream = TestStream()
    assert stream.sql == "value_query"
```

## Debugging Tips

### Check What Properties Were Registered

```python
# List all properties on DomoStream
props = [p for p in dir(DomoStream)
         if isinstance(getattr(DomoStream, p), property)]
print(f"Properties: {props}")
```

### Check Property Source

```python
# Check if property was manually defined or dynamically registered
import inspect

sql_prop = getattr(DomoStream, 'sql')
source = inspect.getsource(sql_prop.fget)
print(source)  # Will show "lambda" for dynamic, full code for manual
```

### Verify Registration Happened

```python
# Before import
assert not hasattr(DomoStream, "sql")

# After registration
from stream_configs._register import register_conformed_properties
register_conformed_properties(DomoStream, CONFORMED_PROPERTIES)

assert hasattr(DomoStream, "sql")
```

## Conclusion

**Dynamic property registration is definitely possible** and offers significant benefits for maintainability and scalability.

**Recommendation:**
- Start with hybrid approach (manual for common, dynamic for rest)
- Validate with less common properties first
- Migrate incrementally if successful

**Current Implementation (Manual)** is fine for now with 12 properties, but **dynamic registration** becomes compelling when you have 20+ properties.

## Examples

See working examples in:
- `examples/dynamic_property_registration_example.py` - All 4 approaches
- `stream_configs/_register.py` - Registration utilities

## Decision Matrix

| Criteria | Manual | Dynamic | Hybrid |
|----------|--------|---------|--------|
| **Maintainability** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Readability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Scalability** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Debuggability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Explicitness** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **DRY** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Winner:** Hybrid approach for production code (best balance)
