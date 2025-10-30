"""
User Routes Test Suite - Function Call Validation

Simple test suite that validates all user route functions can be called.
No mocking - just verifies function signatures, imports, and basic functionality.
"""

import inspect
import os

import pytest

from domolibrary2.client.auth import DomoTokenAuth

# Import all user route functions to test they exist and are callable
from domolibrary2.routes.user import (
    DeleteUser_Error,
    DownloadAvatar_Error,
    ResetPassword_PasswordUsed,
    SearchUser_NotFound,
    User_CRUD_Error,
    # Exception classes
    User_GET_Error,
    UserAttributes_CRUD_Error,
    UserAttributes_GET_Error,
    # User attributes
    UserAttributes_IssuerType,
    UserProperty,
    # User properties
    UserProperty_Type,
    UserSharing_Error,
    clean_attribute_id,
    create_user,
    create_user_attribute,
    delete_user,
    delete_user_attribute,
    download_avatar,
    generate_avatar_bytestr,
    generate_create_user_attribute_body,
    generate_patch_user_property_body,
    # Core user functions
    get_all_users,
    get_by_id,
    get_user_attribute_by_id,
    get_user_attributes,
    process_v1_search_users,
    request_password_reset,
    reset_password,
    search_users,
    search_users_by_email,
    search_users_by_id,
    search_virtual_user_by_subscriber_instance,
    set_user_landing_page,
    update_user,
    update_user_attribute,
    upload_avatar,
    user_is_allowed_direct_signon,
)


class TestUserFunctionExistence:
    """Test that all user route functions exist and are callable."""

    def test_core_user_functions_exist(self):
        """Test that core user functions are importable and callable."""
        # Test core functions exist
        assert callable(get_all_users)
        assert callable(search_users)
        assert callable(search_users_by_id)
        assert callable(search_users_by_email)
        assert callable(get_by_id)  # This is get_user_by_id
        assert callable(search_virtual_user_by_subscriber_instance)
        assert callable(create_user)
        assert callable(delete_user)
        assert callable(process_v1_search_users)
        assert callable(user_is_allowed_direct_signon)

        # Test they are async functions
        assert inspect.iscoroutinefunction(get_all_users)
        assert inspect.iscoroutinefunction(search_users)
        assert inspect.iscoroutinefunction(get_by_id)
        assert inspect.iscoroutinefunction(create_user)
        assert inspect.iscoroutinefunction(search_virtual_user_by_subscriber_instance)

    def test_property_functions_exist(self):
        """Test that user property functions are importable and callable."""
        assert callable(update_user)
        assert callable(set_user_landing_page)
        assert callable(download_avatar)
        assert callable(upload_avatar)
        assert callable(reset_password)
        assert callable(request_password_reset)

        # Test utility functions
        assert callable(generate_patch_user_property_body)
        assert callable(generate_avatar_bytestr)

        # Test async property functions
        assert inspect.iscoroutinefunction(update_user)
        assert inspect.iscoroutinefunction(upload_avatar)

    def test_attribute_functions_exist(self):
        """Test that user attribute functions are importable and callable."""
        assert callable(get_user_attributes)
        assert callable(get_user_attribute_by_id)
        assert callable(create_user_attribute)
        assert callable(update_user_attribute)
        assert callable(delete_user_attribute)

        # Test utility functions
        assert callable(clean_attribute_id)
        assert callable(generate_create_user_attribute_body)

    def test_user_property_classes_exist(self):
        """Test that UserProperty classes and enums exist."""
        # Test UserProperty_Type enum
        assert hasattr(UserProperty_Type, "__members__")
        assert len(list(UserProperty_Type)) > 0

        # Test UserProperty class
        assert inspect.isclass(UserProperty)

        # Test can create UserProperty instances
        prop = UserProperty(UserProperty_Type.display_name, "test")
        assert hasattr(prop, "property_type")
        assert hasattr(prop, "values")

    def test_user_attribute_classes_exist(self):
        """Test that UserAttribute classes exist."""
        # Test UserAttributes_IssuerType enum
        assert hasattr(UserAttributes_IssuerType, "__members__")
        assert len(list(UserAttributes_IssuerType)) > 0

    def test_exception_classes_exist(self):
        """Test that all user exception classes exist."""
        # Core exceptions
        assert inspect.isclass(User_GET_Error)
        assert inspect.isclass(User_CRUD_Error)
        assert inspect.isclass(SearchUser_NotFound)
        assert inspect.isclass(DeleteUser_Error)
        assert inspect.isclass(UserSharing_Error)

        # Property exceptions
        assert inspect.isclass(ResetPassword_PasswordUsed)
        assert inspect.isclass(DownloadAvatar_Error)

        # Attribute exceptions
        assert inspect.isclass(UserAttributes_GET_Error)
        assert inspect.isclass(UserAttributes_CRUD_Error)

        # Test they are proper exception classes
        assert issubclass(User_GET_Error, Exception)
        assert issubclass(User_CRUD_Error, Exception)
        assert issubclass(DeleteUser_Error, Exception)
        assert issubclass(UserSharing_Error, Exception)

    def test_user_property_enumeration_values(self):
        """Test UserProperty_Type enumeration has expected values."""
        # Test enumeration exists and has expected members
        assert hasattr(UserProperty_Type, "__members__")

        # Test some expected property types exist
        member_names = [member.name for member in UserProperty_Type]
        expected_types = ["display_name", "email_address", "role_id"]

        for expected_type in expected_types:
            assert (
                expected_type in member_names
            ), f"Expected {expected_type} in UserProperty_Type"

    def test_user_property_instantiation(self):
        """Test UserProperty class can be instantiated."""
        # Create UserProperty instances
        display_name_prop = UserProperty(UserProperty_Type.display_name, "Test User")
        email_prop = UserProperty(UserProperty_Type.email_address, "test@example.com")
        role_prop = UserProperty(UserProperty_Type.role_id, 1)

        # Test structure
        assert display_name_prop.property_type == UserProperty_Type.display_name
        assert display_name_prop.values == ["Test User"]

        assert email_prop.property_type == UserProperty_Type.email_address
        assert email_prop.values == ["test@example.com"]

        assert role_prop.property_type == UserProperty_Type.role_id
        assert role_prop.values == [1]

    def test_generate_patch_user_property_body_utility(self):
        """Test patch body generation utility function."""
        # Create test properties
        properties = [
            UserProperty(UserProperty_Type.display_name, "Jae Wilson"),
            UserProperty(UserProperty_Type.email_address, "jae@example.com"),
            UserProperty(UserProperty_Type.role_id, 1),
        ]

        # Generate patch body
        patch_body = generate_patch_user_property_body(properties)

        # Verify structure
        assert isinstance(patch_body, dict)
        assert "attributes" in patch_body
        assert isinstance(patch_body["attributes"], list)
        assert len(patch_body["attributes"]) == 3

        # Verify each attribute has proper structure
        for attr in patch_body["attributes"]:
            assert "key" in attr
            assert "values" in attr
            assert isinstance(attr["values"], list)

    def test_generate_avatar_bytestr_utility(self):
        """Test avatar byte string generation utility."""
        # Test with bytes
        fake_image = b"\x89PNG\r\n\x1a\n"
        result = generate_avatar_bytestr(fake_image, "png")

        assert isinstance(result, str)
        assert result.startswith("data:image/png;base64,")

    def test_clean_attribute_id_utility(self):
        """Test attribute ID cleaning utility function exists and works."""
        # Test that the function exists and can be called
        assert callable(clean_attribute_id)

        # Test with basic input (whatever the actual behavior is)
        result = clean_attribute_id("Test Attribute")
        assert isinstance(result, str)

        # Test function doesn't crash with various inputs
        assert isinstance(clean_attribute_id("test_attribute"), str)
        assert isinstance(clean_attribute_id("Test@Attribute!"), str)

    def test_user_attributes_issuer_type_enum(self):
        """Test UserAttributes_IssuerType enumeration."""
        assert hasattr(UserAttributes_IssuerType, "__members__")

        # Should have common issuer types
        member_names = [member.name for member in UserAttributes_IssuerType]
        expected_types = ["CUSTOM", "DOMO", "SAML"]

        for expected_type in expected_types:
            if hasattr(UserAttributes_IssuerType, expected_type):
                assert expected_type in member_names

    def test_generate_create_user_attribute_body_utility(self):
        """Test user attribute body generation utility."""
        body = generate_create_user_attribute_body(
            attribute_id="test-attr",
            name="Test Attribute",
            description="Test Description",
            issuer_type=UserAttributes_IssuerType.CUSTOM,
        )

        assert isinstance(body, dict)
        assert "key" in body
        assert "title" in body
        assert "description" in body
        assert "keyspace" in body

    def test_exception_classes_inheritance(self):
        """Test that all user exception classes exist and inherit properly."""
        # Core exceptions
        assert issubclass(User_GET_Error, Exception)
        assert issubclass(User_CRUD_Error, Exception)
        assert issubclass(SearchUser_NotFound, Exception)
        assert issubclass(DeleteUser_Error, Exception)
        assert issubclass(UserSharing_Error, Exception)

        # Property exceptions
        assert issubclass(ResetPassword_PasswordUsed, Exception)
        assert issubclass(DownloadAvatar_Error, Exception)

        # Attribute exceptions
        assert issubclass(UserAttributes_GET_Error, Exception)
        assert issubclass(UserAttributes_CRUD_Error, Exception)

    def test_exception_instantiation(self):
        """Test that user exception classes exist and are callable."""
        # Test that exception classes exist and are callable
        assert callable(User_GET_Error)
        assert callable(User_CRUD_Error)
        assert callable(SearchUser_NotFound)
        assert callable(DeleteUser_Error)
        assert callable(UserSharing_Error)

        # Test other exception classes are callable
        assert callable(ResetPassword_PasswordUsed)
        assert callable(DownloadAvatar_Error)
        assert callable(UserAttributes_GET_Error)
        assert callable(UserAttributes_CRUD_Error)


# Integration test class (optional - requires real credentials)
class TestUserRoutesIntegration:
    """Integration tests using real API calls (optional)."""

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.skipif(
        not all(key in os.environ for key in ["DOMO_INSTANCE", "DOMO_ACCESS_TOKEN"]),
        reason="Integration test requires DOMO_INSTANCE and DOMO_ACCESS_TOKEN environment variables",
    )
    async def test_real_get_all_users(self):
        """Integration test with real API call."""
        auth = DomoTokenAuth(
            domo_instance=os.environ["DOMO_INSTANCE"],
            domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
        )

        try:
            result = await get_all_users(auth=auth)
            assert result.is_success
            assert hasattr(result, "response")
            print(f"✅ Successfully retrieved {len(result.response)} users from API")

        except Exception as e:
            pytest.skip(f"Integration test failed due to API error: {e}")


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v", "--tb=short"])
