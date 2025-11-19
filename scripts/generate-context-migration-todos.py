"""Generate TODO files for RouteContext migration.

This script scans routes and classes to identify functions/methods that need
to be updated to use the new RouteContext pattern.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set


class RouteAnalyzer(ast.NodeVisitor):
    """Analyze route functions for context migration needs."""

    def __init__(self):
        self.functions: list[Dict] = []
        self.has_route_decorator = False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Check for @gd.route_function or similar decorators
        has_decorator = any(
            (
                isinstance(d, ast.Attribute)
                and isinstance(d.value, ast.Name)
                and d.value.id == "gd"
            )
            or (isinstance(d, ast.Name))
            for d in node.decorator_list
        )

        # Extract parameter names
        params = {arg.arg for arg in node.args.args + node.args.kwonlyargs}

        # Check if already migrated (has context param)
        has_context = "context" in params

        # Check for legacy params
        has_legacy = any(
            p in params
            for p in [
                "session",
                "debug_api",
                "debug_num_stacks_to_drop",
                "parent_class",
            ]
        )

        # Check for get_data calls in body
        has_get_data_call = self._has_get_data_call(node)

        if (has_decorator or has_get_data_call) and has_legacy:
            self.functions.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "has_context": has_context,
                    "has_legacy": has_legacy,
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "params": list(params),
                }
            )

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def _has_get_data_call(self, node: ast.FunctionDef) -> bool:
        """Check if function body contains gd.get_data calls."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if (
                        isinstance(child.func.value, ast.Name)
                        and child.func.value.id == "gd"
                        and child.func.attr in ["get_data", "get_data_stream", "looper"]
                    ):
                        return True
        return False


class ClassAnalyzer(ast.NodeVisitor):
    """Analyze class methods for context migration needs."""

    def __init__(self):
        self.methods: list[Dict] = []
        self.current_class = None

    def visit_ClassDef(self, node: ast.ClassDef):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.current_class and node.name not in ["__init__", "__post_init__"]:
            # Extract parameter names
            params = {arg.arg for arg in node.args.args + node.args.kwonlyargs}

            # Check for route calls or direct get_data usage
            has_route_call = self._has_route_or_getdata_call(node)

            # Check for legacy params being passed
            has_legacy = any(
                p in params
                for p in [
                    "session",
                    "debug_api",
                    "debug_num_stacks_to_drop",
                    "parent_class",
                ]
            )

            if has_route_call and has_legacy:
                self.methods.append(
                    {
                        "class_name": self.current_class,
                        "method_name": node.name,
                        "line": node.lineno,
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                        "params": list(params),
                    }
                )

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def _has_route_or_getdata_call(self, node: ast.FunctionDef) -> bool:
        """Check if method calls route functions or gd.get_data."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                # Check for gd.get_data
                if isinstance(child.func, ast.Attribute):
                    if (
                        isinstance(child.func.value, ast.Name)
                        and child.func.value.id == "gd"
                        and child.func.attr in ["get_data", "get_data_stream", "looper"]
                    ):
                        return True

                # Check for route module calls (e.g., user_routes.get_user)
                if isinstance(child.func, ast.Attribute):
                    if isinstance(child.func.value, ast.Name):
                        if (
                            "_routes" in child.func.value.id
                            or "routes." in child.func.value.id
                        ):
                            return True

                # Check for direct route calls (await module.function)
                if isinstance(child.func, ast.Attribute):
                    # Common route call patterns
                    return True
        return False


def analyze_route_file(file_path: Path) -> Dict:
    """Analyze a route file for context migration needs."""
    try:
        with open(file_path, encoding="utf-8") as f:
            tree = ast.parse(f.read())

        analyzer = RouteAnalyzer()
        analyzer.visit(tree)

        return {
            "path": file_path,
            "functions": analyzer.functions,
            "total": len(analyzer.functions),
            "migrated": sum(1 for f in analyzer.functions if f["has_context"]),
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {
            "path": file_path,
            "functions": [],
            "total": 0,
            "migrated": 0,
            "error": str(e),
        }


def analyze_class_file(file_path: Path) -> Dict:
    """Analyze a class file for context migration needs."""
    try:
        with open(file_path, encoding="utf-8") as f:
            tree = ast.parse(f.read())

        analyzer = ClassAnalyzer()
        analyzer.visit(tree)

        return {
            "path": file_path,
            "methods": analyzer.methods,
            "total": len(analyzer.methods),
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {"path": file_path, "methods": [], "total": 0, "error": str(e)}


def generate_route_todo(analysis: Dict, output_path: Path, routes_dir: Path):
    """Generate TODO markdown for a route module."""
    rel_path = analysis["path"].relative_to(routes_dir)
    module_name = str(rel_path).replace("\\", "/").replace(".py", "")

    content = f"""# RouteContext Migration – {module_name}

## Status
- [ ] PR created
- [ ] All functions migrated ({analysis['migrated']}/{analysis['total']})
- [ ] Tests updated/verified
- [ ] Classes updated to call with context

## Functions to Update

"""

    if not analysis["functions"]:
        content += "_No functions need migration (already done or not applicable)._\n\n"
    else:
        for func in analysis["functions"]:
            status = "✓" if func["has_context"] else " "
            content += f"- [{status}] `{func['name']}` (line {func['line']})\n"
            if not func["has_context"]:
                content += (
                    f"  - Add `context: RouteContext | None = None` (keyword-only)\n"
                )
                content += f"  - Normalize context inside function\n"
                content += f"  - Call `get_data(..., context=context)`\n"

    content += """
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
"""

    output_path.write_text(content, encoding="utf-8")


def generate_class_todo(analysis: Dict, output_path: Path, classes_dir: Path):
    """Generate TODO markdown for a class module."""
    rel_path = analysis["path"].relative_to(classes_dir)
    module_name = str(rel_path).replace("\\", "/").replace(".py", "")

    content = f"""# RouteContext Migration – {module_name}

## Status
- [ ] PR created
- [ ] All methods migrated (0/{analysis['total']})
- [ ] Tests updated/verified

## Methods to Update

"""

    if not analysis["methods"]:
        content += "_No methods need migration (already done or not applicable)._\n\n"
    else:
        for method in analysis["methods"]:
            content += f"- [ ] `{method['class_name']}.{method['method_name']}` (line {method['line']})\n"
            content += f"  - Use `self._build_route_context(...)` to create context\n"
            content += f"  - Pass `context` to route functions\n"
            content += f"  - Remove manual `session`/`debug_api` pass-through\n"

    content += """
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
"""

    output_path.write_text(content, encoding="utf-8")


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    routes_dir = repo_root / "src" / "domolibrary2" / "routes"
    classes_dir = repo_root / "src" / "domolibrary2" / "classes"
    todos_dir = repo_root / "to_dos"

    # Create output directories
    (todos_dir / "routes").mkdir(parents=True, exist_ok=True)
    (todos_dir / "classes").mkdir(parents=True, exist_ok=True)

    # Analyze routes
    print("Analyzing routes...")
    route_files = list(routes_dir.rglob("*.py"))
    route_analyses = []

    for route_file in route_files:
        if "__pycache__" in str(route_file) or route_file.name in [
            "__init__.py",
            "exceptions.py",
        ]:
            continue

        analysis = analyze_route_file(route_file)
        if analysis["total"] > 0 or "error" in analysis:
            route_analyses.append(analysis)

            # Generate TODO file
            rel_path = route_file.relative_to(routes_dir)
            output_name = (
                str(rel_path).replace("\\", ".").replace("/", ".").replace(".py", ".md")
            )
            output_path = todos_dir / "routes" / output_name

            generate_route_todo(analysis, output_path, routes_dir)
            print(f"  Generated: {output_path.name} ({analysis['total']} functions)")

    # Analyze classes
    print("\nAnalyzing classes...")
    class_files = list(classes_dir.rglob("*.py"))
    class_analyses = []

    for class_file in class_files:
        if "__pycache__" in str(class_file) or class_file.name in ["__init__.py"]:
            continue

        analysis = analyze_class_file(class_file)
        if analysis["total"] > 0 or "error" in analysis:
            class_analyses.append(analysis)

            # Generate TODO file
            rel_path = class_file.relative_to(classes_dir)
            output_name = (
                str(rel_path).replace("\\", ".").replace("/", ".").replace(".py", ".md")
            )
            output_path = todos_dir / "classes" / output_name

            generate_class_todo(analysis, output_path, classes_dir)
            print(f"  Generated: {output_path.name} ({analysis['total']} methods)")

    # Generate index
    print("\nGenerating index...")
    index_content = f"""# RouteContext Migration Progress

Last updated: {Path(__file__).stat().st_mtime}

## Summary

- **Routes**: {len(route_analyses)} modules, {sum(a['total'] for a in route_analyses)} functions
  - Migrated: {sum(a['migrated'] for a in route_analyses)}
  - Remaining: {sum(a['total'] - a['migrated'] for a in route_analyses)}
- **Classes**: {len(class_analyses)} modules, {sum(a['total'] for a in class_analyses)} methods

## Routes

"""

    for analysis in sorted(route_analyses, key=lambda a: str(a["path"])):
        rel_path = analysis["path"].relative_to(routes_dir)
        module_name = str(rel_path).replace("\\", "/")
        status = "✓" if analysis["migrated"] == analysis["total"] else " "
        index_content += f"- [{status}] `{module_name}` – {analysis['migrated']}/{analysis['total']} functions\n"

    index_content += "\n## Classes\n\n"

    for analysis in sorted(class_analyses, key=lambda a: str(a["path"])):
        rel_path = analysis["path"].relative_to(classes_dir)
        module_name = str(rel_path).replace("\\", "/")
        index_content += f"- [ ] `{module_name}` – {analysis['total']} methods\n"

    index_content += """
## Migration Order

Suggested order (high-traffic routes first):

1. `user/core.py` – User management routes
2. `dataset/*.py` – Dataset routes
3. `group.py` – Group management
4. `page/*.py` – Page routes
5. `card.py` – Card routes
6. Other modules as needed

For classes, start with:

1. `DomoUser.py`
2. `DomoDataset.py`
3. `DomoGroup.py`
4. Other entities as needed
"""

    (todos_dir / "index.md").write_text(index_content, encoding="utf-8")
    print(f"\nGenerated: {todos_dir / 'index.md'}")

    print(
        f"\n✓ Done! Generated {len(route_analyses) + len(class_analyses)} TODO files."
    )


if __name__ == "__main__":
    main()
