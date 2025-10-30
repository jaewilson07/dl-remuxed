"""
Comprehensive tests for domolibrary2.routes.user module using test harness.

This module tests all user route functions including:
- Core user operations (get, search, create, update, delete)
- User attributes management
- User properties and configuration
"""

import inspect
from typing import list
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

# Import user route functions and exceptions
import domolibrary2.routes.user as user_routes
from domolibrary2.routes.user import (
    SearchUser_NotFound,
    create_user_attribute,
    get_by_id,
    get_user_attributes,
    reset_password,
    search_users_by_id,
    # Property functions
    set_user_landing_page,
)

# Import test harness utilities
from ..tools.test_harness import (
    PytestRouteTestCase,
)

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

        print("✅ Function signatures inspected:")
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


class TestUserCoreRoutes(PytestRouteTestCase):
    """Test core user route functions using test harness."""

    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            "id": "12345678",
            "name": "Test User",
            "email": "test.user@example.com",
            "displayName": "Test User",
            "department": "Engineering",
            "title": "Software Engineer",
            "active": True,
        }

    @pytest.fixture
    def sample_users_list(self, sample_user_data):
        """Sample list of users for testing."""
        return [
            sample_user_data,
            {
                "id": "87654321",
                "name": "Another User",
                "email": "another.user@example.com",
                "displayName": "Another User",
                "department": "Marketing",
                "title": "Marketing Manager",
                "active": True,
            },
        ]

    def test_get_all_users_sync(self, harness, sample_users_list):
        """Test get_all_users function with mocked async behavior."""
        with patch("domolibrary2.routes.user.get_all_users") as mock_func:
            # Mock the async function to return expected data
            mock_func.return_value = harness.create_response_get_data(
                status=200, res=sample_users_list, is_success=True
            )

            # Test the mock works
            result = mock_func(auth=harness.default_auth)

            assert result is not None
            assert result.is_success
            assert result.response == sample_users_list

            # Verify function was called with correct parameters
            mock_func.assert_called_once_with(auth=harness.default_auth)
            call_args = mock_func.call_args
            assert call_args[1]["auth"] == harness.default_auth
            assert "method" in call_args[1]
            assert "url" in call_args[1]

    @pytest.mark.asyncio
    async def test_search_users_by_id(self, harness, sample_user_data):
        """Test search_users_by_id function."""
        with patch("domolibrary2.routes.user.core.gd.get_data") as mock_get_data:
            mock_get_data.return_value = harness.create_response_get_data(
                status=200, res=[sample_user_data], is_success=True
            )

            # Test successful search
            result = await search_users_by_id(
                auth=harness.default_auth, user_id_ls=["12345678"]
            )

            assert result is not None
            assert result.is_success
            assert isinstance(result.response, list)

    @pytest.mark.asyncio
    async def test_get_by_id(self, harness, sample_user_data):
        """Test get_by_id function."""
        with patch("domolibrary2.routes.user.core.gd.get_data") as mock_get_data:
            mock_get_data.return_value = harness.create_response_get_data(
                status=200, res=sample_user_data, is_success=True
            )

            # Test successful get by ID
            result = await get_by_id(auth=harness.default_auth, user_id="12345678")

            assert result is not None
            assert result.is_success
            assert result.response == sample_user_data

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, harness):
        """Test get_by_id function with not found scenario."""
        with patch("domolibrary2.routes.user.core.gd.get_data") as mock_get_data:
            mock_get_data.return_value = harness.create_response_get_data(
                status=404, res={"error": "User not found"}, is_success=False
            )

            # Test not found scenario
            with pytest.raises(SearchUser_NotFound):
                await get_by_id(auth=harness.default_auth, user_id="nonexistent")


class TestUserAttributeRoutes(PytestRouteTestCase):
    """Test user attribute route functions."""

    @pytest.fixture
    def sample_attribute_data(self):
        """Sample user attribute data for testing."""
        return {
            "id": "attr-123",
            "name": "Department",
            "type": "TEXT",
            "issuerType": "DOMO",
            "values": ["Engineering", "Marketing", "Sales"],
        }

    @pytest.mark.asyncio
    async def test_get_user_attributes(self, harness, sample_attribute_data):
        """Test get_user_attributes function."""
        with patch("domolibrary2.routes.user.attributes.gd.get_data") as mock_get_data:
            mock_get_data.return_value = harness.create_response_get_data(
                status=200, res=[sample_attribute_data], is_success=True
            )

            # Test successful retrieval
            result = await get_user_attributes(auth=harness.default_auth)

            assert result is not None
            assert result.is_success
            assert isinstance(result.response, list)

    @pytest.mark.asyncio
    async def test_create_user_attribute(self, harness, sample_attribute_data):
        """Test create_user_attribute function."""
        with patch("domolibrary2.routes.user.attributes.gd.get_data") as mock_get_data:
            mock_get_data.return_value = harness.create_response_get_data(
                status=201, res=sample_attribute_data, is_success=True
            )

            # Test successful creation
            result = await create_user_attribute(
                auth=harness.default_auth, name="Test Attribute", attribute_type="TEXT"
            )

            assert result is not None
            assert result.is_success


class TestUserPropertyRoutes(PytestRouteTestCase):
    """Test user property route functions."""

    @pytest.mark.asyncio
    async def test_set_user_landing_page(self, harness):
        """Test set_user_landing_page function."""
        with patch("domolibrary2.routes.user.properties.gd.get_data") as mock_get_data:
            mock_get_data.return_value = harness.create_response_get_data(
                status=200, res={"success": True}, is_success=True
            )

            # Test successful landing page update
            result = await set_user_landing_page(
                auth=harness.default_auth, user_id="12345678", page_id="98765432"
            )

            assert result is not None
            assert result.is_success

    @pytest.mark.asyncio
    async def test_reset_password(self, harness):
        """Test reset_password function."""
        with patch("domolibrary2.routes.user.properties.gd.get_data") as mock_get_data:
            mock_get_data.return_value = harness.create_response_get_data(
                status=200,
                res={"success": True, "temporaryPassword": "temp123"},
                is_success=True,
            )

            # Test successful password reset
            result = await reset_password(
                auth=harness.default_auth, user_id="12345678", password="newpassword123"
            )

            assert result is not None
            assert result.is_success


def test_user_route_module_completeness():
    """Test that the user routes module exports all expected items."""
    expected_exports = [
        # Core functions
        "get_all_users",
        "search_users",
        "search_users_by_id",
        "search_users_by_email",
        "get_by_id",
        "create_user",
        # Attribute functions
        "get_user_attributes",
        "get_user_attribute_by_id",
        "create_user_attribute",
        "update_user_attribute",
        # Property functions
        "set_user_landing_page",
        "reset_password",
        "request_password_reset",
        "download_avatar",
        "upload_avatar",
        # Exception classes
        "User_GET_Error",
        "User_CRUD_Error",
        "SearchUser_NotFound",
        "UserSharing_Error",
        "UserAttributes_GET_Error",
        "UserAttributes_CRUD_Error",
    ]

    missing_exports = []
    for export in expected_exports:
        if not hasattr(user_routes, export):
            missing_exports.append(export)

    assert not missing_exports, f"Missing exports: {missing_exports}"
    print(f"✅ All {len(expected_exports)} expected exports are present")


if __name__ == "__main__":
    # Run tests manually for debugging
    print("🧪 Running user routes comprehensive tests...")

    # Run basic import tests
    test_class = TestUserRoutesImport()
    test_class.test_can_import_user_routes()
    test_class.test_user_routes_contains_functions()
    test_class.test_user_routes_has_expected_structure()
    test_class.test_user_routes_functions_are_callable()
    test_class.test_user_routes_function_signatures()

    # Test module completeness
    test_user_route_module_completeness()

    print("\n🎉 Basic tests completed successfully!")
    print("\nTo run full async tests, use: pytest tests/routes/user.py -v")
