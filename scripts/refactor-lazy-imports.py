#!/usr/bin/env python3
"""
Refactor class imports to use lazy loading for non-subclass dependencies.

This script identifies class-to-class imports and moves them inside methods
to prevent circular import issues and improve loading performance.

Usage:
    python scripts/refactor-lazy-imports.py
    python scripts/refactor-lazy-imports.py --dry-run
"""

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class LazyImportRefactorer:
    """Helper class to refactor imports to lazy loading."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.changes_made = []
        self.errors = []

    def log_change(self, file_path: str, change_type: str, description: str):
        """Log a change that was made."""
        self.changes_made.append(
            {"file": file_path, "type": change_type, "description": description}
        )

    def log_error(self, file_path: str, error: str):
        """Log an error that occurred."""
        self.errors.append({"file": file_path, "error": error})

    def analyze_imports(self, file_path: Path) -> Dict:
        """Analyze imports in a file to identify candidates for lazy loading."""
        result = {
            "class_imports": [],  # Imports from same package (classes)
            "route_imports": [],  # Route module imports
            "other_internal_imports": [],  # Other internal imports
            "has_inheritance": False,
            "class_names": [],
        }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Find class definitions to understand inheritance
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    result["class_names"].append(node.name)
                    if node.bases:
                        result["has_inheritance"] = True

            # Find imports
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        if node.module.startswith(".") and "classes" not in node.module:
                            # Internal imports from same package (classes)
                            for alias in node.names:
                                result["class_imports"].append(
                                    {
                                        "module": node.module,
                                        "name": alias.name,
                                        "asname": alias.asname,
                                        "line": node.lineno,
                                    }
                                )
                        elif node.module.startswith("..routes"):
                            # Route imports
                            for alias in node.names:
                                result["route_imports"].append(
                                    {
                                        "module": node.module,
                                        "name": alias.name,
                                        "asname": alias.asname,
                                        "line": node.lineno,
                                    }
                                )
                        elif node.module.startswith(".."):
                            # Other internal imports
                            for alias in node.names:
                                result["other_internal_imports"].append(
                                    {
                                        "module": node.module,
                                        "name": alias.name,
                                        "asname": alias.asname,
                                        "line": node.lineno,
                                    }
                                )

        except Exception as e:
            self.log_error(str(file_path), f"Failed to analyze imports: {e}")

        return result

    def find_import_usage(
        self, content: str, import_name: str, alias: str = None
    ) -> List[int]:
        """Find line numbers where an import is used."""
        usage_lines = []
        lines = content.split("\n")

        # Use alias if available, otherwise use the import name
        search_name = alias if alias else import_name

        for i, line in enumerate(lines, 1):
            # Skip import lines
            if "import" in line and (import_name in line or (alias and alias in line)):
                continue

            # Look for usage
            if search_name in line:
                # Simple heuristic - if the name appears and it's not a comment
                if not line.strip().startswith("#"):
                    usage_lines.append(i)

        return usage_lines

    def create_lazy_import_function(self, import_info: Dict, file_stem: str) -> str:
        """Create a lazy import function for an import."""
        alias = import_info.get("asname") or import_info["name"]
        module = import_info["module"]
        name = import_info["name"]

        # Create function name
        func_name = f"_lazy_import_{alias.lower().replace('.', '_')}"

        # Create the function
        if module.startswith("."):
            import_statement = f"from {module} import {name}"
        else:
            import_statement = f"import {module}"

        if import_info.get("asname"):
            import_statement += f" as {import_info['asname']}"

        return f"""def {func_name}():
    \"\"\"Lazy import for {alias}.\"\"\"
    {import_statement}
    return {alias}"""

    def refactor_file(self, file_path: Path) -> bool:
        """Refactor a single file to use lazy imports."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            analysis = self.analyze_imports(file_path)

            # Skip files with no candidate imports
            candidates = analysis["class_imports"] + analysis["route_imports"]
            if not candidates:
                return False

            # For now, let's focus on class imports that aren't inheritance-related
            # This is a conservative approach to avoid breaking inheritance chains

            # Remove import statements that are candidates for lazy loading
            lines = content.split("\n")
            new_lines = []
            lazy_functions = []
            imports_to_remove = set()

            for candidate in candidates:
                # Check if this import might be for inheritance
                line_content = (
                    lines[candidate["line"] - 1]
                    if candidate["line"] <= len(lines)
                    else ""
                )

                # Skip if this looks like it might be used for inheritance
                # This is a heuristic - in practice, you'd want more sophisticated analysis
                if any(
                    class_name in line_content for class_name in analysis["class_names"]
                ):
                    continue

                # Check usage to determine if we should make it lazy
                alias = candidate.get("asname") or candidate["name"]
                usage_lines = self.find_import_usage(content, candidate["name"], alias)

                # If used in class definition lines, skip (likely inheritance)
                class_def_lines = []
                for line_num, line in enumerate(lines, 1):
                    if line.strip().startswith("class ") and ":" in line:
                        class_def_lines.append(line_num)

                if any(line in class_def_lines for line in usage_lines):
                    continue

                # Mark for removal and create lazy function
                imports_to_remove.add(candidate["line"] - 1)  # Convert to 0-based
                lazy_func = self.create_lazy_import_function(candidate, file_path.stem)
                lazy_functions.append(lazy_func)

            # If no imports to refactor, return early
            if not lazy_functions:
                return False

            # Rebuild the file
            for i, line in enumerate(lines):
                if i not in imports_to_remove:
                    new_lines.append(line)

            # Add lazy import functions after existing imports
            # Find a good place to insert them
            insert_index = 0
            for i, line in enumerate(new_lines):
                if line.strip().startswith("import ") or line.strip().startswith(
                    "from "
                ):
                    insert_index = i + 1
                elif line.strip() and not line.strip().startswith("#"):
                    break

            # Insert lazy functions
            for lazy_func in reversed(lazy_functions):
                for func_line in reversed(lazy_func.split("\n")):
                    new_lines.insert(insert_index, func_line)
                new_lines.insert(insert_index, "")  # Add blank line

            new_content = "\n".join(new_lines)

            if new_content != original_content:
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)

                self.log_change(
                    str(file_path),
                    "lazy_import_refactor",
                    f"Converted {len(lazy_functions)} imports to lazy loading",
                )
                return True

        except Exception as e:
            self.log_error(str(file_path), f"Failed to refactor file: {e}")

        return False

    def process_directory(self, directory: Path) -> Dict:
        """Process all Python files in a directory."""
        results = {
            "files_processed": 0,
            "files_modified": 0,
            "total_imports_converted": 0,
        }

        for py_file in directory.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            results["files_processed"] += 1

            # Analyze first
            analysis = self.analyze_imports(py_file)
            candidates = analysis["class_imports"] + analysis["route_imports"]

            if candidates and self.refactor_file(py_file):
                results["files_modified"] += 1

        return results

    def generate_report(self) -> str:
        """Generate a report of all changes made."""
        report = []
        report.append("Lazy Import Refactoring Report")
        report.append("=" * 50)

        if self.dry_run:
            report.append("🔍 DRY RUN - No changes were actually made\n")

        # Group changes by type
        refactor_changes = [
            c for c in self.changes_made if c["type"] == "lazy_import_refactor"
        ]

        report.append(f"📊 Summary:")
        report.append(f"  • Files refactored: {len(refactor_changes)}")
        report.append(f"  • Errors: {len(self.errors)}")
        report.append("")

        if refactor_changes:
            report.append("🔧 Files Refactored for Lazy Imports:")
            for change in refactor_changes:
                report.append(f"  • {change['file']}: {change['description']}")
            report.append("")

        if self.errors:
            report.append("❌ Errors Encountered:")
            for error in self.errors:
                report.append(f"  • {error['file']}: {error['error']}")
            report.append("")

        if not self.dry_run and refactor_changes:
            report.append("⚠️  IMPORTANT: Manual Review Required")
            report.append("After refactoring imports, you may need to:")
            report.append("1. Update method calls to use lazy_import_*() functions")
            report.append("2. Ensure lazy imports are called in appropriate methods")
            report.append("3. Test that functionality is preserved")
            report.append("4. Review for any missed import dependencies")

        return "\n".join(report)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Refactor class imports to use lazy loading"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--target", help="Specific file to refactor (default: all classes)"
    )

    args = parser.parse_args()

    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    refactorer = LazyImportRefactorer(dry_run=args.dry_run)

    print("🔄 Refactoring imports for lazy loading...")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
    print()

    # Process classes directory
    classes_dir = project_root / "src" / "classes"
    if classes_dir.exists():
        if args.target:
            target_file = classes_dir / args.target
            if target_file.exists():
                if args.verbose:
                    print(f"Processing {target_file}...")
                refactorer.refactor_file(target_file)
            else:
                print(f"❌ Target file not found: {target_file}")
                sys.exit(1)
        else:
            if args.verbose:
                print(f"Processing {classes_dir}...")
            results = refactorer.process_directory(classes_dir)
            if args.verbose:
                print(f"  Processed {results['files_processed']} files")
                print(f"  Modified {results['files_modified']} files")

    # Generate and display report
    print(refactorer.generate_report())

    # Exit with error code if there were errors
    if refactorer.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
