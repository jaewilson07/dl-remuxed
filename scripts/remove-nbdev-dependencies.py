#!/usr/bin/env python3
"""
Remove all nbdev dependencies and refactor @patch_to decorators.

This script:
1. Removes all nbdev imports
2. Removes @patch_to decorators and their usage
3. Updates dependency files
4. Provides a report of changes made

Usage:
    python scripts/remove-nbdev-dependencies.py
    python scripts/remove-nbdev-dependencies.py --dry-run
"""

import argparse
import re
import sys
from pathlib import Path


class NBDevRemover:
    """Helper class to remove nbdev dependencies."""

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

    def remove_nbdev_imports(self, file_path: Path) -> bool:
        """Remove nbdev imports from a Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Remove nbdev imports
            # Pattern 1: from nbdev.showdoc import patch_to
            content = re.sub(
                r"^from nbdev\.showdoc import patch_to\s*\n",
                "",
                content,
                flags=re.MULTILINE,
            )

            # Pattern 2: from nbdev import *
            content = re.sub(
                r"^from nbdev import \*\s*\n", "", content, flags=re.MULTILINE
            )

            # Pattern 3: import nbdev
            content = re.sub(r"^import nbdev\s*\n", "", content, flags=re.MULTILINE)

            # Pattern 4: Other nbdev imports
            content = re.sub(
                r"^from nbdev[.\w]* import .*\n", "", content, flags=re.MULTILINE
            )

            if content != original_content:
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)

                self.log_change(
                    str(file_path), "import_removal", "Removed nbdev imports"
                )
                return True

        except Exception as e:
            self.log_error(str(file_path), f"Failed to remove imports: {e}")

        return False

    def remove_patch_to_decorators(self, file_path: Path) -> bool:
        """Remove @patch_to decorators from a Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Remove @patch_to decorators
            # This is a simple removal - more complex refactoring would need manual work
            content = re.sub(
                r"^@patch_to\([^)]*\)\s*\n", "", content, flags=re.MULTILINE
            )

            if content != original_content:
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)

                self.log_change(
                    str(file_path), "decorator_removal", "Removed @patch_to decorators"
                )
                return True

        except Exception as e:
            self.log_error(str(file_path), f"Failed to remove decorators: {e}")

        return False

    def update_pyproject_toml(self, file_path: Path) -> bool:
        """Update pyproject.toml to remove nbdev dependencies."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Remove nbdev from keywords
            content = re.sub(
                r'keywords = \[([^]]*)"nbdev",?\s*([^]]*)\]',
                r"keywords = [\1\2]",
                content,
            )

            # Clean up empty keywords or trailing commas
            content = re.sub(r"keywords = \[,\s*", "keywords = [", content)
            content = re.sub(r",\s*\]", "]", content)

            # Remove nbdev from dependencies
            content = re.sub(r'^\s*"nbdev",?\s*\n', "", content, flags=re.MULTILINE)

            # Remove nbdev entry points if present
            content = re.sub(
                r'^\s*"nbdev": \[[^\]]*\],?\s*\n', "", content, flags=re.MULTILINE
            )

            if content != original_content:
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)

                self.log_change(
                    str(file_path),
                    "dependency_removal",
                    "Removed nbdev from pyproject.toml",
                )
                return True

        except Exception as e:
            self.log_error(str(file_path), f"Failed to update pyproject.toml: {e}")

        return False

    def update_setup_py(self, file_path: Path) -> bool:
        """Update setup.py to remove nbdev references."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Remove nbdev entry points
            content = re.sub(
                r'^\s*"nbdev": \[[^\]]*\],?\s*\n', "", content, flags=re.MULTILINE
            )

            if content != original_content:
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)

                self.log_change(
                    str(file_path), "dependency_removal", "Removed nbdev from setup.py"
                )
                return True

        except Exception as e:
            self.log_error(str(file_path), f"Failed to update setup.py: {e}")

        return False

    def process_directory(self, directory: Path) -> dict:
        """Process all Python files in a directory."""
        results = {"files_processed": 0, "imports_removed": 0, "decorators_removed": 0}

        for py_file in directory.rglob("*.py"):
            results["files_processed"] += 1

            if self.remove_nbdev_imports(py_file):
                results["imports_removed"] += 1

            if self.remove_patch_to_decorators(py_file):
                results["decorators_removed"] += 1

        return results

    def generate_report(self) -> str:
        """Generate a report of all changes made."""
        report = []
        report.append("NBDev Removal Report")
        report.append("=" * 50)

        if self.dry_run:
            report.append("🔍 DRY RUN - No changes were actually made\n")

        # Group changes by type
        import_changes = [c for c in self.changes_made if c["type"] == "import_removal"]
        decorator_changes = [
            c for c in self.changes_made if c["type"] == "decorator_removal"
        ]
        dependency_changes = [
            c for c in self.changes_made if c["type"] == "dependency_removal"
        ]

        report.append("📊 Summary:")
        report.append(f"  • Import removals: {len(import_changes)}")
        report.append(f"  • Decorator removals: {len(decorator_changes)}")
        report.append(f"  • Dependency updates: {len(dependency_changes)}")
        report.append(f"  • Errors: {len(self.errors)}")
        report.append("")

        if import_changes:
            report.append("🗑️  NBDev Import Removals:")
            for change in import_changes:
                report.append(f"  • {change['file']}")
            report.append("")

        if decorator_changes:
            report.append("🔧 @patch_to Decorator Removals:")
            for change in decorator_changes:
                report.append(f"  • {change['file']}")
            report.append("")

        if dependency_changes:
            report.append("📦 Dependency File Updates:")
            for change in dependency_changes:
                report.append(f"  • {change['file']}: {change['description']}")
            report.append("")

        if self.errors:
            report.append("❌ Errors Encountered:")
            for error in self.errors:
                report.append(f"  • {error['file']}: {error['error']}")
            report.append("")

        if not self.dry_run:
            report.append("⚠️  IMPORTANT: Manual Review Required")
            report.append("After removing @patch_to decorators, you may need to:")
            report.append(
                "1. Move methods from standalone functions into their target classes"
            )
            report.append("2. Review method signatures and self parameters")
            report.append(
                "3. Update any method calls that relied on patched functionality"
            )
            report.append(
                "4. Test the affected classes to ensure functionality is preserved"
            )

        return "\n".join(report)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Remove nbdev dependencies from the project"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    remover = NBDevRemover(dry_run=args.dry_run)

    print("🧹 Removing nbdev dependencies...")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
    print()

    # Process source directory
    src_dir = project_root / "src"
    if src_dir.exists():
        if args.verbose:
            print(f"Processing {src_dir}...")
        results = remover.process_directory(src_dir)
        if args.verbose:
            print(f"  Processed {results['files_processed']} files")

    # Update dependency files
    pyproject_file = project_root / "pyproject.toml"
    if pyproject_file.exists():
        if args.verbose:
            print(f"Updating {pyproject_file}...")
        remover.update_pyproject_toml(pyproject_file)

    setup_file = project_root / "setup.py"
    if setup_file.exists():
        if args.verbose:
            print(f"Updating {setup_file}...")
        remover.update_setup_py(setup_file)

    # Generate and display report
    print(remover.generate_report())

    # Exit with error code if there were errors
    if remover.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
