# RouteContext Migration – instance_config/toggle

## Status
- [ ] PR created
- [ ] All functions migrated (0/10)
- [ ] Tests updated/verified
- [ ] Classes updated to call with context

## Functions to Update

- [ ] `get_is_invite_social_users_enabled` (line 33)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `toggle_is_invite_social_users_enabled` (line 71)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_is_user_invite_notifications_enabled` (line 127)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `toggle_is_user_invite_enabled` (line 166)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_is_weekly_digest_enabled` (line 210)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `toggle_is_weekly_digest_enabled` (line 248)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_is_left_nav_enabled_v1` (line 288)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_is_left_nav_enabled` (line 327)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `toggle_is_left_nav_enabled_v1` (line 366)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `toggle_is_left_nav_enabled` (line 409)
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
