"""Generate GitHub issue templates for RouteContext migration.

This script reads the TO_DOS files and generates issue descriptions that can be
used with the GitHub Copilot coding agent.
"""

import json
from pathlib import Path


def generate_route_issue(todo_file: Path) -> dict:
    """Generate issue data for a route module migration."""
    content = todo_file.read_text(encoding="utf-8")
    module_name = todo_file.stem.replace(".", "/")

    # Extract function count
    function_lines = [
        line for line in content.split("\n") if line.strip().startswith("- [ ] `")
    ]
    function_count = len(function_lines)

    title = (
        f"[RouteContext] Migrate routes/{module_name}.py ({function_count} functions)"
    )

    body = f"""## Objective
Migrate `src/domolibrary2/routes/{module_name}.py` to use the RouteContext pattern.

## Reference Implementation
See `src/domolibrary2/routes/appdb/collections.py` for the canonical example.

## Tasks
- [ ] Add `RouteContext` import: `from ...client.context import RouteContext`
- [ ] Update all {function_count} `@gd.route_function` decorated functions to accept `context` parameter
- [ ] Add context normalization inside each function
- [ ] Update `get_data()` calls to use `context=context`
- [ ] Verify all tests pass
- [ ] Update `TO_DOS/routes/{todo_file.name}` to mark functions as complete

## Migration Pattern

Each function should follow this pattern:

```python
@gd.route_function
async def function_name(
    auth: DomoAuth,
    required_param: str,
    *,  # Make following params keyword-only
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    \"\"\"Docstring here.\"\"\"
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{{auth.domo_instance}}.domo.com/api/..."

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        context=context,  # Use context instead of individual params
    )

    if not res.is_success:
        raise SomeError(res=res)

    return res
```

## Functions to Update
{chr(10).join(function_lines)}

## Success Criteria
- All functions accept optional `context` parameter
- All functions normalize context if not provided
- All `get_data()` calls use context
- Existing tests pass without modification
- No breaking changes (legacy parameters still work via decorator)

## Related Files
- TODO: `external/dl-remuxed/TO_DOS/routes/{todo_file.name}`
- Implementation Plan: `external/dl-remuxed/code_review/route-context-implementation-plan.md`
"""

    return {
        "title": title,
        "body": body,
        "labels": ["route-context-migration", "refactor"],
    }


def generate_class_issue(todo_file: Path) -> dict:
    """Generate issue data for a class module migration."""
    content = todo_file.read_text(encoding="utf-8")
    class_name = todo_file.stem.replace(".", "/")

    # Extract method count
    method_lines = [
        line for line in content.split("\n") if line.strip().startswith("- [ ] `")
    ]
    method_count = len(method_lines)

    title = f"[RouteContext] Migrate classes/{class_name}.py ({method_count} methods)"

    body = f"""## Objective
Migrate `src/domolibrary2/classes/{class_name}.py` to use RouteContext via `_build_route_context()`.

## Reference
Class methods should use `self._build_route_context()` to construct context from passed parameters.

## Tasks
- [ ] Update all {method_count} methods that call route functions
- [ ] Replace individual session/debug_api params with context
- [ ] Use `self._build_route_context()` to create context
- [ ] Pass context to route function calls
- [ ] Verify all tests pass
- [ ] Update `TO_DOS/classes/{todo_file.name}` to mark methods as complete

## Migration Pattern

```python
async def method_name(
    self,
    param: str,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    return_raw: bool = False,
) -> ResultType:
    \"\"\"Docstring here.\"\"\"
    context = self._build_route_context(
        session=session,
        debug_api=debug_api,
        # log_level="WARNING",  # Optional per-call override
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

## Methods to Update
{chr(10).join(method_lines)}

## Success Criteria
- All methods use `_build_route_context()`
- Context properly passed to route functions
- Existing tests pass without modification
- Optional: Add test for `log_level` parameter if needed

## Related Files
- TODO: `external/dl-remuxed/TO_DOS/classes/{todo_file.name}`
- Implementation Plan: `external/dl-remuxed/code_review/route-context-implementation-plan.md`
"""

    return {
        "title": title,
        "body": body,
        "labels": ["route-context-migration", "refactor", "classes"],
    }


def main():
    """Generate issue JSON files for all TODOs."""
    repo_root = Path(__file__).parent.parent
    todos_dir = repo_root / "TO_DOS"
    output_dir = repo_root / "scripts" / "issues"
    output_dir.mkdir(exist_ok=True)

    # High-priority routes from implementation plan
    priority_routes = [
        "user.core",
        "dataset.core",
        "dataset.upload",
        "group",
        "page.core",
        "card",
    ]

    # Generate route issues
    routes_dir = todos_dir / "routes"
    route_issues = []

    for todo_file in sorted(routes_dir.glob("*.md")):
        if todo_file.name == "README.md":
            continue

        issue = generate_route_issue(todo_file)

        # Mark as high-priority
        if todo_file.stem in priority_routes:
            issue["labels"].append("priority-high")
            issue["title"] = f"[HIGH] {issue['title']}"

        route_issues.append(issue)

        # Save individual issue file
        output_file = output_dir / f"route-{todo_file.stem}.json"
        output_file.write_text(json.dumps(issue, indent=2), encoding="utf-8")

    # Generate class issues
    classes_dir = todos_dir / "classes"
    class_issues = []

    for todo_file in sorted(classes_dir.glob("*.md")):
        if todo_file.name == "README.md":
            continue

        issue = generate_class_issue(todo_file)
        class_issues.append(issue)

        # Save individual issue file
        output_file = output_dir / f"class-{todo_file.stem}.json"
        output_file.write_text(json.dumps(issue, indent=2), encoding="utf-8")

    # Generate master list
    master = {
        "route_issues": route_issues,
        "class_issues": class_issues,
        "total": len(route_issues) + len(class_issues),
    }

    (output_dir / "all_issues.json").write_text(
        json.dumps(master, indent=2), encoding="utf-8"
    )

    print(f"✓ Generated {len(route_issues)} route issues")
    print(f"✓ Generated {len(class_issues)} class issues")
    print(f"✓ Total: {master['total']} issues")
    print(f"\nIssue files saved to: {output_dir}")
    print("\nTo create issues with GitHub Copilot coding agent:")
    print("1. Use the issue titles and bodies from the JSON files")
    print("2. Tag issues with #github-pull-request_copilot-coding-agent")
    print("3. Copilot will create branches and PRs automatically")


if __name__ == "__main__":
    main()
