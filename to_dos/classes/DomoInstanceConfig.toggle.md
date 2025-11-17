# RouteContext Migration – DomoInstanceConfig/toggle

## Status
- [ ] PR created
- [ ] All methods migrated (0/9)
- [ ] Tests updated/verified

## Methods to Update

- [ ] `DomoToggle.get_is_invite_social_users_enabled` (line 105)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.toggle_is_invite_social_users_enabled` (line 147)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.get_is_user_invite_notifications_enabled` (line 212)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.toggle_is_user_invite_notifications_enabled` (line 245)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.get_is_weekly_digest_enabled` (line 301)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.toggle_is_weekly_digest_enabled` (line 330)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.get_is_left_nav_enabled` (line 382)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.toggle_is_left_nav_enabled` (line 411)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoToggle.get_all` (line 465)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through

## Migration Pattern

```python
async def method_name(
    self,
    param: str,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    return_raw: bool = False,
) -> ResultType:
    context = self._build_route_context(
        session=session,
        debug_api=debug_api,
        # log_level="WARNING",  # optional per-call override
    )

    res = await route_module.route_function(
        auth=self.auth,
        param=param,
        context=context,
        return_raw=return_raw,
    )

    if return_raw:
        return res

    return self.from_dict(auth=self.auth, obj=res.response)
```

## Reference
`DomoEntity._build_route_context` is available on all entity classes.
