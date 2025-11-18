# RouteContext Migration – subentity/tags

## Status
- [ ] PR created
- [ ] All methods migrated (0/4)
- [ ] Tests updated/verified

## Methods to Update

- [ ] `DomoTags.get` (line 29)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoTags.update` (line 48)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoTags.add` (line 67)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoTags.remove` (line 86)
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
