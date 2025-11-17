# RouteContext Migration – instance_config/user_attributes

## Status
- [ ] PR created
- [ ] All functions migrated (0/5)
- [ ] Tests updated/verified
- [ ] Classes updated to call with context

## Functions to Update

- [ ] `get_user_attributes` (line 113)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_user_attribute_by_id` (line 180)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `create_user_attribute` (line 237)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `update_user_attribute` (line 322)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `delete_user_attribute` (line 418)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`

## Migration Pattern

```python
@gd.route_function
async def function_name(
    auth: DomoAuth,
    required_param: str,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        context=context,
    )
```

## Reference
See `src/domolibrary2/routes/appdb/collections.py` for canonical example.
