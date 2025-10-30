#!/usr/bin/env python3
"""
Script to systematically add type hints to Python files following project conventions.
This script analyzes existing patterns and suggests type hints.
"""

import argparse
import ast
import os
from pathlib import Path
from typing import list


class TypeHintAnalyzer(ast.NodeVisitor):
    """Analyze Python files and suggest type hints based on project patterns"""

    def __init__(self, filename: str):
        self.filename = filename
        self.suggestions: list[dict] = []
        self.current_class = None
        self.imports = set()
        self.existing_typing_imports = set()
        self.needs_typing_imports = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.add(alias.name)
            if alias.name.startswith("typing"):
                self.existing_typing_imports.add(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module == "typing":
            for alias in node.names:
                self.existing_typing_imports.add(alias.name)
        if node.module:
            self.imports.add(node.module)

    def visit_ClassDef(self, node: ast.ClassDef):
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.analyze_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.analyze_function(node, is_async=True)
        self.generic_visit(node)

    def analyze_function(self, node, is_async=False):
        """Analyze function and suggest type hints"""
        # Skip private methods and special methods
        if node.name.startswith("_"):
            return


        # Analyze parameters
        missing_param_hints = []
        for arg in node.args.args:
            if arg.arg in ["self", "cls"]:
                continue
            if arg.annotation is None:
                param_type = self.suggest_param_type(arg.arg, node.name, is_async)
                missing_param_hints.append(
                    {"param": arg.arg, "suggested_type": param_type}
                )

        # Analyze return type
        return_type_suggestion = None
        if node.returns is None:
            return_type_suggestion = self.suggest_return_type(node.name, is_async, node)

        if missing_param_hints or return_type_suggestion:
            location = (
                f"{self.current_class}.{node.name}" if self.current_class else node.name
            )
            suggestion = {
                "function": location,
                "line": node.lineno,
                "is_async": is_async,
                "missing_params": missing_param_hints,
                "return_type": return_type_suggestion,
                "file": self.filename,
            }
            self.suggestions.append(suggestion)

    def suggest_param_type(
        self, param_name: str, func_name: str, is_async: bool
    ) -> str:
        """Suggest type hint for parameter based on naming patterns"""

        # Common parameter patterns in the project
        param_patterns = {
            "auth": "dmda.DomoAuth",
            "session": "Optional[httpx.AsyncClient]",
            "debug_api": "bool",
            "debug_num_stacks_to_drop": "int",
            "return_raw": "bool",
            "domo_instance": "str",
            "user_id": "str",
            "email": "str",
            "email_address": "str",
            "display_name": "str",
            "role_id": "str",
            "page_id": "str",
            "dataset_id": "str",
            "password": "str",
            "token": "str",
            "user_ids": "list[str]",
            "email_ls": "list[str]",
            "property_ls": "list[UserProperty]",
            "only_allow_one": "bool",
            "suppress_no_results_error": "bool",
            "pixels": "int",
            "folder_path": "str",
            "img_name": "Optional[str]",
            "is_download_image": "bool",
            "send_password_reset_email": "bool",
        }

        # Check exact matches first
        if param_name in param_patterns:
            self.needs_typing_imports.update(["Optional", "list"])
            return param_patterns[param_name]

        # Pattern matching
        if param_name.endswith("_id") or param_name.endswith("_name"):
            return "str"
        elif param_name.endswith("_ls") or param_name.endswith("_list"):
            self.needs_typing_imports.add("list")
            return "list[str]"  # Default to list[str], may need manual adjustment
        elif param_name.startswith("is_") or param_name.startswith("has_"):
            return "bool"
        elif "date" in param_name or "time" in param_name:
            return "Optional[dt.datetime]"

        # Default suggestion
        return "Any"

    def suggest_return_type(self, func_name: str, is_async: bool, node) -> str:
        """Suggest return type based on function patterns"""

        # Analyze function body for return statements
        return_types = set()

        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value:
                # Try to infer from return value
                if isinstance(child.value, ast.Constant):
                    if child.value.value is None:
                        return_types.add("None")
                    elif isinstance(child.value.value, bool):
                        return_types.add("bool")
                    elif isinstance(child.value.value, str):
                        return_types.add("str")
                elif isinstance(child.value, ast.Name):
                    if child.value.id == "True" or child.value.id == "False":
                        return_types.add("bool")
                    elif child.value.id == "None":
                        return_types.add("None")

        # Function name patterns
        if func_name.startswith("get_") and not func_name.endswith("_all"):
            if self.current_class:
                self.needs_typing_imports.add("Optional")
                return f"Optional[{self.current_class}]"
            return "Optional[Any]"
        elif func_name.startswith("get_") and func_name.endswith("_all"):
            if self.current_class:
                self.needs_typing_imports.add("list")
                return f"list[{self.current_class.replace('s', '')}]"  # Remove trailing 's'
            return "list[Any]"
        elif func_name in ["create", "upsert"]:
            if self.current_class:
                return self.current_class.replace(
                    "s", ""
                )  # Remove trailing 's' for collection classes
            return "Any"
        elif func_name.startswith("search_"):
            if self.current_class:
                self.needs_typing_imports.update(["Union", "list", "Optional"])
                base_class = self.current_class.replace("s", "")
                return f"Union[{base_class}, list[{base_class}], None]"
            return "Union[Any, list[Any], None]"
        elif func_name in ["delete", "update", "reset_password", "upload_avatar"]:
            if is_async:
                return "ResponseGetData"
            return "bool"
        elif func_name.startswith("download_"):
            return "bytes"
        elif "test" in func_name or "check" in func_name or func_name.startswith("is_"):
            return "bool"

        # For async functions, common patterns
        if is_async:
            if "return_raw" in [arg.arg for arg in node.args.args]:
                if self.current_class:
                    self.needs_typing_imports.add("Union")
                    base_class = (
                        self.current_class.replace("s", "")
                        if self.current_class.endswith("s")
                        else self.current_class
                    )
                    return f"Union[{base_class}, ResponseGetData, None]"
                return "Union[Any, ResponseGetData, None]"
            return "ResponseGetData"

        # Check if function has return statements
        if return_types:
            if len(return_types) == 1:
                return_type = list(return_types)[0]
                return return_type if return_type != "None" else "None"
            else:
                self.needs_typing_imports.add("Union")
                return f"Union[{', '.join(sorted(return_types))}]"

        # Default
        return "None" if not is_async else "Any"


def analyze_file(file_path: Path) -> TypeHintAnalyzer:
    """Analyze a single Python file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        analyzer = TypeHintAnalyzer(str(file_path))
        analyzer.visit(tree)
        return analyzer
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return TypeHintAnalyzer(str(file_path))


def generate_type_hint_suggestions(directory: Path) -> dict[str, TypeHintAnalyzer]:
    """Generate type hint suggestions for all Python files in directory"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for file in files:
            if file.endswith(".py") and not file.startswith("."):
                python_files.append(Path(root) / file)

    results = {}
    for file_path in python_files:
        analyzer = analyze_file(file_path)
        if analyzer.suggestions:
            results[str(file_path)] = analyzer

    return results


def create_implementation_guide(results: dict[str, TypeHintAnalyzer], output_file: str):
    """Create a detailed implementation guide"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Type Hints Implementation Guide\n\n")
        f.write(
            "This guide provides specific suggestions for adding type hints to your codebase.\n\n"
        )

        # Priority order
        priority_dirs = ["classes", "client", "routes", "utils", "integrations"]

        for priority_dir in priority_dirs:
            f.write(f"## {priority_dir.title()} Directory\n\n")

            files_in_dir = [
                file_path
                for file_path in results.keys()
                if f"\\{priority_dir}\\" in file_path
                or f"/{priority_dir}/" in file_path
            ]

            if not files_in_dir:
                f.write("No files requiring type hints found.\n\n")
                continue

            for file_path in sorted(files_in_dir):
                analyzer = results[file_path]

                f.write(f"### {Path(file_path).name}\n\n")

                # Required imports
                if analyzer.needs_typing_imports:
                    missing_imports = (
                        analyzer.needs_typing_imports - analyzer.existing_typing_imports
                    )
                    if missing_imports:
                        f.write("**Add these imports:**\n")
                        f.write("```python\n")
                        f.write(
                            f"from typing import {', '.join(sorted(missing_imports))}\n"
                        )
                        f.write("```\n\n")

                # Function suggestions
                for suggestion in analyzer.suggestions:
                    f.write(
                        f"**Line {suggestion['line']}: `{suggestion['function']}`**\n\n"
                    )

                    if suggestion["missing_params"]:
                        f.write("Parameter type hints:\n")
                        for param in suggestion["missing_params"]:
                            f.write(
                                f"- `{param['param']}: {param['suggested_type']}`\n"
                            )
                        f.write("\n")

                    if suggestion["return_type"]:
                        f.write(f"Return type: `{suggestion['return_type']}`\n\n")

                    # Generate complete signature suggestion
                    f.write("**Suggested signature:**\n")
                    f.write("```python\n")
                    if suggestion["is_async"]:
                        f.write("async ")
                    f.write(f"def {suggestion['function'].split('.')[-1]}(\n")

                    # Add self/cls parameter
                    if "." in suggestion["function"]:
                        f.write("    self,\n")

                    # Add typed parameters
                    for param in suggestion["missing_params"]:
                        default = (
                            " = None"
                            if param["suggested_type"].startswith("Optional")
                            else ""
                        )
                        default = (
                            " = False"
                            if param["suggested_type"] == "bool"
                            and "debug" in param["param"]
                            else default
                        )
                        f.write(
                            f"    {param['param']}: {param['suggested_type']}{default},\n"
                        )

                    f.write(f") -> {suggestion['return_type']}:\n")
                    f.write("    pass\n")
                    f.write("```\n\n")
                f.write("\n")

        # Summary
        total_functions = sum(
            len(analyzer.suggestions) for analyzer in results.values()
        )
        f.write("## Summary\n\n")
        f.write(f"- **Files to update:** {len(results)}\n")
        f.write(f"- **Functions needing type hints:** {total_functions}\n")
        f.write(
            "- **Implementation priority:** classes → client → routes → utils → integrations\n\n"
        )

        f.write("## Next Steps\n\n")
        f.write("1. Start with the `classes/` directory\n")
        f.write("2. Add the suggested imports to each file\n")
        f.write("3. Add type hints to functions following the suggestions\n")
        f.write("4. Test that imports work after changes\n")
        f.write("5. Run linting to ensure consistency\n")
        f.write("6. Move to the next directory\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate type hint implementation guide"
    )
    parser.add_argument(
        "directory", default="src", nargs="?", help="Directory to analyze"
    )
    parser.add_argument(
        "--output", default="type-hints-guide.md", help="Output guide file"
    )

    args = parser.parse_args()

    src_dir = Path(args.directory)
    if not src_dir.exists():
        print(f"Directory {src_dir} does not exist")
        return 1

    print(f"Analyzing {src_dir} for type hint opportunities...")
    results = generate_type_hint_suggestions(src_dir)

    if not results:
        print("🎉 All functions already have type hints!")
        return 0

    print(f"Creating implementation guide: {args.output}")
    create_implementation_guide(results, args.output)

    total_functions = sum(len(analyzer.suggestions) for analyzer in results.values())
    print(
        f"\n📋 Generated guide for {len(results)} files with {total_functions} functions needing type hints"
    )
    print(f"📖 See {args.output} for detailed implementation instructions")

    return 0


if __name__ == "__main__":
    exit(main())
