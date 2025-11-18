# RouteContext Migration TODO Tracker

This folder contains automatically generated TODO files for the RouteContext migration effort.

## What This Is

The domolibrary2 codebase is migrating from individual `session`, `debug_num_stacks_to_drop`, and `parent_class` parameters to a unified `RouteContext` object. This migration:

- **Reduces signature bloat** across ~287 route functions and ~325 class methods
- **Enables per-call log level control** via `context.log_level`
- **Centralizes context construction** through `DomoEntity._build_route_context()`
- **Maintains backward compatibility** during the transition

## Structure

```
to_dos/
├── README.md           # This file
├── index.md           # Master progress tracker with full module list
├── routes/            # One TODO file per route module
│   ├── user.core.md
│   ├── dataset.core.md
│   ├── appdb.collections.md  # ✅ Completed (reference implementation)
│   └── ...
└── classes/           # One TODO file per class module
    ├── DomoUser.md
    ├── DomoDataset.core.md
    └── ...
```

## How to Use

### 1. Check Progress

Open `index.md` to see:
- Overall migration status (functions/methods migrated)
- Module-by-module checklist
- Suggested migration order

### 2. Pick a Module

Choose a module from the suggested order in `index.md` or based on your current work.

### 3. Open TODO File

Navigate to the relevant TODO file:
- Routes: `to_dos/routes/{module-path}.md`
- Classes: `to_dos/classes/{ClassName}.md`

Each TODO file contains:
- Migration status checklist
- Function/method list with line numbers
- Migration pattern template
- Reference to canonical implementation

### 4. Create Branch & Implement

Follow the one-PR-per-module workflow:

```powershell
# Create branch
git checkout -b feature/context-routes-user-core

# Make changes (see TODO file for pattern)
# ...

# Run tests
pytest tests/routes/test_user.py -v

# Commit and push
git add .
git commit -m "Add RouteContext to routes.user.core"
git push origin feature/context-routes-user-core
```

### 5. Update TODO & Create PR

- Mark completed functions/methods in the TODO file
- Create PR with link to TODO file in description
- Use TODO checklist as PR acceptance criteria

## Migration Patterns

### Routes

```python
@gd.route_function
async def function_name(
    auth: DomoAuth,
    param: str,
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

### Classes

```python
async def method_name(
    self,
    param: str,
    session: httpx.AsyncClient | None = None,
    return_raw: bool = False,
) -> ResultType:
    context = self._build_route_context(
        session=session,
        # log_level="WARNING",  # optional per-call override
    )

    res = await route_module.route_function(
        auth=self.auth,
        param=param,
        context=context,
        return_raw=return_raw,
    )
```

## Reference Implementation

**See**: `src/domolibrary2/routes/appdb/collections.py`

All 4 functions demonstrate the complete pattern. Use this as your template.

## Regenerating TODOs

To update progress or regenerate TODO files after code changes:

```powershell
python scripts\generate-context-migration-todos.py
```

This will:
- Re-scan all routes and classes
- Update completion status in TODO files
- Regenerate `index.md` with current metrics

## Implementation Plan

For full details on strategy, phases, and timeline, see:
`code_review/route-context-implementation-plan.md`

## Questions?

- **How do I test my changes?** See "Testing Strategy" in the implementation plan
- **What order should I migrate?** See "Migration Order" in `index.md`
- **How do I handle edge cases?** Reference `appdb/collections.py` or ask in PR
