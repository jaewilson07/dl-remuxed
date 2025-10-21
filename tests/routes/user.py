"""
Tests for domolibrary2.routes.user module imports and functions.
"""

import inspect
import domolibrary2.client.auth as dmda
import domolibrary2.routes.user as user_routes
from dotenv import load_dotenv

load_dotenv()


class TestUserRoutesImport:
    """Test class for verifying user routes module imports and functionality."""

    def test_can_import_user_routes(self):
        """Test that we can successfully import domolibrary2.routes.user."""
        # This test passes if the import above doesn't raise an exception
        assert user_routes is not None
        assert hasattr(user_routes, "__name__")
        print("✅ Successfully imported domolibrary2.routes.user")

    def test_user_routes_contains_functions(self):
        """Test that user routes module contains callable functions."""
        # Get all members of the user_routes module
        members = inspect.getmembers(user_routes)

        # Filter for functions (excluding imported modules and private functions)
        functions = [
            (name, obj)
            for name, obj in members
            if inspect.isfunction(obj) and not name.startswith("_")
        ]

        # Assert we have at least one function
        assert (
            len(functions) > 0
        ), "user_routes module should contain at least one function"

        # Print found functions for visibility
        print(f"✅ Found {len(functions)} functions in domolibrary2.routes.user:")
        for name, func in functions:
            print(f"  - {name}()")

    def test_user_routes_has_expected_structure(self):
        """Test that user routes has the expected module structure."""
        # Check if it's a module
        assert inspect.ismodule(user_routes)

        # Check for common attributes that modules should have
        assert hasattr(user_routes, "__file__")
        assert hasattr(user_routes, "__name__")

        # Verify the module name is correct
        assert user_routes.__name__ == "domolibrary2.routes.user"

        print(f"✅ Module structure verified: {user_routes.__name__}")
        print(f"   File location: {user_routes.__file__}")

    def test_user_routes_functions_are_callable(self):
        """Test that all functions in user routes are callable."""
        members = inspect.getmembers(user_routes)
        functions = [
            (name, obj)
            for name, obj in members
            if inspect.isfunction(obj) and not name.startswith("_")
        ]

        for name, func in functions:
            assert callable(func), f"Function {name} should be callable"

        print(f"✅ All {len(functions)} functions are callable")

    def test_user_routes_function_signatures(self):
        """Test that user route functions have proper signatures."""
        members = inspect.getmembers(user_routes)
        functions = [
            (name, obj)
            for name, obj in members
            if inspect.isfunction(obj) and not name.startswith("_")
        ]

        signature_info = []
        for name, func in functions:
            try:
                sig = inspect.signature(func)
                signature_info.append(
                    {
                        "name": name,
                        "parameters": list(sig.parameters.keys()),
                        "return_annotation": sig.return_annotation,
                    }
                )
            except (ValueError, TypeError) as e:
                # Some functions might not have inspectable signatures
                signature_info.append({"name": name, "error": str(e)})

        assert (
            len(signature_info) > 0
        ), "Should be able to inspect at least one function signature"

        print(f"✅ Function signatures inspected:")
        for info in signature_info:
            if "error" in info:
                print(f"  - {info['name']}: Error - {info['error']}")
            else:
                params = ", ".join(info["parameters"])
                return_type = (
                    info["return_annotation"]
                    if info["return_annotation"] != inspect.Signature.empty
                    else "Any"
                )
                print(f"  - {info['name']}({params}) -> {return_type}")


if __name__ == "__main__":
    # Run tests manually for debugging
    test_class = TestUserRoutesImport()

    print("🧪 Running user routes import tests...")

    try:
        test_class.test_can_import_user_routes()
        test_class.test_user_routes_contains_functions()
        test_class.test_user_routes_has_expected_structure()
        test_class.test_user_routes_functions_are_callable()
        test_class.test_user_routes_function_signatures()

        print("\n🎉 All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
