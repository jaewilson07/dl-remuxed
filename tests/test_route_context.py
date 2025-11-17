"""
Test RouteContext Pattern

This module tests the new RouteContext pattern to ensure backward compatibility
and proper context handling in route functions.
"""

import pytest
from domolibrary2.client.context import RouteContext


class TestRouteContext:
    """Test suite for RouteContext functionality."""

    def test_context_creation(self):
        """Test that RouteContext can be created with default values."""
        context = RouteContext()
        
        assert context.session is None
        assert context.debug_api is False
        assert context.debug_num_stacks_to_drop == 1
        assert context.parent_class is None

    def test_context_with_custom_values(self):
        """Test that RouteContext can be created with custom values."""
        context = RouteContext(
            debug_api=True,
            debug_num_stacks_to_drop=3,
            parent_class="TestClass",
        )
        
        assert context.debug_api is True
        assert context.debug_num_stacks_to_drop == 3
        assert context.parent_class == "TestClass"

    def test_context_to_dict(self):
        """Test that RouteContext can be converted to dictionary."""
        context = RouteContext(
            debug_api=True,
            debug_num_stacks_to_drop=2,
            parent_class="MyClass",
        )
        
        result = context.to_dict()
        
        assert isinstance(result, dict)
        assert result["session"] is None
        assert result["debug_api"] is True
        assert result["debug_num_stacks_to_drop"] == 2
        assert result["parent_class"] == "MyClass"


class TestJupyterRoutesWithContext:
    """Test suite for Jupyter routes with RouteContext pattern."""

    def test_jupyter_functions_accept_context_parameter(self):
        """Test that Jupyter route functions accept context parameter."""
        from domolibrary2.routes.jupyter.core import (
            get_jupyter_workspace_by_id,
            get_jupyter_workspaces,
            start_jupyter_workspace,
        )
        import inspect

        # Check that all three functions accept 'context' parameter
        for func in [
            get_jupyter_workspaces,
            get_jupyter_workspace_by_id,
            start_jupyter_workspace,
        ]:
            sig = inspect.signature(func)
            params = sig.parameters
            
            # Verify context parameter exists
            assert "context" in params, f"{func.__name__} should accept 'context' parameter"
            
            # Verify it's optional (has default value)
            assert (
                params["context"].default is None
            ), f"{func.__name__} context parameter should default to None"

    def test_backward_compatibility_parameters(self):
        """Test that functions still accept legacy parameters for backward compatibility."""
        from domolibrary2.routes.jupyter.core import (
            get_jupyter_workspace_by_id,
            get_jupyter_workspaces,
            start_jupyter_workspace,
        )
        import inspect

        legacy_params = ["session", "debug_api", "debug_num_stacks_to_drop", "parent_class"]

        for func in [
            get_jupyter_workspaces,
            get_jupyter_workspace_by_id,
            start_jupyter_workspace,
        ]:
            sig = inspect.signature(func)
            params = sig.parameters
            
            # Verify all legacy parameters still exist
            for param in legacy_params:
                assert param in params, f"{func.__name__} should still accept '{param}' parameter"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
