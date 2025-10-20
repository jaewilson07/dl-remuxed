#!/usr/bin/env python3
"""
Script to analyze Python files and identify functions missing type hints.
"""

import argparse
import ast
import os
from pathlib import Path
from typing import Dict, List


class TypeHintChecker(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.issues: List[Dict[str, any]] = []
        self.current_class = None

    def visit_ClassDef(self, node: ast.ClassDef):
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.check_function_typing(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.check_function_typing(node)
        self.generic_visit(node)

    def check_function_typing(self, node):
        """Check if function has proper type hints"""
        issues = []

        # Skip special methods and private methods for now
        if node.name.startswith("_"):
            return

        # Check return type annotation
        if node.returns is None:
            issues.append("Missing return type annotation")

        # Check parameter type annotations
        missing_params = []
        for arg in node.args.args:
            # Skip 'self' and 'cls' parameters
            if arg.arg in ["self", "cls"]:
                continue
            if arg.annotation is None:
                missing_params.append(arg.arg)

        if missing_params:
            issues.append(
                f"Missing type hints for parameters: {', '.join(missing_params)}"
            )

        # If there are issues, record them
        if issues:
            location = (
                f"{self.current_class}.{node.name}" if self.current_class else node.name
            )
            self.issues.append(
                {
                    "function": location,
                    "line": node.lineno,
                    "issues": issues,
                    "file": self.filename,
                }
            )


def analyze_file(file_path: Path) -> List[Dict]:
    """Analyze a single Python file for type hint issues"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        checker = TypeHintChecker(str(file_path))
        checker.visit(tree)
        return checker.issues
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return []


def find_python_files(directory: Path) -> List[Path]:
    """Find all Python files in directory recursively"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        for file in files:
            if file.endswith(".py") and not file.startswith("."):
                python_files.append(Path(root) / file)
    return python_files


def main():
    parser = argparse.ArgumentParser(
        description="Check Python files for missing type hints"
    )
    parser.add_argument(
        "directory",
        default="src",
        nargs="?",
        help="Directory to analyze (default: src)",
    )
    parser.add_argument(
        "--output",
        choices=["console", "file", "both"],
        default="console",
        help="Output format",
    )
    parser.add_argument(
        "--output-file",
        default="type-hints-report.txt",
        help="Output file name when using file output",
    )

    args = parser.parse_args()

    src_dir = Path(args.directory)
    if not src_dir.exists():
        print(f"Directory {src_dir} does not exist")
        return 1

    print(f"Analyzing Python files in {src_dir}...")

    python_files = find_python_files(src_dir)
    print(f"Found {len(python_files)} Python files")

    all_issues = []
    files_with_issues = 0

    for file_path in python_files:
        issues = analyze_file(file_path)
        if issues:
            all_issues.extend(issues)
            files_with_issues += 1

    # Generate report
    report_lines = []
    report_lines.append("Type Hint Analysis Report")
    report_lines.append("=" * 50)
    report_lines.append(f"Files analyzed: {len(python_files)}")
    report_lines.append(f"Files with issues: {files_with_issues}")
    report_lines.append(f"Total functions needing type hints: {len(all_issues)}")
    report_lines.append("")

    if all_issues:
        # Group by file
        by_file = {}
        for issue in all_issues:
            file_path = issue["file"]
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(issue)

        for file_path, file_issues in by_file.items():
            report_lines.append(f"File: {file_path}")
            report_lines.append("-" * len(f"File: {file_path}"))

            for issue in file_issues:
                report_lines.append(f"  Line {issue['line']}: {issue['function']}")
                for problem in issue["issues"]:
                    report_lines.append(f"    - {problem}")
                report_lines.append("")
            report_lines.append("")
    else:
        report_lines.append("🎉 All functions have proper type hints!")

    report_text = "\n".join(report_lines)

    # Output results
    if args.output in ["console", "both"]:
        print(report_text)

    if args.output in ["file", "both"]:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"\nReport saved to {args.output_file}")

    return 0


if __name__ == "__main__":
    exit(main())
