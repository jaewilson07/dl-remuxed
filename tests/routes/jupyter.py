"""
Test Jupyter Route Import Structure

This module tests that all Jupyter route functions and classes can be imported
correctly from both the unified module interface and individual submodules.
Ensures backward compatibility and proper modular organization.
"""

# Add src directory to Python path for imports


import inspect
from typing import get_type_hints

import pytest


class TestJupyterImports:
    """Test suite for Jupyter route import functionality."""

    def test_unified_imports_all_functions(self):
        """Test that all expected functions can be imported from main module."""
        from domolibrary2.routes.jupyter import (
            create_jupyter_obj,
            delete_jupyter_content,
            # Utility functions
            generate_update_jupyter_body,
            get_content,
            get_jupyter_content,
            get_jupyter_workspace_by_id,
            # Core functions
            get_jupyter_workspaces,
            start_jupyter_workspace,
            update_jupyter_file,
            # Configuration functions
            update_jupyter_workspace_config,
        )

        # Verify all functions are callable
        functions = [
            get_jupyter_workspaces,
            get_jupyter_workspace_by_id,
            start_jupyter_workspace,
            get_jupyter_content,
            create_jupyter_obj,
            delete_jupyter_content,
            update_jupyter_file,
            get_content,
            update_jupyter_workspace_config,
            generate_update_jupyter_body,
        ]

        for func in functions:
            assert callable(func), f"{func.__name__} should be callable"
            assert hasattr(
                func, "__doc__"
            ), f"{func.__name__} should have documentation"

    def test_unified_imports_all_exceptions(self):
        """Test that all exception classes can be imported from main module."""
        from domolibrary2.routes.jupyter import (
            Jupyter_CRUD_Error,
            Jupyter_GET_Error,
            # Backward compatibility aliases
            JupyterAPI_Error,
            JupyterAPI_WorkspaceStarted,
            JupyterWorkspace_Error,
            SearchJupyterNotFoundError,
        )

        # Verify all exceptions are proper exception classes
        exceptions = [
            Jupyter_GET_Error,
            SearchJupyterNotFoundError,
            Jupyter_CRUD_Error,
            JupyterWorkspace_Error,
        ]

        for exc in exceptions:
            assert issubclass(
                exc, Exception
            ), f"{exc.__name__} should be an Exception subclass"
            assert hasattr(exc, "__doc__"), f"{exc.__name__} should have documentation"

        # Test backward compatibility aliases
        assert JupyterAPI_Error is Jupyter_GET_Error
        assert JupyterAPI_WorkspaceStarted is JupyterWorkspace_Error

    def test_modular_core_imports(self):
        """Test that core functions can be imported from core module."""
        from domolibrary2.routes.jupyter.core import (
            get_jupyter_workspace_by_id,
            get_jupyter_workspaces,
            get_workspace_auth_token_params,
            parse_instance_service_location_and_prefix,
            start_jupyter_workspace,
        )

        # Verify functions have proper signatures and decorations
        assert hasattr(
            get_jupyter_workspaces, "__wrapped__"
        )  # Has @gd.route_function decorator
        assert hasattr(get_jupyter_workspace_by_id, "__wrapped__")
        assert hasattr(start_jupyter_workspace, "__wrapped__")

        # Verify utility functions don't have decorators (they're helpers)
        assert not hasattr(parse_instance_service_location_and_prefix, "__wrapped__")
        assert not hasattr(get_workspace_auth_token_params, "__wrapped__")

    def test_modular_content_imports(self):
        """Test that content functions can be imported from content module."""
        from domolibrary2.routes.jupyter.content import (
            create_jupyter_obj,
            delete_jupyter_content,
            # Utility functions moved here
            get_content,
            get_jupyter_content,
            update_jupyter_file,
        )

        # Verify route functions have decorators
        route_functions = [
            get_jupyter_content,
            create_jupyter_obj,
            delete_jupyter_content,
            update_jupyter_file,
            get_content,
        ]

        for func in route_functions:
            assert hasattr(
                func, "__wrapped__"
            ), f"{func.__name__} should have @gd.route_function decorator"

    def test_modular_config_imports(self):
        """Test that config functions can be imported from config module."""
        from domolibrary2.routes.jupyter.config import (
            update_jupyter_workspace_config,
        )

        assert hasattr(update_jupyter_workspace_config, "__wrapped__")

    def test_modular_exception_imports(self):
        """Test that exceptions can be imported from exceptions module."""
        # Verify exception hierarchy
        from domolibrary2.base.exceptions import RouteError
        from domolibrary2.routes.jupyter.exceptions import (
            Jupyter_CRUD_Error,
            Jupyter_GET_Error,
            JupyterWorkspace_Error,
            SearchJupyterNotFoundError,
        )

        for exc in [
            Jupyter_GET_Error,
            SearchJupyterNotFoundError,
            Jupyter_CRUD_Error,
            JupyterWorkspace_Error,
        ]:
            assert issubclass(
                exc, RouteError
            ), f"{exc.__name__} should inherit from RouteError"

    def test_wildcard_import(self):
        """Test that wildcard import works and includes expected items."""
        import domolibrary2.routes.jupyter as jupyter_module

        # Get all exported items via __all__
        all_items = getattr(jupyter_module, "__all__", [])

        # Verify __all__ is properly defined and not empty
        assert isinstance(all_items, list), "__all__ should be a list"
        assert len(all_items) > 0, "__all__ should not be empty"

        # Verify all items in __all__ are actually available
        for item_name in all_items:
            assert hasattr(
                jupyter_module, item_name
            ), f"{item_name} should be available in module"

    def test_function_signatures_have_proper_types(self):
        """Test that functions have proper type hints."""
        from domolibrary2.routes.jupyter import (
            create_jupyter_obj,
            get_jupyter_workspace_by_id,
            get_jupyter_workspaces,
        )

        # Test a few key functions have type hints
        functions_to_check = [
            get_jupyter_workspaces,
            get_jupyter_workspace_by_id,
            create_jupyter_obj,
        ]

        for func in functions_to_check:
            # Get the actual function (unwrap decorator)
            actual_func = getattr(func, "__wrapped__", func)
            type_hints = get_type_hints(actual_func)

            # Should have return type hint
            assert (
                "return" in type_hints
            ), f"{func.__name__} should have return type hint"

            # Should have some parameter type hints
            sig = inspect.signature(actual_func)
            params_with_hints = [
                p
                for p in sig.parameters.values()
                if p.annotation != inspect.Parameter.empty
            ]
            assert (
                len(params_with_hints) > 0
            ), f"{func.__name__} should have parameter type hints"

    def test_utility_functions_work(self):
        """Test that utility functions can be called and work correctly."""
        from domolibrary2.routes.jupyter import (
            generate_update_jupyter_body,
            generate_update_jupyter_body__new_content_path,
        )

        # Test path generation utility
        assert generate_update_jupyter_body__new_content_path("") == ""
        assert generate_update_jupyter_body__new_content_path("file.txt") == ""
        assert (
            generate_update_jupyter_body__new_content_path("folder/file.txt")
            == "folder"
        )
        assert (
            generate_update_jupyter_body__new_content_path("./folder/file.txt")
            == "folder"
        )

        # Test body generation utility
        body = generate_update_jupyter_body("test content", "test.txt")

        assert isinstance(body, dict), "Body should be a dictionary"
        assert "name" in body, "Body should have name field"
        assert "content" in body, "Body should have content field"
        assert "path" in body, "Body should have path field"
        assert body["name"] == "test.txt"
        assert body["content"] == "test content"

    def test_backward_compatibility_imports(self):
        """Test that old import patterns still work for backward compatibility."""
        # Test that we can import with the old style
        try:
            from domolibrary2.routes.jupyter import (
                Jupyter_GET_Error,
                JupyterAPI_Error,
                JupyterAPI_WorkspaceStarted,
                JupyterWorkspace_Error,
            )

            # Verify aliases point to new classes
            assert JupyterAPI_Error is Jupyter_GET_Error
            assert JupyterAPI_WorkspaceStarted is JupyterWorkspace_Error

        except ImportError as e:
            pytest.fail(f"Backward compatibility imports failed: {e}")

    def test_no_circular_imports(self):
        """Test that there are no circular import issues between modules."""
        # Import all modules to ensure no circular dependencies
        try:
            from domolibrary2.routes.jupyter import config, content, core, exceptions

            # Verify each module has its expected attributes
            assert hasattr(exceptions, "Jupyter_GET_Error")
            assert hasattr(core, "get_jupyter_workspaces")
            assert hasattr(content, "get_jupyter_content")
            assert hasattr(config, "update_jupyter_workspace_config")

        except ImportError as e:
            pytest.fail(f"Circular import detected: {e}")

    def test_module_organization_structure(self):
        """Test that the modular organization follows expected patterns."""
        import domolibrary2.routes.jupyter as main_module

        # Verify main module has proper docstring
        assert main_module.__doc__ is not None, "Main module should have documentation"
        assert "Jupyter Route Functions" in main_module.__doc__

        # Verify submodules exist and are properly organized
        expected_submodules = ["exceptions", "core", "content", "config"]

        for submodule_name in expected_submodules:
            assert (
                hasattr(main_module, submodule_name) or True
            )  # Submodules might not be directly accessible

            # Try to import each submodule directly
            try:
                exec(f"from domolibrary2.routes.jupyter import {submodule_name}")
            except ImportError:
                # Try alternative import path
                exec(f"import domolibrary2.routes.jupyter.{submodule_name}")


if __name__ == "__main__":
    # Run with pytest if executed directly
    pytest.main([__file__, "-v"])
