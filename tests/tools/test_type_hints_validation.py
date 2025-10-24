"""
Test module to validate that all functions have proper type hints and return types.

This test can be used to validate any module's functions for complete type annotations.
"""

import inspect
from typing import get_type_hints

import pytest


def validate_function_type_hints(func, function_name: str = None):
    """
    Validate that a function has proper type hints for all parameters and return type.

    Args:
        func: Function to validate
        function_name: Optional name for better error messages

    Returns:
        tuple: (is_valid, issues) where issues is a list of missing type hints
    """
    function_name = function_name or func.__name__
    issues = []

    # Get function signature
    sig = inspect.signature(func)

    # Check return type annotation
    if sig.return_annotation == inspect.Signature.empty:
        issues.append("Missing return type annotation")

    # Check parameter type hints
    try:
        type_hints = get_type_hints(func)
    except (NameError, AttributeError) as e:
        issues.append(f"Error getting type hints: {e}")
        return False, issues

    for param_name, param in sig.parameters.items():
        # Skip 'self' and 'cls' parameters
        if param_name in ("self", "cls"):
            continue

        if param.annotation == inspect.Parameter.empty:
            issues.append(f"Parameter '{param_name}' missing type annotation")

    return len(issues) == 0, issues


def validate_module_type_hints(module, exclude_functions=None, include_private=False):
    """
    Validate type hints for all functions in a module.

    Args:
        module: The module to validate
        exclude_functions: List of function names to exclude from validation
        include_private: Whether to include private functions (starting with _)

    Returns:
        dict: Results with function names as keys and (is_valid, issues) as values
    """
    exclude_functions = exclude_functions or []
    results = {}

    # Get all functions from the module
    for name, obj in inspect.getmembers(module):
        # Skip if not a function
        if not inspect.isfunction(obj):
            continue

        # Skip if excluded
        if name in exclude_functions:
            continue

        # Skip private functions unless explicitly included
        if not include_private and name.startswith("_"):
            continue

        # Validate the function
        is_valid, issues = validate_function_type_hints(obj, name)
        results[name] = (is_valid, issues)

    return results


class TestTypeHintsValidation:
    """Test class for validating type hints in modules."""

    def test_user_attributes_type_hints(self):
        """Test that all functions in user.attributes module have proper type hints."""
        from domolibrary2.routes.instance_config import user_attributes

        # Functions that might be excluded (if any)
        exclude_functions = []

        results = validate_module_type_hints(
            user_attributes, exclude_functions=exclude_functions, include_private=False
        )

        # Collect all issues
        all_issues = {}
        for func_name, (is_valid, issues) in results.items():
            if not is_valid:
                all_issues[func_name] = issues

        # Assert no issues found
        if all_issues:
            error_msg = "Type hint validation failed:\n"
            for func_name, issues in all_issues.items():
                error_msg += f"\n{func_name}:\n"
                for issue in issues:
                    error_msg += f"  - {issue}\n"

            pytest.fail(error_msg)

        # Print success message
        print(
            f"\n✅ All {len(results)} functions in user.attributes have proper type hints!"
        )
        for func_name in results.keys():
            print(f"  ✅ {func_name}")

    def test_specific_function_type_hints(self):
        """Test specific functions have proper type hints."""
        from domolibrary2.routes.instance_config.user_attributes import (
            clean_attribute_id,
            create_user_attribute,
            delete_user_attribute,
            generate_create_user_attribute_body,
            get_user_attributes,
            update_user_attribute,
        )

        functions_to_test = [
            clean_attribute_id,
            generate_create_user_attribute_body,
            get_user_attributes,
            create_user_attribute,
            update_user_attribute,
            delete_user_attribute,
        ]

        for func in functions_to_test:
            is_valid, issues = validate_function_type_hints(func)

            if not is_valid:
                error_msg = f"Function {func.__name__} has type hint issues:\n"
                for issue in issues:
                    error_msg += f"  - {issue}\n"
                pytest.fail(error_msg)

        print(
            f"\n✅ All {len(functions_to_test)} tested functions have proper type hints!"
        )

    def test_return_type_annotations_exist(self):
        """Test that all functions have return type annotations."""
        from domolibrary2.routes.instance_config import user_attributes

        functions = [
            getattr(user_attributes, name)
            for name in dir(user_attributes)
            if callable(getattr(user_attributes, name)) and not name.startswith("_")
        ]

        functions_without_return_type = []

        for func in functions:
            if inspect.isfunction(func):
                sig = inspect.signature(func)
                if sig.return_annotation == inspect.Signature.empty:
                    functions_without_return_type.append(func.__name__)

        if functions_without_return_type:
            pytest.fail(
                f"Functions missing return type annotations: {functions_without_return_type}"
            )

        print("\n✅ All functions have return type annotations!")

    def test_parameter_type_annotations_exist(self):
        """Test that all function parameters have type annotations."""
        from domolibrary2.routes.instance_config import user_attributes

        functions = [
            getattr(user_attributes, name)
            for name in dir(user_attributes)
            if callable(getattr(user_attributes, name)) and not name.startswith("_")
        ]

        functions_with_missing_param_types = {}

        for func in functions:
            if inspect.isfunction(func):
                sig = inspect.signature(func)
                missing_params = []

                for param_name, param in sig.parameters.items():
                    # Skip 'self' and 'cls'
                    if param_name in ("self", "cls"):
                        continue

                    if param.annotation == inspect.Parameter.empty:
                        missing_params.append(param_name)

                if missing_params:
                    functions_with_missing_param_types[func.__name__] = missing_params

        if functions_with_missing_param_types:
            error_msg = "Functions with missing parameter type annotations:\n"
            for func_name, params in functions_with_missing_param_types.items():
                error_msg += f"  {func_name}: {params}\n"
            pytest.fail(error_msg)

        print("\n✅ All function parameters have type annotations!")


def main():
    """Run validation manually (for development/debugging)."""
    from domolibrary2.routes.instance_config import user_attributes

    print("🔍 Validating type hints in user.attributes module...\n")

    results = validate_module_type_hints(user_attributes)

    print(f"Found {len(results)} functions to validate:\n")

    all_valid = True
    for func_name, (is_valid, issues) in results.items():
        status = "✅" if is_valid else "❌"
        print(f"{status} {func_name}")

        if not is_valid:
            all_valid = False
            for issue in issues:
                print(f"    - {issue}")

        print()

    if all_valid:
        print("🎉 All functions have proper type hints!")
    else:
        print("⚠️  Some functions are missing type hints.")

    return all_valid


if __name__ == "__main__":
    main()
