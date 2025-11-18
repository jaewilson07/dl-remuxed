# RouteContext Migration – DomoJupyter/DataSource

## Status
- [ ] PR created
- [ ] All methods migrated (0/4)
- [ ] Tests updated/verified

## Methods to Update

- [ ] `DomoJupyter_DataSource.get_dataset` (line 36)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoJupyter_DataSource.from_dict` (line 60)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoJupyter_DataSource.share_with_workspace_as_input_datasource` (line 86)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoJupyter_DataSource.share_with_workspace_as_output_datasource` (line 100)
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
