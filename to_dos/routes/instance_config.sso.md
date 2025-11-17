# RouteContext Migration – instance_config/sso

## Status
- [ ] PR created
- [ ] All functions migrated (0/13)
- [ ] Tests updated/verified
- [ ] Classes updated to call with context

## Functions to Update

- [ ] `toggle_user_direct_signon_access` (line 58)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_sso_oidc_config` (line 92)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `_update_sso_oidc_temp_config` (line 167)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `_update_sso_oidc_standard_config` (line 196)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `update_sso_oidc_config` (line 232)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_sso_saml_config` (line 265)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `get_sso_saml_certificate` (line 293)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `_update_sso_saml_temp_config` (line 373)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `_update_sso_saml_standard_config` (line 402)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `update_sso_saml_config` (line 436)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `toggle_sso_skip_to_idp` (line 469)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `toggle_sso_custom_attributes` (line 498)
  - Add `context: RouteContext | None = None` (keyword-only)
  - Normalize context inside function
  - Call `get_data(..., context=context)`
- [ ] `set_sso_certificate` (line 530)
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
