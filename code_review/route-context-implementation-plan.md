> Last updated: 2025-11-17

# RouteContext Implementation Plan

## Overview

This document defines the implementation strategy for migrating all routes and classes to use the new `RouteContext` pattern. The migration centralizes transport/debug/logging metadata in a single object, enables per-call log level control, and reduces signature bloat across ~287 route functions and ~325 class methods.

## Goals

1. **Eliminate parameter duplication**: Replace repeated `session`, `debug_api`, `debug_num_stacks_to_drop`, `parent_class` parameters with a single `context` object.
2. **Enable per-call log level control**: Add `log_level` field to `RouteContext` so class methods can quiet noisy logs on a case-by-case basis.
3. **Centralize context construction**: Use `DomoEntity._build_route_context()` so classes maintain default settings and can override per-call.
4. **Maintain backward compatibility**: Keep legacy parameters during transition to avoid breaking existing code.

## Current Status

### Completed
- ✅ `RouteContext` dataclass created (`src/domolibrary2/client/context.py`)
- ✅ `get_data` and `get_data_stream` accept optional `context` parameter
- ✅ `route_function` decorator updated to support `context`
- ✅ `looper` accepts and propagates `context`
- ✅ `DomoEntity._build_route_context()` helper method added
- ✅ `DomoEntity._default_route_context` field added
- ✅ **Pilot implementation**: `routes/appdb/collections.py` (4/4 functions migrated)

### Remaining
- 🔲 283 route functions across 54 modules
- 🔲 325 class methods across 55 modules
- 🔲 Logging integration (wire `context.log_level` into logger)
- 🔲 Test coverage for context pattern
- 🔲 Documentation updates

## Migration Scope

### Routes Summary
- **Total modules**: 55
- **Total functions**: 287
- **Migrated**: 4 (appdb/collections.py)
- **Remaining**: 283

### Classes Summary
- **Total modules**: 55
- **Total methods**: 325
- **Migrated**: 0
- **Remaining**: 325

## Implementation Strategy

### Phase 1: High-Traffic Routes (Priority)

Migrate the most frequently used route modules first to maximize benefit:

1. **`user/core.py`** (10 functions) – User management
2. **`dataset/core.py`** (6 functions) – Dataset retrieval
3. **`dataset/upload.py`** (7 functions) – Dataset data operations
4. **`group.py`** (13 functions) – Group management
5. **`page/core.py`** (3 functions) – Page operations
6. **`card.py`** (4 functions) – Card operations

### Phase 2: Entity Classes (High Value)

Migrate core entity classes to enable `log_level` control:

1. **`DomoUser.py`** (19 methods)
2. **`DomoDataset/dataset_default.py`** (4 methods)
3. **`DomoDataset/dataset_data.py`** (6 methods)
4. **`DomoGroup/core.py`** (9 methods)
5. **`DomoPage/core.py`** (5 methods)
6. **`DomoCard/card_default.py`** (6 methods)

### Phase 3: Remaining Routes

Complete migration of all route modules in logical groups:

- **Authentication & Config**: auth, instance_config/*
- **Data Operations**: dataflow, stream, filesets
- **Advanced Features**: publish, workflows, jupyter/*
- **Infrastructure**: application, appstudio, sandbox

### Phase 4: Remaining Classes

Complete migration of all class modules:

- **Managers & Collections**: DomoUsers, DomoDatasets, DomoGroups
- **Subentities**: tags, lineage, schedule
- **Complex Entities**: DomoJupyter/*, DomoAccount/*, DomoInstanceConfig/*
- **Specialized**: DomoEverywhere, DomoCodeEngine

## Per-Module Workflow

Each module follows this process (one PR per module):

### For Route Modules

1. **Create branch**: `feature/context-routes-{module-path}`
2. **Update functions**:
   ```python
   @gd.route_function
   async def function_name(
       auth: DomoAuth,
       domain_param: str,
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
3. **Update tests**: Add test cases for both legacy and context patterns
4. **Update TODO**: Mark functions in `to_dos/routes/{module}.md` as complete
5. **Open PR**: Link to TODO file in description

### For Class Modules

1. **Create branch**: `feature/context-classes-{ClassName}`
2. **Update methods**:
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
3. **Update tests**: Verify existing tests pass, add log_level test if needed
4. **Update TODO**: Mark methods in `to_dos/classes/{Class}.md` as complete
5. **Open PR**: Link to TODO file in description

## TODO File Organization

All migration TODO files are stored under `to_dos/`:

```
to_dos/
├── index.md                    # Master progress tracker
├── routes/
│   ├── user.core.md           # User route functions
│   ├── dataset.core.md        # Dataset route functions
│   ├── appdb.collections.md   # ✅ Completed pilot
│   └── ...                    # 54 more route modules
└── classes/
    ├── DomoUser.md            # DomoUser methods
    ├── DomoDataset.core.md    # DomoDataset methods
    └── ...                    # 54 more class modules
```

Each TODO file contains:
- Migration status checklist
- Function/method list with line numbers
- Migration pattern example
- Reference to canonical implementation

## Testing Strategy

### Route Tests

For each migrated route module:

1. **Legacy compatibility test**: Call functions with old parameters
   ```python
   res = await route_fn(
       auth=auth,
       param=value,
       session=session,
       debug_api=True,
   )
   ```

2. **Context pattern test**: Call functions with RouteContext
   ```python
   context = RouteContext(session=session, debug_api=True)
   res = await route_fn(
       auth=auth,
       param=value,
       context=context,
   )
   ```

3. **Verify equivalence**: Both patterns should produce identical results

### Class Tests

For each migrated class module:

1. **Existing tests**: Ensure all existing tests still pass
2. **Context usage test**: Verify `_build_route_context` is called
3. **Log level test** (optional): Test that `log_level` parameter works
   ```python
   # Should produce less noisy logs
   result = await entity.method(
       param=value,
       log_level="WARNING",
   )
   ```

## Logging Integration

Wire `RouteContext.log_level` into the logging pipeline:

### Option 1: Via additional_information (Current)

In `get_data`:
```python
if context.log_level:
    additional_information["log_level"] = context.log_level
```

Update `ResponseGetDataProcessor` to honor this field.

### Option 2: Via log_call decorator

If `log_call` supports dynamic log levels, pass `context.log_level` directly.

### Implementation

1. Choose integration approach (likely Option 1)
2. Update `get_data` to set `additional_information["log_level"]`
3. Update logging processor to check and apply `log_level`
4. Add test to verify log suppression works

## Deprecation Strategy

After full migration (estimated: 3-6 months):

### Minor Version (e.g., 2.x.0)

- ✅ Keep both context and legacy parameters
- ✅ No warnings or breaking changes
- ✅ Document context as preferred pattern

### Next Minor Version (e.g., 2.y.0)

- Add `PendingDeprecationWarning` when legacy params used without context
- Update docstrings to mark legacy params as deprecated
- Recommend context pattern in all examples

### Major Version (e.g., 3.0.0)

- Remove legacy parameters from route function signatures
- Signatures become: `fn(auth, domain_params, *, context=None, return_raw=False)`
- Breaking change: external code must update to use context

## Progress Tracking

### Metrics

Track progress via `to_dos/index.md`:
- Routes migrated: X/55 modules, Y/287 functions
- Classes migrated: X/55 modules, Y/325 methods

### Automation

Use `scripts/generate-context-migration-todos.py` to:
- Re-scan codebase for progress
- Update TODO files with completion status
- Regenerate index with current metrics

Run periodically:
```powershell
python scripts\generate-context-migration-todos.py
```

## Reference Implementation

**Canonical route example**: `src/domolibrary2/routes/appdb/collections.py`

All 4 functions demonstrate the complete pattern:
- Optional `context` parameter
- Context normalization
- Legacy compatibility
- Clean `get_data` delegation

## Next Steps

1. **Immediate**: Migrate `user/core.py` (10 functions)
2. **Week 1**: Complete high-traffic routes (Phase 1)
3. **Week 2**: Migrate core entity classes (Phase 2)
4. **Weeks 3-6**: Systematic migration of remaining modules
5. **Week 7+**: Logging integration, documentation, deprecation plan

## Questions / Considerations

- **Batch size**: Should we batch multiple small modules into single PRs?
  - Recommendation: Keep one module per PR for clarity
- **Test coverage**: Should we require new tests for every migrated module?
  - Recommendation: Require at least one context test per module
- **Log level values**: Should we standardize allowed log levels?
  - Recommendation: Use standard Python log levels ("DEBUG", "INFO", "WARNING", "ERROR")

## Appendix: Key Files

- `src/domolibrary2/client/context.py` – RouteContext definition
- `src/domolibrary2/client/get_data.py` – Client layer with context support
- `src/domolibrary2/base/entities.py` – DomoEntity with _build_route_context
- `src/domolibrary2/routes/appdb/collections.py` – Reference implementation
- `scripts/generate-context-migration-todos.py` – TODO generation script
- `to_dos/index.md` – Master progress tracker
