# RouteContext Pattern

## Overview

The RouteContext pattern consolidates common debugging and control parameters into a single context object, providing cleaner function signatures and better maintainability.

## Motivation

Before RouteContext, route functions had multiple debug and control parameters:

```python
async def get_card_by_id(
    card_id,
    auth: DomoAuth,
    optional_parts="...",
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    return_raw: bool = False,
):
    # ...
```

This approach had several issues:
- Function signatures became cluttered with many parameters
- Difficult to add new debug/control parameters without breaking changes
- Inconsistent parameter ordering across functions
- Hard to group related parameters

## Solution: RouteContext

The RouteContext class consolidates these parameters:

```python
@dataclass
class RouteContext:
    session: Optional[httpx.AsyncClient] = None
    debug_api: bool = False
    debug_num_stacks_to_drop: int = 1
    parent_class: Optional[str] = None
```

## Usage

### Using RouteContext

```python
from domolibrary2.client.context import RouteContext
from domolibrary2.routes import card

# Create context
context = RouteContext(
    debug_api=True,
    debug_num_stacks_to_drop=2,
    parent_class="MyClass",
)

# Use with route function
result = await card.get_card_by_id(
    card_id="123",
    auth=auth,
    context=context,
)
```

### Backward Compatibility

Legacy code continues to work without changes:

```python
# Old style - still works!
result = await card.get_card_by_id(
    card_id="123",
    auth=auth,
    debug_api=True,
    debug_num_stacks_to_drop=2,
    parent_class="MyClass",
)
```

The function internally normalizes these parameters into a RouteContext.

## Implementation Pattern

### Route Function Structure

```python
@gd.route_function
async def my_route_function(
    auth: DomoAuth,
    required_param: str,
    optional_param: str = "default",
    *,  # Make following params keyword-only
    context: RouteContext | None = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
    return_raw: bool = False,
) -> ResponseGetData:
    """Function description.
    
    Args:
        auth: Authentication object
        required_param: Required parameter
        optional_param: Optional parameter
        context: Optional RouteContext (overrides individual debug params)
        debug_api: Enable API debugging (overridden by context)
        session: HTTP session (overridden by context)
        parent_class: Parent class name (overridden by context)
        debug_num_stacks_to_drop: Stack frames to drop (overridden by context)
        return_raw: Return raw response
        
    Returns:
        ResponseGetData object
    """
    # Normalize context
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )
    
    url = f"https://{auth.domo_instance}.domo.com/api/..."
    
    # Use context in get_data call
    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        context=context,
    )
    
    if not res.is_success:
        raise SomeError(res=res)
    
    return res
```

### Key Implementation Points

1. **Context Parameter Position**: After `*` separator to make it keyword-only
2. **Context Normalization**: Always normalize at the start of the function
3. **Parameter Order**:
   - Required positional parameters
   - Optional parameters with defaults
   - `*` separator
   - `context` parameter
   - Backward compatibility parameters
   - `return_raw` parameter (always last)

4. **Docstring**: Document that context overrides individual parameters

## RouteContext Class Methods

### `to_dict()`

Convert context to dictionary for unpacking:

```python
context = RouteContext(debug_api=True, parent_class="Test")
context_dict = context.to_dict()
# {'session': None, 'debug_api': True, 'debug_num_stacks_to_drop': 1, 'parent_class': 'Test'}
```

### `from_params()`

Create RouteContext from individual parameters:

```python
context = RouteContext.from_params(
    debug_api=True,
    parent_class="Test",
)
```

## Benefits

### Cleaner Signatures

Before:
```python
async def func(auth, param, debug_api, session, parent_class, debug_num_stacks_to_drop, return_raw):
```

After:
```python
async def func(auth, param, *, context=None, debug_api=False, session=None, parent_class=None, debug_num_stacks_to_drop=1, return_raw=False):
```

### Easier Extension

Adding new context parameters:
1. Add to RouteContext class
2. Update normalization logic
3. No changes needed in route function signatures

### Better Grouping

Related parameters are now grouped in a single object, making it clear they belong together.

### Type Safety

RouteContext provides type hints for all its attributes, improving IDE support and type checking.

## Migration Guide

### Migrating a Route Function

1. **Import RouteContext**:
   ```python
   from ..client.context import RouteContext
   ```

2. **Add context parameter** (after `*`):
   ```python
   async def my_function(
       auth: DomoAuth,
       required_param: str,
       *,
       context: RouteContext | None = None,
       debug_api: bool = False,
       # ... other params
   ):
   ```

3. **Add context normalization**:
   ```python
   if context is None:
       context = RouteContext(
           session=session,
           debug_api=debug_api,
           debug_num_stacks_to_drop=debug_num_stacks_to_drop,
           parent_class=parent_class,
       )
   ```

4. **Update get_data/looper calls**:
   ```python
   res = await gd.get_data(
       auth=auth,
       url=url,
       context=context,  # Use context instead of individual params
   )
   ```

5. **Update docstring** to document context parameter and overriding behavior

## Testing

### Test with Context

```python
@pytest.mark.asyncio
async def test_function_with_context(mock_auth):
    context = RouteContext(
        debug_api=True,
        parent_class="TestClass",
    )
    
    result = await my_function(
        auth=mock_auth,
        param="value",
        context=context,
    )
    
    assert result is not None
```

### Test Backward Compatibility

```python
@pytest.mark.asyncio
async def test_function_without_context(mock_auth):
    result = await my_function(
        auth=mock_auth,
        param="value",
        debug_api=True,
        parent_class="TestClass",
    )
    
    assert result is not None
```

## Example: routes/card.py

See `src/domolibrary2/routes/card.py` for a complete example of RouteContext migration:

- All 4 functions migrated
- Full backward compatibility maintained
- Comprehensive test coverage in `tests/routes/test_card_route_context.py`

## Future Enhancements

Potential additions to RouteContext:
- `timeout: int` - Request timeout
- `retry_config: RetryConfig` - Retry configuration
- `tracing_context: TracingContext` - Distributed tracing
- `rate_limit_config: RateLimitConfig` - Rate limiting

These can be added without changing existing function signatures.
