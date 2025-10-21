#!/usr/bin/env python3
"""
Route syntax validator - checks for syntax errors without full imports.

This script validates route files for syntax errors and basic import issues
without trying to execute the full import chain, which can be problematic
due to dependencies and circular imports.

Usage:
    python scripts/check-route-syntax.py
    python scripts/check-route-syntax.py --verbose
"""

import argparse
import ast
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Tuple


def check_syntax(file_path: Path) -> Dict:
    """Check Python syntax without importing."""
    result = {
        "file": str(file_path.relative_to(Path.cwd())),
        "success": False,
        "error": None,
        "error_type": None,
        "line_number": None,
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        # Parse the AST to check syntax
        ast.parse(source, filename=str(file_path))
        result["success"] = True

    except SyntaxError as e:
        result["error"] = str(e)
        result["error_type"] = "SyntaxError"
        result["line_number"] = e.lineno

    except Exception as e:
        result["error"] = str(e)
        result["error_type"] = type(e).__name__

    return result


def analyze_imports(file_path: Path) -> Dict:
    """Analyze import statements in a file."""
    result = {
        "file": str(file_path.relative_to(Path.cwd())),
        "relative_imports": [],
        "absolute_imports": [],
        "from_imports": [],
        "potential_issues": [],
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result["absolute_imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.level > 0:  # Relative import
                    module_name = node.module or ""
                    for alias in node.names:
                        import_name = f"{'.' * node.level}{module_name}.{alias.name}"
                        result["relative_imports"].append(import_name)
                else:  # Absolute from import
                    module_name = node.module or ""
                    for alias in node.names:
                        import_name = f"{module_name}.{alias.name}"
                        result["from_imports"].append(import_name)

        # Check for potential issues
        if "nbdev" in str(result["absolute_imports"]) or "nbdev" in str(
            result["from_imports"]
        ):
            result["potential_issues"].append("nbdev dependency detected")

        if len(result["relative_imports"]) > 10:
            result["potential_issues"].append(
                "Many relative imports (potential circular import risk)"
            )

    except Exception as e:
        result["potential_issues"].append(f"Analysis failed: {e}")

    return result


def discover_python_files(routes_path: Path) -> List[Path]:
    """Discover all Python files in routes directory."""
    python_files = []

    # Individual route files
    for py_file in routes_path.glob("*.py"):
        python_files.append(py_file)

    # Files in subdirectories
    for subdir in routes_path.rglob("*.py"):
        if subdir not in python_files:
            python_files.append(subdir)

    return sorted(python_files)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Check route file syntax")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--analyze-imports", "-i", action="store_true", help="Analyze import patterns"
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show errors")

    args = parser.parse_args()

    # Find routes directory
    script_dir = Path(__file__).parent
    routes_path = script_dir.parent / "src" / "routes"

    if not routes_path.exists():
        print(f"❌ Routes directory not found: {routes_path}")
        sys.exit(1)

    # Discover Python files
    python_files = discover_python_files(routes_path)

    if not args.quiet:
        print(f"🔍 Checking syntax for {len(python_files)} Python files...")
        if args.verbose:
            print()

    # Check syntax
    results = []
    error_count = 0

    for file_path in python_files:
        result = check_syntax(file_path)
        results.append(result)

        if not result["success"]:
            error_count += 1

            if args.verbose:
                line_info = (
                    f" (line {result['line_number']})" if result["line_number"] else ""
                )
                print(f"❌ {result['file']}: {result['error_type']}{line_info}")
                if result["error"]:
                    print(f"   {result['error']}")
            elif not args.quiet:
                print(f"❌ {result['file']}: {result['error_type']}")
        else:
            if args.verbose:
                print(f"✅ {result['file']}")

    # Analyze imports if requested
    if args.analyze_imports:
        if not args.quiet:
            print(f"\n🔍 Analyzing import patterns...")

        import_issues = 0
        for file_path in python_files:
            if file_path.suffix == ".py":
                analysis = analyze_imports(file_path)

                if analysis["potential_issues"]:
                    import_issues += 1
                    if args.verbose or not args.quiet:
                        print(
                            f"⚠️  {analysis['file']}: {', '.join(analysis['potential_issues'])}"
                        )

    # Summary
    success_count = len(python_files) - error_count
    success_rate = (success_count / len(python_files)) * 100

    if not args.quiet:
        print()
        print(
            f"📊 Syntax Check Results: {success_count}/{len(python_files)} files valid ({success_rate:.1f}%)"
        )

    if error_count > 0:
        if not args.quiet:
            print(f"\n❌ Syntax errors found in {error_count} files:")

        for result in results:
            if not result["success"]:
                if args.quiet:
                    line_info = (
                        f":{result['line_number']}" if result["line_number"] else ""
                    )
                    print(
                        f"{result['file']}{line_info}: {result['error_type']} - {result['error']}"
                    )
                else:
                    print(f"  • {result['file']}: {result['error_type']}")
                    if args.verbose and result["error"]:
                        print(f"    {result['error']}")

        sys.exit(1)
    else:
        if not args.quiet:
            print("✅ All route files have valid syntax!")
        sys.exit(0)


if __name__ == "__main__":
    main()
