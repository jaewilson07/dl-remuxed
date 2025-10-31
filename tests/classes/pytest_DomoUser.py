"""
Test file for DomoUser class validation and testing.
Tests core functionality following domolibrary2 design patterns.
"""

import os

import pytest
from dotenv import load_dotenv

import domolibrary2.classes.DomoUser as dmdu
import domolibrary2.client.auth as dmda

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


@pytest.mark.asyncio
async def test_domouser_structure():
    """Test that DomoUser class has proper structure and inheritance."""
    # Verify DomoUser inherits from DomoEntity
    from domolibrary2.entities.entities import DomoEntity

    assert issubclass(
        dmdu.DomoUser, DomoEntity
    ), "DomoUser should inherit from DomoEntity"

    # Verify DomoUsers inherits from DomoManager
    from domolibrary2.entities.entities import DomoManager

    assert issubclass(
        dmdu.DomoUsers, DomoManager
    ), "DomoUsers should inherit from DomoManager"

    # Verify required methods exist
    assert hasattr(dmdu.DomoUser, "get_by_id"), "DomoUser should have get_by_id method"
    assert hasattr(dmdu.DomoUser, "from_dict"), "DomoUser should have from_dict method"
    assert hasattr(
        dmdu.DomoUser, "display_url"
    ), "DomoUser should have display_url property"
    assert hasattr(
        dmdu.DomoUser, "__post_init__"
    ), "DomoUser should have __post_init__ method"


@pytest.mark.asyncio
async def test_domouser_get_by_id():
    """Test DomoUser.get_by_id() method with authenticated user."""
    # Get authenticated user's ID
    if not token_auth.user_id:
        await token_auth.who_am_i()

    user_id = token_auth.user_id
    assert user_id is not None, "User ID should be available after who_am_i"

    # Test get_by_id
    domo_user = await dmdu.DomoUser.get_by_id(
        user_id=user_id, auth=token_auth, return_raw=False
    )

    # Verify returned object
    assert domo_user is not None, "get_by_id should return a DomoUser object"
    assert isinstance(
        domo_user, dmdu.DomoUser
    ), "Returned object should be DomoUser instance"
    assert domo_user.id == str(user_id), "User ID should match"
    assert domo_user.auth == token_auth, "Auth should be set correctly"
    assert hasattr(domo_user, "raw"), "DomoUser should have raw attribute"
    assert isinstance(domo_user.raw, dict), "raw attribute should be a dict"


@pytest.mark.asyncio
async def test_domouser_get_by_id_return_raw():
    """Test DomoUser.get_by_id() with return_raw=True."""
    if not token_auth.user_id:
        await token_auth.who_am_i()

    user_id = token_auth.user_id

    # Test return_raw
    res = await dmdu.DomoUser.get_by_id(
        user_id=user_id, auth=token_auth, return_raw=True
    )

    # Verify response
    from domolibrary2.client.response import ResponseGetData

    assert isinstance(res, ResponseGetData), "return_raw should return ResponseGetData"
    assert res.is_success, "Response should be successful"


@pytest.mark.asyncio
async def test_domouser_from_dict():
    """Test DomoUser.from_dict() method."""
    # Sample user data
    user_data = {
        "id": "123456789",
        "displayName": "Test User",
        "emailAddress": "test@example.com",
        "title": "Test Title",
        "department": "Engineering",
        "roleId": 1,
        "avatarKey": "avatar-key-123",
        "created": 1609459200000,  # Epoch milliseconds
    }

    # Create DomoUser from dict
    domo_user = dmdu.DomoUser.from_dict(auth=token_auth, obj=user_data)

    # Verify attributes
    assert domo_user.id == "123456789", "ID should match"
    assert domo_user.display_name == "Test User", "Display name should match"
    assert domo_user.email_address == "test@example.com", "Email should match"
    assert domo_user.title == "Test Title", "Title should match"
    assert domo_user.department == "Engineering", "Department should match"
    assert domo_user.role_id == 1, "Role ID should match"
    assert domo_user.avatar_key == "avatar-key-123", "Avatar key should match"
    assert domo_user.created_dt is not None, "Created datetime should be set"
    assert domo_user.raw == user_data, "Raw data should be stored"


@pytest.mark.asyncio
async def test_domouser_display_url():
    """Test DomoUser.display_url property."""
    if not token_auth.user_id:
        await token_auth.who_am_i()

    user_id = token_auth.user_id
    domo_user = await dmdu.DomoUser.get_by_id(user_id=user_id, auth=token_auth)

    # Test display_url
    url = domo_user.display_url
    assert url is not None, "display_url should return a URL"
    assert isinstance(url, str), "display_url should return a string"
    assert token_auth.domo_instance in url, "URL should contain instance name"
    assert user_id in url, "URL should contain user ID"
    assert "admin/people" in url, "URL should be admin people URL"


@pytest.mark.asyncio
async def test_domouser_equality():
    """Test DomoUser.__eq__() method."""
    user_data = {
        "id": "123456789",
        "displayName": "Test User",
        "emailAddress": "test@example.com",
    }

    user1 = dmdu.DomoUser.from_dict(auth=token_auth, obj=user_data)
    user2 = dmdu.DomoUser.from_dict(auth=token_auth, obj=user_data)

    # Same ID should be equal
    assert user1 == user2, "Users with same ID should be equal"

    # Different ID should not be equal
    user_data2 = {**user_data, "id": "987654321"}
    user3 = dmdu.DomoUser.from_dict(auth=token_auth, obj=user_data2)
    assert user1 != user3, "Users with different IDs should not be equal"


@pytest.mark.asyncio
async def test_domousers_manager_structure():
    """Test DomoUsers manager class structure."""
    # Create manager instance
    domo_users = dmdu.DomoUsers(auth=token_auth)

    # Verify attributes
    assert domo_users.auth == token_auth, "Auth should be set"
    assert hasattr(domo_users, "get"), "Manager should have get method"
    assert hasattr(
        domo_users, "search_by_email"
    ), "Manager should have search_by_email method"
    assert hasattr(
        domo_users, "search_by_id"
    ), "Manager should have search_by_id method"


@pytest.mark.asyncio
async def test_domousers_search_by_email():
    """Test DomoUsers.search_by_email() method."""
    if not token_auth.user_id:
        await token_auth.who_am_i()

    # Get current user first to know their email
    current_user = await dmdu.DomoUser.get_by_id(
        user_id=token_auth.user_id, auth=token_auth
    )

    if current_user.email_address:
        # Test search by email
        domo_users = dmdu.DomoUsers(auth=token_auth)
        found_user = await domo_users.search_by_email(
            email=current_user.email_address,
            only_allow_one=True,
            suppress_no_results_error=False,
        )

        # Verify result
        assert found_user is not None, "Search should find the user"
        assert isinstance(found_user, dmdu.DomoUser), "Should return DomoUser instance"
        assert (
            found_user.email_address == current_user.email_address
        ), "Email should match"


@pytest.mark.asyncio
async def test_domousers_search_by_id():
    """Test DomoUsers.search_by_id() method."""
    if not token_auth.user_id:
        await token_auth.who_am_i()

    user_id = token_auth.user_id

    # Test search by ID
    domo_users = dmdu.DomoUsers(auth=token_auth)
    found_user = await domo_users.search_by_id(
        user_ids=[user_id], only_allow_one=True, suppress_no_results_error=False
    )

    # Verify result
    assert found_user is not None, "Search should find the user"
    assert isinstance(found_user, dmdu.DomoUser), "Should return DomoUser instance"
    assert found_user.id == str(user_id), "User ID should match"


@pytest.mark.asyncio
async def test_exception_handling():
    """Test that proper exceptions are raised for invalid operations."""
    # Test with invalid user ID
    invalid_user_id = "999999999999"

    domo_user = await dmdu.DomoUser.get_by_id(
        user_id=invalid_user_id, auth=token_auth, return_raw=False
    )

    # get_by_id returns None for non-existent users (not an exception)
    assert domo_user is None, "get_by_id should return None for non-existent user"


@pytest.mark.asyncio
async def test_exception_imports():
    """Test that exceptions are properly imported from route modules."""
    # Verify exceptions are available
    assert hasattr(dmdu, "User_GET_Error"), "User_GET_Error should be exported"
    assert hasattr(dmdu, "User_CRUD_Error"), "User_CRUD_Error should be exported"
    assert hasattr(
        dmdu, "SearchUserNotFoundError"
    ), "SearchUserNotFoundError should be exported"
    assert hasattr(dmdu, "DeleteUserError"), "DeleteUserError should be exported"

    # Verify they're from the route module
    from domolibrary2.routes.user.exceptions import RouteError

    assert issubclass(
        dmdu.User_GET_Error, RouteError
    ), "User_GET_Error should inherit from RouteError"
    assert issubclass(
        dmdu.User_CRUD_Error, RouteError
    ), "User_CRUD_Error should inherit from RouteError"


@pytest.mark.asyncio
async def test_all_exports():
    """Test that __all__ exports are complete."""
    # Check that key classes and exceptions are in __all__
    assert "DomoUser" in dmdu.__all__, "DomoUser should be in __all__"
    assert "DomoUsers" in dmdu.__all__, "DomoUsers should be in __all__"
    assert "User_GET_Error" in dmdu.__all__, "User_GET_Error should be in __all__"
    assert "User_CRUD_Error" in dmdu.__all__, "User_CRUD_Error should be in __all__"
    assert (
        "SearchUserNotFoundError" in dmdu.__all__
    ), "SearchUserNotFoundError should be in __all__"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
