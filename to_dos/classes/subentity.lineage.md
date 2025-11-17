# RouteContext Migration – subentity/lineage

## Status
- [ ] PR created
- [ ] All methods migrated (0/11)
- [ ] Tests updated/verified

## Methods to Update

- [ ] `DomoLineageLink_Dataflow.get_entity` (line 102)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineageLink_Publication.get_entity` (line 134)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineageLink_Card.get_entity` (line 168)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineageLink_Dataset.get_entity` (line 205)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineage.get_parent` (line 285)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineage.get_datacenter_lineage` (line 309)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineage.get_federated_lineage` (line 356)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineage.get` (line 418)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineage_Page.get_cards` (line 485)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineage_Page.get` (line 505)
  - Use `self._build_route_context(...)` to create context
  - Pass `context` to route functions
  - Remove manual `session`/`debug_api` pass-through
- [ ] `DomoLineage_Publication.get` (line 554)
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
