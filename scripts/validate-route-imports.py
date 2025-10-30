#!/usr/bin/env python3
"""
Quick route import validator script.

This is a lightweight script to quickly validate that all route files
can be imported without errors. Useful for development and CI.

Usage:
    python scripts/validate-route-imports.py
    python scripts/validate-route-imports.py --verbose
    python scripts/validate-route-imports.py --fail-fast
"""

import argparse
import importlib
import sys
from pathlib import Path
from typing import list


def discover_route_modules(routes_path: Path) -> list[tuple[str, Path]]:
    """Discover all route modules to test."""
    modules = []

    # Main routes package
    modules.append(("src.routes", routes_path / "__init__.py"))

    # Individual route files
    for py_file in routes_path.glob("*.py"):
        if py_file.name != "__init__.py":
            module_name = f"src.routes.{py_file.stem}"
            modules.append((module_name, py_file))

    # Route subpackages
    for subdir in routes_path.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("__"):
            init_file = subdir / "__init__.py"
            if init_file.exists():
                # Package itself
                module_name = f"src.routes.{subdir.name}"
                modules.append((module_name, init_file))

                # Files within package
                for py_file in subdir.glob("*.py"):
                    if py_file.name != "__init__.py":
                        sub_module = f"src.routes.{subdir.name}.{py_file.stem}"
                        modules.append((sub_module, py_file))

    return sorted(modules)


def test_import(module_name: str, verbose: bool = False) -> dict:
    """Test importing a single module."""
    result = {
        "module": module_name,
        "success": False,
        "error": None,
        "error_type": None,
        "exports": [],
    }

    try:
        module = importlib.import_module(module_name)
        result["success"] = True

        if hasattr(module, "__all__"):
            result["exports"] = list(module.__all__)

        if verbose:
            print(f"  ✅ {module_name} ({len(result['exports'])} exports)")

    except Exception as e:
        result["error"] = str(e)
        result["error_type"] = type(e).__name__

        if verbose:
            print(f"  ❌ {module_name}: {result['error_type']} - {result['error']}")

    return result


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Validate route imports")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--fail-fast", "-f", action="store_true", help="Stop on first failure"
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show failures")

    args = parser.parse_args()

    # Find routes directory and add src to Python path
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    src_path = project_root / "src"
    routes_path = src_path / "routes"

    if not routes_path.exists():
        print(f"❌ Routes directory not found: {routes_path}")
        sys.exit(1)

    # Add project root to Python path so we can import src.routes
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Discover modules
    modules = discover_route_modules(routes_path)

    if not args.quiet:
        print(f"🔍 Testing {len(modules)} route modules...")
        if args.verbose:
            print()

    # Test imports
    results = []
    failed_count = 0

    for module_name, file_path in modules:
        result = test_import(module_name, args.verbose)
        results.append(result)

        if not result["success"]:
            failed_count += 1

            if not args.verbose and not args.quiet:
                print(f"❌ {module_name}: {result['error_type']}")

            if args.fail_fast:
                if not args.quiet:
                    print("\n💥 Stopping on first failure (--fail-fast)")
                    print(f"   Module: {module_name}")
                    print(f"   Error: {result['error']}")
                sys.exit(1)

    # Summary
    success_count = len(modules) - failed_count
    success_rate = (success_count / len(modules)) * 100

    if not args.quiet:
        print()
        print(
            f"📊 Results: {success_count}/{len(modules)} successful ({success_rate:.1f}%)"
        )

    if failed_count > 0:
        if not args.quiet:
            print(f"\n❌ Failed imports ({failed_count}):")

        for result in results:
            if not result["success"]:
                if args.quiet:
                    print(
                        f"{result['module']}: {result['error_type']} - {result['error']}"
                    )
                else:
                    print(f"  • {result['module']}: {result['error_type']}")
                    if args.verbose:
                        print(f"    {result['error']}")

        sys.exit(1)
    else:
        if not args.quiet:
            print("✅ All route modules imported successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
