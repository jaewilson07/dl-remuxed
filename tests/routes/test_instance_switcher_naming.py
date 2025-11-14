"""
Unit tests for instance_config_instance_switcher.py naming convention compliance.

Tests verify:
- Error class naming follows conventions
- Error classes have proper constructors
- Functions have return_raw parameter
- Type hints are complete
"""

import inspect
from typing import get_type_hints

import pytest
from domolibrary2.routes.instance_config_instance_switcher import (
    InstanceSwitcher_CRUD_Error,
    InstanceSwitcher_GET_Error,
    get_instance_switcher_mapping,
    set_instance_switcher_mapping,
)


class TestErrorClassNaming:
    """Test error class naming conventions."""

    def test_get_error_class_exists(self):
        """Verify InstanceSwitcher_GET_Error class exists."""
        assert InstanceSwitcher_GET_Error is not None
        assert InstanceSwitcher_GET_Error.__name__ == "InstanceSwitcher_GET_Error"

    def test_crud_error_class_exists(self):
        """Verify InstanceSwitcher_CRUD_Error class exists."""
        assert InstanceSwitcher_CRUD_Error is not None
        assert InstanceSwitcher_CRUD_Error.__name__ == "InstanceSwitcher_CRUD_Error"

    def test_get_error_constructor(self):
        """Verify GET error has standardized constructor."""
        sig = inspect.signature(InstanceSwitcher_GET_Error.__init__)
        params = list(sig.parameters.keys())

        # Should have: self, entity_id, res, message, **kwargs
        assert "entity_id" in params
        assert "res" in params
        assert "message" in params
        assert "kwargs" in params

    def test_crud_error_constructor(self):
        """Verify CRUD error has standardized constructor."""
        sig = inspect.signature(InstanceSwitcher_CRUD_Error.__init__)
        params = list(sig.parameters.keys())

        # Should have: self, operation, entity_id, res, message, **kwargs
        assert "operation" in params
        assert "entity_id" in params
        assert "res" in params
        assert "message" in params
        assert "kwargs" in params


class TestFunctionSignatures:
    """Test function signature compliance."""

    def test_get_function_has_return_raw(self):
        """Verify get_instance_switcher_mapping has return_raw parameter."""
        sig = inspect.signature(get_instance_switcher_mapping)
        params = sig.parameters

        assert "return_raw" in params
        assert params["return_raw"].default is False

    def test_set_function_has_return_raw(self):
        """Verify set_instance_switcher_mapping has return_raw parameter."""
        sig = inspect.signature(set_instance_switcher_mapping)
        params = sig.parameters

        assert "return_raw" in params
        assert params["return_raw"].default is False

    def test_get_function_parameter_order(self):
        """Verify parameter order follows standard pattern."""
        sig = inspect.signature(get_instance_switcher_mapping)
        params = list(sig.parameters.keys())

        # auth should be first
        assert params[0] == "auth"

        # return_raw should be before timeout (control params at end)
        return_raw_idx = params.index("return_raw")
        timeout_idx = params.index("timeout")
        assert return_raw_idx < timeout_idx

    def test_set_function_parameter_order(self):
        """Verify parameter order follows standard pattern."""
        sig = inspect.signature(set_instance_switcher_mapping)
        params = list(sig.parameters.keys())

        # auth should be first
        assert params[0] == "auth"

        # mapping_payloads should be second (entity parameter)
        assert params[1] == "mapping_payloads"

        # return_raw should be before timeout (control params at end)
        return_raw_idx = params.index("return_raw")
        timeout_idx = params.index("timeout")
        assert return_raw_idx < timeout_idx


class TestTypeHints:
    """Test type hint completeness."""

    def test_get_function_type_hints(self):
        """Verify get_instance_switcher_mapping has complete type hints."""
        hints = get_type_hints(get_instance_switcher_mapping)

        # Should have type hints for key parameters
        assert "auth" in hints
        assert "return_raw" in hints
        assert "return" in hints

    def test_set_function_type_hints(self):
        """Verify set_instance_switcher_mapping has complete type hints."""
        hints = get_type_hints(set_instance_switcher_mapping)

        # Should have type hints for key parameters
        assert "auth" in hints
        assert "mapping_payloads" in hints
        assert "return_raw" in hints
        assert "return" in hints

    def test_mapping_payloads_uses_builtin_list(self):
        """Verify mapping_payloads uses built-in list type hint."""
        hints = get_type_hints(set_instance_switcher_mapping)
        mapping_payloads_hint = str(hints.get("mapping_payloads", ""))

        # Should use list[dict] not list[dict]
        assert "list" in mapping_payloads_hint.lower()


class TestDocstrings:
    """Test documentation completeness."""

    def test_get_function_has_docstring(self):
        """Verify get_instance_switcher_mapping has docstring."""
        assert get_instance_switcher_mapping.__doc__ is not None
        assert len(get_instance_switcher_mapping.__doc__) > 0

        # Should document return_raw parameter
        assert "return_raw" in get_instance_switcher_mapping.__doc__

    def test_set_function_has_docstring(self):
        """Verify set_instance_switcher_mapping has docstring."""
        assert set_instance_switcher_mapping.__doc__ is not None
        assert len(set_instance_switcher_mapping.__doc__) > 0

        # Should document return_raw parameter
        assert "return_raw" in set_instance_switcher_mapping.__doc__

    def test_get_error_has_docstring(self):
        """Verify InstanceSwitcher_GET_Error has docstring."""
        assert InstanceSwitcher_GET_Error.__doc__ is not None
        assert len(InstanceSwitcher_GET_Error.__doc__) > 0

    def test_crud_error_has_docstring(self):
        """Verify InstanceSwitcher_CRUD_Error has docstring."""
        assert InstanceSwitcher_CRUD_Error.__doc__ is not None
        assert len(InstanceSwitcher_CRUD_Error.__doc__) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
