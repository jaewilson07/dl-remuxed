#!/usr/bin/env python3
"""
Analyze @patch_to usage and generate refactoring plan
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class PatchToAnalyzer(ast.NodeVisitor):
    """Analyze @patch_to usage in Python files"""

    def __init__(self, filename: str):
        self.filename = filename
        self.classes = {}  # class_name -> line number
        self.patch_methods = []  # list of method info
        self.imports_patch_to = False

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if "patch_to" in alias.name:
                self.imports_patch_to = True

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module and "nbdev" in node.module and node.names:
            for alias in node.names:
                if alias.name == "patch_to":
                    self.imports_patch_to = True

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes[node.name] = node.lineno
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.check_patch_to_decorator(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.check_patch_to_decorator(node, is_async=True)
        self.generic_visit(node)

    def check_patch_to_decorator(self, node, is_async=False):
        """Check if function has @patch_to decorator"""
        for decorator in node.decorator_list:
            if self.is_patch_to_decorator(decorator):
                target_class, is_classmethod = self.parse_patch_to_decorator(decorator)

                method_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "target_class": target_class,
                    "is_async": is_async,
                    "is_classmethod": is_classmethod,
                    "docstring": ast.get_docstring(node),
                    "file": self.filename,
                }
                self.patch_methods.append(method_info)

    def is_patch_to_decorator(self, decorator):
        """Check if decorator is @patch_to"""
        if isinstance(decorator, ast.Name):
            return decorator.id == "patch_to"
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id == "patch_to"
        return False

    def parse_patch_to_decorator(self, decorator):
        """Parse @patch_to(Class) or @patch_to(Class, cls_method=True)"""
        target_class = None
        is_classmethod = False

        if isinstance(decorator, ast.Call):
            # Get target class
            if decorator.args:
                if isinstance(decorator.args[0], ast.Name):
                    target_class = decorator.args[0].id
                elif isinstance(decorator.args[0], ast.Attribute):
                    # Handle cases like dmee.DomoEnum
                    target_class = (
                        f"{decorator.args[0].value.id}.{decorator.args[0].attr}"
                    )

            # Check for cls_method=True
            for keyword in decorator.keywords:
                if keyword.arg == "cls_method" and isinstance(
                    keyword.value, ast.Constant
                ):
                    is_classmethod = keyword.value.value

        return target_class, is_classmethod


def analyze_file(file_path: Path) -> PatchToAnalyzer:
    """Analyze a single Python file for @patch_to usage"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        analyzer = PatchToAnalyzer(str(file_path))
        analyzer.visit(tree)
        return analyzer
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return PatchToAnalyzer(str(file_path))


def generate_refactoring_plan(src_dir: Path) -> Dict:
    """Generate comprehensive refactoring plan"""

    # Priority order for processing
    directories = ["client", "classes", "utils", "integrations"]

    plan = {
        "summary": {},
        "files": {},
        "by_directory": defaultdict(list),
        "by_class": defaultdict(list),
    }

    total_files = 0
    total_methods = 0
    files_with_patches = 0

    for directory in directories:
        dir_path = src_dir / directory
        if not dir_path.exists():
            continue

        python_files = list(dir_path.glob("**/*.py"))
        python_files = [f for f in python_files if not f.name.startswith("__")]

        for file_path in python_files:
            total_files += 1
            analyzer = analyze_file(file_path)

            if analyzer.patch_methods or analyzer.imports_patch_to:
                files_with_patches += 1
                rel_path = str(file_path.relative_to(src_dir))

                plan["files"][rel_path] = {
                    "classes": analyzer.classes,
                    "patch_methods": analyzer.patch_methods,
                    "imports_patch_to": analyzer.imports_patch_to,
                    "method_count": len(analyzer.patch_methods),
                }

                plan["by_directory"][directory].append(rel_path)
                total_methods += len(analyzer.patch_methods)

                # Group by target class
                for method in analyzer.patch_methods:
                    plan["by_class"][method["target_class"]].append(
                        {
                            "file": rel_path,
                            "method": method["name"],
                            "line": method["line"],
                            "is_async": method["is_async"],
                            "is_classmethod": method["is_classmethod"],
                        }
                    )

    plan["summary"] = {
        "total_files": total_files,
        "files_with_patches": files_with_patches,
        "total_patch_methods": total_methods,
        "affected_classes": len(plan["by_class"]),
        "directories": list(plan["by_directory"].keys()),
    }

    return plan


def create_refactoring_guide(plan: Dict, output_file: str):
    """Create detailed refactoring implementation guide"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# @patch_to Refactoring Implementation Guide\n\n")

        # Summary
        summary = plan["summary"]
        f.write("## Summary\n\n")
        f.write(f"- **Files to refactor:** {summary['files_with_patches']}\n")
        f.write(f"- **Total @patch_to methods:** {summary['total_patch_methods']}\n")
        f.write(f"- **Affected classes:** {summary['affected_classes']}\n")
        f.write(f"- **Directories:** {', '.join(summary['directories'])}\n\n")

        # Implementation order
        f.write("## Implementation Order\n\n")
        f.write("Process directories in this order for minimal dependencies:\n")
        for i, directory in enumerate(
            ["client", "classes", "utils", "integrations"], 1
        ):
            if directory in plan["by_directory"]:
                file_count = len(plan["by_directory"][directory])
                f.write(f"{i}. **{directory}/**: {file_count} files\n")
        f.write("\n")

        # Directory-by-directory breakdown
        for directory in ["client", "classes", "utils", "integrations"]:
            if directory not in plan["by_directory"]:
                continue

            f.write(f"## {directory.title()} Directory\n\n")

            files_in_dir = plan["by_directory"][directory]

            for file_path in sorted(files_in_dir):
                file_info = plan["files"][file_path]
                f.write(f"### {Path(file_path).name}\n\n")
                f.write(f"**File:** `{file_path}`\n\n")

                if file_info["classes"]:
                    f.write("**Classes in file:**\n")
                    for class_name, line in file_info["classes"].items():
                        f.write(f"- `{class_name}` (line {line})\n")
                    f.write("\n")

                if file_info["patch_methods"]:
                    f.write("**Methods to move into classes:**\n")

                    # Group methods by target class
                    methods_by_class = defaultdict(list)
                    for method in file_info["patch_methods"]:
                        methods_by_class[method["target_class"]].append(method)

                    for target_class, methods in methods_by_class.items():
                        f.write(f"\n**Target class: `{target_class}`**\n")
                        for method in methods:
                            method_type = (
                                "classmethod"
                                if method["is_classmethod"]
                                else "instance method"
                            )
                            async_marker = "async " if method["is_async"] else ""
                            f.write(
                                f"- Line {method['line']}: `{async_marker}{method['name']}()` ({method_type})\n"
                            )

                        # Show refactoring example for first method
                        if methods:
                            example_method = methods[0]
                            f.write(
                                f"\n**Example refactor for `{example_method['name']}`:**\n"
                            )
                            f.write("```python\n")
                            f.write("# BEFORE:\n")
                            f.write(f"@patch_to({target_class}")
                            if example_method["is_classmethod"]:
                                f.write(", cls_method=True")
                            f.write(")\n")
                            if example_method["is_async"]:
                                f.write("async ")
                            f.write(f"def {example_method['name']}(")
                            if example_method["is_classmethod"]:
                                f.write(f"cls: {target_class}, ...):\n")
                            else:
                                f.write(f"self: {target_class}, ...):\n")
                            f.write("    pass\n\n")

                            f.write("# AFTER (inside class definition):\n")
                            if example_method["is_classmethod"]:
                                f.write("@classmethod\n")
                            if example_method["is_async"]:
                                f.write("async ")
                            f.write(f"def {example_method['name']}(")
                            if example_method["is_classmethod"]:
                                f.write("cls, ...):\n")
                            else:
                                f.write("self, ...):\n")
                            f.write("    pass\n")
                            f.write("```\n\n")

                f.write("---\n\n")

        # Class-by-class summary
        f.write("## Methods by Target Class\n\n")
        f.write("This shows which methods need to be moved into each class:\n\n")

        for class_name in sorted(plan["by_class"].keys()):
            methods = plan["by_class"][class_name]
            f.write(f"### {class_name}\n\n")
            f.write(f"**Total methods:** {len(methods)}\n\n")

            for method_info in methods:
                method_type = (
                    "classmethod" if method_info["is_classmethod"] else "instance"
                )
                async_marker = "async " if method_info["is_async"] else ""
                f.write(
                    f"- `{async_marker}{method_info['method']}()` ({method_type}) - {method_info['file']}:{method_info['line']}\n"
                )
            f.write("\n")

        # Implementation checklist
        f.write("## Implementation Checklist\n\n")
        f.write("For each file:\n\n")
        f.write("- [ ] Backup original file\n")
        f.write("- [ ] Move all @patch_to methods into their target classes\n")
        f.write("- [ ] Add @classmethod decorators where needed\n")
        f.write("- [ ] Remove explicit self/cls type hints\n")
        f.write("- [ ] Add forward reference quotes to return types\n")
        f.write("- [ ] Remove @patch_to imports if no longer needed\n")
        f.write("- [ ] Test syntax: `python -m py_compile filename.py`\n")
        f.write("- [ ] Test imports work\n")
        f.write("- [ ] Run linting\n\n")

        f.write("## Quality Assurance\n\n")
        f.write("After refactoring:\n\n")
        f.write("```bash\n")
        f.write("# Test all imports work\n")
        f.write("python -c \"import src; print('All imports successful')\"\n\n")
        f.write("# Run linting\n")
        f.write(".\\scripts\\lint.ps1\n\n")
        f.write("# Check for remaining @patch_to usage\n")
        f.write('findstr /s /n "@patch_to" src\\*.py\n')
        f.write("```\n")


def main():
    src_dir = Path("src")
    if not src_dir.exists():
        print("src directory not found")
        return 1

    print("Analyzing @patch_to usage...")
    plan = generate_refactoring_plan(src_dir)

    print("Creating refactoring guide...")
    create_refactoring_guide(plan, "patch-to-refactoring-guide.md")

    summary = plan["summary"]
    print(f"\n📋 Analysis complete!")
    print(f"📊 Files to refactor: {summary['files_with_patches']}")
    print(f"🔧 Methods to move: {summary['total_patch_methods']}")
    print(f"🏗️  Classes affected: {summary['affected_classes']}")
    print(f"📖 See patch-to-refactoring-guide.md for detailed implementation plan")

    return 0


if __name__ == "__main__":
    exit(main())
