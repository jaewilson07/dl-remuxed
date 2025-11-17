# RouteContext Migration – DomoInstanceConfig/allowlist

## Status
- [ ] PR created
- [ ] All methods migrated (0/6)
- [ ] Tests updated/verified

## Methods to Update

- [ ] `DomoAllowlist.get` (line 69)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoAllowlist.set` (line 96)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoAllowlist.add_ips` (line 138)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoAllowlist.remove_ips` (line 166)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoAllowlist.get_is_filter_all_traffic_enabled` (line 194)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoAllowlist.toggle_is_filter_all_traffic_enabled` (line 219)
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
