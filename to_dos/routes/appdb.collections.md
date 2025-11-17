# RouteContext Migration – appdb/collections

## Status
- [ ] PR created
- [ ] All functions migrated (4/4)
- [ ] Tests updated/verified
- [ ] Classes updated to call with context

## Functions to Update

- [✓] `create_collection` (line 47)
- [✓] `get_collections` (line 107)
- [✓] `get_collection_by_id` (line 170)
- [✓] `modify_collection_permissions` (line 231)

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
