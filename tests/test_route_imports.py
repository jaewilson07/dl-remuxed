"""
Test module for validating that all route files can be imported without errors.

This test ensures that:
1. All individual route files can be imported
2. The route package and its subpackages can be imported
3. No circular imports or syntax errors exist
4. All dependencies are properly resolved

Run with: pytest tests/test_route_imports.py -v
"""

import importlib
import inspect
import os
import pkgutil
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Any

import pytest


class RouteImportTester:
    """Helper class for testing route imports."""

    def __init__(self, routes_path: str = None):
        """Initialize the tester with the routes directory path."""
        if routes_path is None:
            # Auto-detect routes path relative to this test file
            test_dir = Path(__file__).parent
            project_root = test_dir.parent
            self.routes_path = project_root / "src" / "routes"

            # Add project root to Python path for imports
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
        else:
            self.routes_path = Path(routes_path)

        self.routes_module_path = "src.routes"
        self.import_results = {}
        self.failed_imports = {}

    def discover_route_files(self) -> List[Tuple[str, Path]]:
        """
        Discover all route files and packages.

        Returns:
            List of tuples (module_name, file_path)
        """
        route_files = []

        # Add the main routes package
        route_files.append(("src.routes", self.routes_path / "__init__.py"))

        # Discover individual route files
        for file_path in self.routes_path.glob("*.py"):
            if file_path.name == "__init__.py":
                continue

            module_name = f"src.routes.{file_path.stem}"
            route_files.append((module_name, file_path))

        # Discover route subpackages (like account/)
        for subdir in self.routes_path.iterdir():
            if subdir.is_dir() and not subdir.name.startswith("__"):
                init_file = subdir / "__init__.py"
                if init_file.exists():
                    module_name = f"src.routes.{subdir.name}"
                    route_files.append((module_name, init_file))

                    # Also discover files within the subpackage
                    for py_file in subdir.glob("*.py"):
                        if py_file.name == "__init__.py":
                            continue
                        sub_module_name = f"src.routes.{subdir.name}.{py_file.stem}"
                        route_files.append((sub_module_name, py_file))

        return sorted(route_files)

    def test_single_import(self, module_name: str, file_path: Path) -> Dict[str, Any]:
        """
        Test importing a single module.

        Args:
            module_name: The full module name (e.g., 'src.routes.auth')
            file_path: Path to the file being imported

        Returns:
            Dictionary with import results
        """
        result = {
            "module_name": module_name,
            "file_path": str(file_path),
            "success": False,
            "error": None,
            "error_type": None,
            "error_details": None,
            "module": None,
            "exports": [],
        }

        try:
            # Import the module
            module = importlib.import_module(module_name)
            result["module"] = module
            result["success"] = True

            # Get exported items from __all__ if available
            if hasattr(module, "__all__"):
                result["exports"] = list(module.__all__)
            else:
                # Fall back to public attributes
                result["exports"] = [
                    name for name in dir(module) if not name.startswith("_")
                ]

        except Exception as e:
            result["error"] = str(e)
            result["error_type"] = type(e).__name__
            result["error_details"] = traceback.format_exc()

        return result

    def test_all_imports(self) -> Dict[str, Any]:
        """
        Test importing all discovered route files.

        Returns:
            Dictionary with overall results
        """
        route_files = self.discover_route_files()
        results = {
            "total_files": len(route_files),
            "successful_imports": 0,
            "failed_imports": 0,
            "import_results": {},
            "failed_modules": [],
            "summary": "",
        }

        print(f"\nTesting imports for {len(route_files)} route files/packages...")

        for module_name, file_path in route_files:
            print(f"  Testing: {module_name}")

            import_result = self.test_single_import(module_name, file_path)
            results["import_results"][module_name] = import_result

            if import_result["success"]:
                results["successful_imports"] += 1
                print(f"    ✅ SUCCESS - {len(import_result['exports'])} exports")
            else:
                results["failed_imports"] += 1
                results["failed_modules"].append(
                    {
                        "module": module_name,
                        "error": import_result["error"],
                        "error_type": import_result["error_type"],
                    }
                )
                print(
                    f"    ❌ FAILED - {import_result['error_type']}: {import_result['error']}"
                )

        # Generate summary
        success_rate = (results["successful_imports"] / results["total_files"]) * 100
        results["summary"] = (
            f"Import Test Results: {results['successful_imports']}/{results['total_files']} "
            f"successful ({success_rate:.1f}% success rate)"
        )

        return results

    def get_import_dependencies(self, module_name: str) -> List[str]:
        """
        Analyze import dependencies for a module.

        Args:
            module_name: The module to analyze

        Returns:
            List of imported module names
        """
        dependencies = []

        try:
            module = importlib.import_module(module_name)

            # Get all imported modules
            for name, obj in inspect.getmembers(module):
                if inspect.ismodule(obj):
                    dependencies.append(obj.__name__)

        except Exception:
            pass  # Module failed to import

        return dependencies

    def validate_module_exports(self, module_name: str) -> Dict[str, Any]:
        """
        Validate that all exports in __all__ are actually available.

        Args:
            module_name: Module to validate

        Returns:
            Validation results
        """
        result = {
            "module_name": module_name,
            "has_all": False,
            "all_exports": [],
            "missing_exports": [],
            "invalid_exports": [],
            "valid": True,
        }

        try:
            module = importlib.import_module(module_name)

            if hasattr(module, "__all__"):
                result["has_all"] = True
                result["all_exports"] = list(module.__all__)

                # Check each export
                for export_name in module.__all__:
                    if not hasattr(module, export_name):
                        result["missing_exports"].append(export_name)
                        result["valid"] = False
                    else:
                        # Check if the export is valid (not None, etc.)
                        export_obj = getattr(module, export_name)
                        if export_obj is None:
                            result["invalid_exports"].append(export_name)

        except Exception:
            result["valid"] = False

        return result


# Test fixtures and helper functions


@pytest.fixture
def route_tester():
    """Provide a RouteImportTester instance."""
    return RouteImportTester()


@pytest.fixture
def routes_path():
    """Get the path to the routes directory."""
    test_dir = Path(__file__).parent
    return test_dir.parent / "src" / "routes"


# Main test classes


class TestRouteImports:
    """Test class for route import validation."""

    def test_all_route_files_can_be_imported(self, route_tester):
        """Test that all route files can be imported without errors."""
        results = route_tester.test_all_imports()

        print(f"\n{results['summary']}")

        if results["failed_imports"] > 0:
            print("\nFailed imports:")
            for failed in results["failed_modules"]:
                print(
                    f"  - {failed['module']}: {failed['error_type']} - {failed['error']}"
                )

        # Assert that all imports succeeded
        assert results["failed_imports"] == 0, (
            f"{results['failed_imports']} route files failed to import. "
            f"See test output for details."
        )

    def test_routes_package_import(self, route_tester):
        """Test that the main routes package can be imported."""
        result = route_tester.test_single_import(
            "src.routes", route_tester.routes_path / "__init__.py"
        )

        assert result[
            "success"
        ], f"Routes package failed to import: {result['error_type']} - {result['error']}"

    def test_individual_route_files(self, route_tester, routes_path):
        """Test each individual route file separately."""
        failures = []

        for py_file in routes_path.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            module_name = f"src.routes.{py_file.stem}"
            result = route_tester.test_single_import(module_name, py_file)

            if not result["success"]:
                failures.append(
                    {
                        "file": py_file.name,
                        "module": module_name,
                        "error": result["error"],
                        "error_type": result["error_type"],
                    }
                )

        if failures:
            error_details = "\n".join(
                [f"  - {f['file']}: {f['error_type']} - {f['error']}" for f in failures]
            )
            pytest.fail(f"Individual route files failed to import:\n{error_details}")

    def test_route_subpackages(self, route_tester, routes_path):
        """Test route subpackages (like account/)."""
        failures = []

        for subdir in routes_path.iterdir():
            if subdir.is_dir() and not subdir.name.startswith("__"):
                init_file = subdir / "__init__.py"
                if init_file.exists():
                    module_name = f"src.routes.{subdir.name}"
                    result = route_tester.test_single_import(module_name, init_file)

                    if not result["success"]:
                        failures.append(
                            {
                                "package": subdir.name,
                                "module": module_name,
                                "error": result["error"],
                                "error_type": result["error_type"],
                            }
                        )

        if failures:
            error_details = "\n".join(
                [
                    f"  - {f['package']}/: {f['error_type']} - {f['error']}"
                    for f in failures
                ]
            )
            pytest.fail(f"Route subpackages failed to import:\n{error_details}")

    def test_route_exports_validation(self, route_tester):
        """Test that all modules with __all__ export valid items."""
        route_files = route_tester.discover_route_files()
        validation_failures = []

        for module_name, _ in route_files:
            validation = route_tester.validate_module_exports(module_name)

            if validation["has_all"] and not validation["valid"]:
                validation_failures.append(
                    {
                        "module": module_name,
                        "missing": validation["missing_exports"],
                        "invalid": validation["invalid_exports"],
                    }
                )

        if validation_failures:
            error_details = "\n".join(
                [
                    f"  - {f['module']}: "
                    f"missing={f['missing']}, invalid={f['invalid']}"
                    for f in validation_failures
                ]
            )
            pytest.fail(f"Route export validation failed:\n{error_details}")

    @pytest.mark.slow
    def test_import_performance(self, route_tester):
        """Test that route imports complete within reasonable time."""
        import time

        start_time = time.time()
        results = route_tester.test_all_imports()
        total_time = time.time() - start_time

        # Assert reasonable performance (adjust threshold as needed)
        max_time = 30.0  # 30 seconds max for all imports
        assert (
            total_time < max_time
        ), f"Route imports took {total_time:.2f}s, exceeding {max_time}s threshold"

        print(
            f"\nImport performance: {total_time:.2f}s for {results['total_files']} files"
        )

    def test_no_circular_imports(self, route_tester):
        """Test that there are no circular import issues."""
        # This test attempts to import all modules and checks for circular import errors
        route_files = route_tester.discover_route_files()
        circular_import_errors = []

        for module_name, _ in route_files:
            result = route_tester.test_single_import(module_name, _)
            if not result["success"] and "circular import" in result["error"].lower():
                circular_import_errors.append(
                    {"module": module_name, "error": result["error"]}
                )

        if circular_import_errors:
            error_details = "\n".join(
                [
                    f"  - {err['module']}: {err['error']}"
                    for err in circular_import_errors
                ]
            )
            pytest.fail(f"Circular import errors detected:\n{error_details}")


class TestSpecificRouteFiles:
    """Test specific route files that might have special requirements."""

    def test_auth_routes(self, route_tester):
        """Test authentication routes specifically."""
        result = route_tester.test_single_import("src.routes.auth", None)
        assert result["success"], f"Auth routes failed: {result['error']}"

    def test_account_package(self, route_tester):
        """Test the account package specifically."""
        # Test main package
        result = route_tester.test_single_import("src.routes.account", None)
        assert result["success"], f"Account package failed: {result['error']}"

        # Test individual account modules
        account_modules = [
            "src.routes.account.core",
            "src.routes.account.crud",
            "src.routes.account.oauth",
            "src.routes.account.config",
            "src.routes.account.sharing",
            "src.routes.account.exceptions",
        ]

        for module_name in account_modules:
            result = route_tester.test_single_import(module_name, None)
            assert result[
                "success"
            ], f"Account module {module_name} failed: {result['error']}"

    def test_core_utility_routes(self, route_tester):
        """Test core utility routes."""
        core_routes = [
            "src.routes.dataset",
            "src.routes.user",
            "src.routes.group",
            "src.routes.datacenter",
        ]

        for route in core_routes:
            result = route_tester.test_single_import(route, None)
            assert result["success"], f"Core route {route} failed: {result['error']}"


# Utility functions for running tests programmatically


def run_import_tests_standalone():
    """Run import tests outside of pytest for debugging."""
    tester = RouteImportTester()
    results = tester.test_all_imports()

    print(f"\n{'='*60}")
    print(f"ROUTE IMPORT TEST RESULTS")
    print(f"{'='*60}")
    print(f"{results['summary']}")

    if results["failed_imports"] > 0:
        print(f"\n❌ FAILED IMPORTS ({results['failed_imports']}):")
        for failed in results["failed_modules"]:
            print(f"  • {failed['module']}")
            print(f"    Error: {failed['error_type']} - {failed['error']}")
            print()

    if results["successful_imports"] > 0:
        print(f"\n✅ SUCCESSFUL IMPORTS ({results['successful_imports']}):")
        for module_name, result in results["import_results"].items():
            if result["success"]:
                exports_count = len(result["exports"])
                print(f"  • {module_name} ({exports_count} exports)")

    return results["failed_imports"] == 0


if __name__ == "__main__":
    """
    Run the import tests directly.

    Usage:
        python tests/test_route_imports.py

    Or with pytest:
        pytest tests/test_route_imports.py -v
        pytest tests/test_route_imports.py::TestRouteImports::test_all_route_files_can_be_imported -v
    """
    success = run_import_tests_standalone()
    sys.exit(0 if success else 1)
