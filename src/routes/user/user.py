"""
Core User Management Routes

This module provides core user management functionality including retrieval,
creation, updates, deletion, and search operations.

Functions:
    get_all_users: Retrieve all users
    search_users: Search users with flexible criteria
    search_users_by_id: Search users by ID list
    search_users_by_email: Search users by email list
    get_by_id: Retrieve specific user by ID
    search_virtual_user_by_subscriber_instance: Find virtual users
    create_user: Create new user
    set_user_landing_page: Set user's landing page
    reset_password: Reset user password
    request_password_reset: Request password reset
    delete_user: Delete user
    user_is_allowed_direct_signon: Manage direct sign-on permissions
    download_avatar: Download user avatar
    upload_avatar: Upload user avatar
    generate_avatar_bytestr: Generate avatar byte string

Exception Classes:
    User_GET_Error: Raised when user retrieval fails
    User_CRUD_Error: Raised when user create/update/delete operations fail
    SearchUser_NotFound: Raised when user search returns no results
    UserSharing_Error: Raised when user sharing operations fail
    ResetPassword_PasswordUsed: Raised when password was previously used
    DownloadAvatar_Error: Raised when avatar download fails
    DeleteUser_Error: Raised when user deletion fails
"""

__all__ = [
    "User_GET_Error",
    "User_CRUD_Error", 
    "SearchUser_NotFound",
    "UserSharing_Error",
    "ResetPassword_PasswordUsed",
    "DownloadAvatar_Error",
    "DeleteUser_Error",
    "get_all_users",
    "search_users",
    "search_users_by_id",
    "search_users_by_email",
    "get_by_id",
    "search_virtual_user_by_subscriber_instance",
    "create_user",
    "set_user_landing_page",
    "reset_password",
    "request_password_reset",
    "delete_user",
    "user_is_allowed_direct_signon",
    "download_avatar",
    "generate_avatar_bytestr",
    "upload_avatar",
    "process_v1_search_users",
]

import asyncio
import base64
import os
from typing import List, Optional

import httpx

from ...client.auth import DomoAuth
from ...client.exceptions import RouteError
from ...client import get_data as gd
from ...client import response as rgd
from ...utils import chunk_execution as ce
from ...utils import Image as uimg
from ...utils.convert import test_valid_email


class User_GET_Error(RouteError):
    """Raised when user retrieval operations fail."""

    def __init__(self, user_id: Optional[str] = None, res=None, **kwargs):
        super().__init__(
            message="User retrieval failed",
            entity_id=user_id,
            res=res,
            **kwargs,
        )


class User_CRUD_Error(RouteError):
    """Raised when user create, update, or delete operations fail."""

    def __init__(
        self,
        operation: str,
        user_id: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        message = f"User {operation} operation failed"
        super().__init__(message=message, entity_id=user_id, res=res, **kwargs)


class SearchUser_NotFound(RouteError):
    """Raised when user search operations return no results."""

    def __init__(self, search_criteria: str, res=None, **kwargs):
        message = f"No users found matching: {search_criteria}"
        super().__init__(
            message=message,
            res=res,
            **kwargs,
        )


class UserSharing_Error(RouteError):
    """Raised when user sharing operations fail."""

    def __init__(
        self,
        operation: str,
        user_id: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        message = f"User sharing {operation} failed"
        super().__init__(message=message, entity_id=user_id, res=res, **kwargs)


class ResetPassword_PasswordUsed(RouteError):
    """Raised when attempting to reset password to a previously used password."""

    def __init__(self, user_id: Optional[str] = None, res=None, **kwargs):
        super().__init__(
            message="Password has been used previously",
            entity_id=user_id,
            res=res,
            **kwargs,
        )


class DownloadAvatar_Error(RouteError):
    """Raised when user avatar download operations fail."""

    def __init__(self, user_id: str, res=None, **kwargs):
        message = f"Unable to download avatar for user {user_id}"
        super().__init__(message=message, entity_id=user_id, res=res, **kwargs)


class DeleteUser_Error(RouteError):
    """Raised when user deletion operations fail."""

    def __init__(
        self,
        res: rgd.ResponseGetData,
        message: str = None,
        entity_id=None,
    ):
        super().__init__(
            res=res,
            message=message,
            entity_id=entity_id,
        )


def process_v1_search_users(
    v1_user_ls: list[dict],  # list of users from v1_users_search API
) -> list[dict]:  # sanitized list of users.
    """sanitizes the response from v1_users_search API and removes unecessary attributes"""

    clean_users = []

    for obj in v1_user_ls:
        # dd_user = dd.DictDot(obj_user)

        attributes = obj.pop("attributes")

        clean_users.append(
            {**obj, **{attr["key"]: attr["values"][0] for attr in attributes}}
        )

    return clean_users


@gd.route_function
async def get_all_users(
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve all users from Domo instance.

    Args:
        auth: Authentication object
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing all users

    Raises:
        User_GET_Error: If user retrieval fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/content/v2/users"

    res = await gd.get_data(
        url=url,
        method="GET",
        auth=auth,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_GET_Error(res=res)

    return res


@gd.route_function
async def search_users(
    auth: DomoAuth,
    body: dict,
    loop_until_end: bool = True,  # retrieve all available rows
    limit=200,  # maximum rows to return per request.  refers to PAGINATION
    maximum=100,  # equivalent to the LIMIT or TOP clause in SQL, the number of rows to return total
    suppress_no_results_error: bool = False,
    debug_api: bool = False,
    return_raw: bool = False,
    debug_loop: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: Optional[httpx.AsyncClient] = None,
) -> rgd.ResponseGetData:
    """Search users with flexible criteria using the v1 users search API.

    Args:
        auth: Authentication object
        body: Search criteria body for the API request
        loop_until_end: Retrieve all available rows across all pages
        limit: Maximum rows to return per request (pagination)
        maximum: Maximum total rows to return (like SQL LIMIT)
        suppress_no_results_error: Don't raise error if no results found
        debug_api: Enable API debugging
        return_raw: Return raw API response without processing
        debug_loop: Enable loop debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        session: HTTP client session

    Returns:
        ResponseGetData object containing search results

    Raises:
        User_GET_Error: If search request fails
        SearchUser_NotFound: If no users found and suppress_no_results_error is False
    """
    url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/users/search"

    offset_params = {"offset": "offset", "limit": "limit"}

    def body_fn(skip, limit, body):
        return {**body, "limit": limit, "offset": skip}

    def arr_fn(res: rgd.ResponseGetData):
        return res.response.get("users")

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        maximum=maximum,
        limit=limit,
        offset_params=offset_params,
        offset_params_in_body=True,
        loop_until_end=loop_until_end,
        arr_fn=arr_fn,
        body_fn=body_fn,
        body=body,
        debug_api=debug_api,
        debug_loop=debug_loop,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_GET_Error(res=res)

    if not suppress_no_results_error and len(res.response) == 0:
        raise SearchUser_NotFound(search_criteria=str(body), res=res)

    res.response = process_v1_search_users(res.response)

    return res


@gd.route_function
async def search_users_by_id(
    user_ids: list[str],  # list of user ids to search
    auth: DomoAuth,
    debug_api: bool = False,
    return_raw: bool = False,
    suppress_no_results_error: bool = False,
    debug_num_stacks_to_drop=2,
    parent_class=None,
    session: Optional[httpx.AsyncClient] = None,
) -> rgd.ResponseGetData:  # ResponseGetData with user list
    """Search for users by their IDs using the v1 users search API.

    Args:
        user_ids: List of user IDs to search for
        auth: Authentication object
        debug_api: Enable API debugging
        return_raw: Return raw API response without processing
        suppress_no_results_error: Don't raise error if no results found
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        session: HTTP client session

    Returns:
        ResponseGetData object containing found users

    Raises:
        User_GET_Error: If search request fails
        SearchUser_NotFound: If no users found and suppress_no_results_error is False
    """

    user_cn = ce.chunk_list(user_ids, 1000)

    res_ls = await ce.gather_with_concurrency(
        n=6,
        *[
            search_users(
                auth=auth,
                body={
                    # "showCount": true,
                    # "count": false,
                    "includeDeleted": False,
                    "includeSupport": False,
                    "filters": [
                        {
                            "field": "id",
                            "filterType": "value",
                            "values": user_ls,
                            "operator": "EQ",
                        }
                    ],
                    "parts": ["DETAILED", "GROUPS", "ROLE"],
                    "attributes": [
                        "id",
                        "displayName",
                        "roleId",
                        "department",
                        "title",
                        "emailAddress",
                        "phoneNumber",
                        "lastActivity",
                    ],
                },
                debug_api=debug_api,
                return_raw=return_raw,
                suppress_no_results_error=suppress_no_results_error,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                parent_class=parent_class,
                session=session,
            )
            for user_ls in user_cn
        ],
    )

    if return_raw:
        return res_ls

    res = res_ls[-1]

    res.response = [row for ls in [_.response for _ in res_ls] for row in ls]

    return res


@gd.route_function
async def search_users_by_email(
    user_email_ls: list[
        str
    ],  # list of user emails to search.  Note:  search does not appear to be case sensitive
    auth: DomoAuth,
    debug_api: bool = False,
    return_raw: bool = False,
    suppress_no_results_error: bool = False,
    debug_num_stacks_to_drop=2,
    parent_class=None,
    session: httpx.AsyncClient = None,
) -> rgd.ResponseGetData:  # ResponseGetData with user list
    """Search for users by their email addresses using the v1 users search API.

    Args:
        user_email_ls: List of user email addresses to search for
        auth: Authentication object
        debug_api: Enable API debugging
        return_raw: Return raw API response without processing
        suppress_no_results_error: Don't raise error if no results found
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        session: HTTP client session

    Returns:
        ResponseGetData object containing found users

    Raises:
        User_GET_Error: If search request fails
        SearchUser_NotFound: If no users found and suppress_no_results_error is False

    Note:
        Search does not appear to be case sensitive
    """

    user_cn = ce.chunk_list(user_email_ls, 1000)

    res_ls = await ce.gather_with_concurrency(
        n=10,
        *[
            search_users(
                auth=auth,
                body={
                    # "showCount": true,
                    # "count": false,
                    "includeDeleted": False,
                    "includeSupport": False,
                    "limit": 200,
                    "offset": 0,
                    "sort": {"field": "displayName", "order": "ASC"},
                    "filters": [
                        {
                            "filterType": "text",
                            "field": "emailAddress",
                            "text": " ".join(user_ls),
                        }
                    ],
                    "parts": ["DETAILED", "GROUPS", "ROLE"],
                    "attributes": [
                        "id",
                        "displayName",
                        "roleId",
                        "department",
                        "title",
                        "emailAddress",
                        "phoneNumber",
                        "lastActivity",
                    ],
                },
                debug_api=debug_api,
                return_raw=return_raw,
                suppress_no_results_error=suppress_no_results_error,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                parent_class=parent_class,
                session=session,
            )
            for user_ls in user_cn
        ],
    )

    if return_raw:
        return res_ls

    res = res_ls[-1]

    res.response = [row for ls in [_.response for _ in res_ls] for row in ls]
    return res


@gd.route_function
async def _get_by_id(
    user_id,
    auth: DomoAuth,
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=1,
    parent_class=None,
):
    """Internal function to get user by ID using v2 and v3 APIs.
    
    This function combines data from both v2 and v3 endpoints to provide
    comprehensive user information. Does not include role_id from v2 endpoint.
    """
    # does not include role_id
    v2_url = f"https://{auth.domo_instance}.domo.com/api/content/v2/users/{user_id}"

    v3_url = f"https://{auth.domo_instance}.domo.com/api/content/v3/users/{user_id}"

    params = {
        "includeDetails": True,
        "attributes": [
            "id",
            "displayName",
            "roleId",
            "department",
            "title",
            "emailAddress",
            "phoneNumber",
            "lastActivity",
        ],
    }

    res_v2, res_v3 = await asyncio.gather(
        gd.get_data(
            url=v2_url,
            method="GET",
            auth=auth,
            debug_api=debug_api,
            session=session,
            params=params,
            num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        ),
        gd.get_data(
            url=v3_url,
            method="GET",
            auth=auth,
            debug_api=debug_api,
            session=session,
            params=params,
            num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        ),
    )

    if return_raw:
        res_v2.response = {**res_v2.response, **res_v3.response}
        return res_v2

    if res_v2.status == 200 and res_v2.response == "":
        raise SearchUser_NotFound(
            search_criteria=f"user_id {user_id} not found", res=res_v2
        )

    if not res_v2.is_success:
        raise User_GET_Error(res=res_v2)

    if res_v3.status == "404" and res_v3.response == "Not Found":
        raise SearchUser_NotFound(
            res=res_v3,
            search_criteria=f"user_id {user_id} not found",
        )
    if (
        not res_v3.status == "404" and not res_v3.response == "Not Found"
    ) and not res_v3.is_success:
        raise User_GET_Error(res=res_v3)

    detail = {
        **res_v3.response.pop("detail"),
        # **res_v2.response.pop('detail')
    }

    res_v2.response = {**res_v2.response, **res_v3.response, **detail}

    return res_v2


@gd.route_function
async def get_by_id(
    user_id,
    auth: DomoAuth,
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    is_v2: bool = True,
):
    """Retrieve a specific user by ID.

    Args:
        user_id: The unique identifier for the user
        auth: Authentication object
        debug_api: Enable API debugging
        return_raw: Return raw API response without processing
        session: HTTP client session
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        is_v2: If True, use v2 search API, otherwise use combined v2/v3 approach

    Returns:
        ResponseGetData object containing user information

    Raises:
        User_GET_Error: If user retrieval fails
        SearchUser_NotFound: If user with specified ID doesn't exist
    """
    if not is_v2:
        return await _get_by_id(
            user_id=user_id,
            auth=auth,
            debug_api=debug_api,
            return_raw=return_raw,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            parent_class=parent_class,
        )

    res = await search_users_by_id(
        user_ids=[user_id],
        auth=auth,
        debug_api=debug_api,
        return_raw=return_raw,
        suppress_no_results_error=False,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 2,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    res.response = res.response[0]
    return res


@gd.route_function
async def search_virtual_user_by_subscriber_instance(
    auth: DomoAuth,  # domo auth object
    subscriber_instance_ls: list[str],  # list of subscriber domo instances
    debug_api: bool = False,  # debug API requests
    debug_num_stacks_to_drop: int = 1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:  # list of virtual domo users
    """Retrieve virtual users for subscriber instances tied to one publisher.

    Args:
        auth: Authentication object for the publisher instance
        subscriber_instance_ls: List of subscriber Domo instance names
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        session: HTTP client session
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing virtual users

    Raises:
        User_GET_Error: If virtual user retrieval fails
    """

    url = f"https://{auth.domo_instance}.domo.com/api/publish/v2/proxy_user/domain/"

    body = {
        "domains": [
            f"{subscriber_instance}.domo.com"
            for subscriber_instance in subscriber_instance_ls
        ]
    }

    res = await gd.get_data(
        url=url,
        method="POST",
        auth=auth,
        body=body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_GET_Error(res=res)

    return res


@gd.route_function
async def create_user(
    auth: DomoAuth,
    display_name: str,
    email_address: str,
    role_id: int,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 1,
    parent_class: str = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Create a new user in the Domo instance.

    Args:
        auth: Authentication object
        display_name: Display name for the new user
        email_address: Email address for the new user (must be valid)
        role_id: Role ID to assign to the new user
        debug_api: Enable API debugging
        session: HTTP client session
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing created user information

    Raises:
        User_CRUD_Error: If user creation fails
        ValueError: If email address is invalid
    """
    url = f"https://{auth.domo_instance}.domo.com/api/content/v3/users"

    test_valid_email(email_address)

    body = {
        "displayName": display_name,
        "detail": {"email": email_address},
        "roleId": role_id,
    }

    res = await gd.get_data(
        url=url,
        method="POST",
        body=body,
        auth=auth,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if res.status == 400 and res.response == "Bad Request":
        raise User_CRUD_Error(
            operation="create",
            res=res,
            message=f"{res.response} - does this user {email_address} already exist?",
        )

    if not res.is_success:
        raise User_CRUD_Error(operation="create", res=res)

    res.is_success = True
    return res


@gd.route_function
async def set_user_landing_page(
    auth: DomoAuth,
    user_id: str,
    page_id: str,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    """Set a user's landing page.

    Args:
        auth: Authentication object
        user_id: ID of the user to update
        page_id: ID of the page to set as landing page
        debug_api: Enable API debugging
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        session: HTTP client session
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object confirming the update

    Raises:
        User_CRUD_Error: If landing page update fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/landings/target/DESKTOP/entity/PAGE/id/{page_id}/{user_id}"

    res = await gd.get_data(
        url=url,
        method="PUT",
        auth=auth,
        # body = body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_CRUD_Error(
            operation="set_landing_page",
            user_id=user_id,
            res=res,
        )

    return res


@gd.route_function
async def reset_password(
    auth: DomoAuth,
    user_id: str,
    new_password: str,
    debug_api: bool = False,
    parent_class=None,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Reset a user's password.

    Args:
        auth: Authentication object
        user_id: ID of the user whose password to reset
        new_password: New password for the user
        debug_api: Enable API debugging
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        session: HTTP client session
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object confirming password reset

    Raises:
        User_CRUD_Error: If password reset fails
        ResetPassword_PasswordUsed: If password was previously used
    """
    url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/password"

    body = {"domoUserId": user_id, "password": new_password}

    res = await gd.get_data(
        url=url,
        method="PUT",
        auth=auth,
        body=body,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_CRUD_Error(
            operation="reset_password",
            user_id=user_id,
            res=res,
            message="unable to change password",
        )

    if (
        res.status == 200
        and res.response.get("description", None)
        == "Password has been used previously."
    ):
        raise ResetPassword_PasswordUsed(
            user_id=user_id,
            res=res,
            message=res.response["description"].replace(".", ""),
        )

    return res


@gd.route_function
async def request_password_reset(
    domo_instance: str,
    email: str,
    locale="en-us",
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    return_raw: bool = False,
):
    """Request a password reset for a user via email.

    Args:
        domo_instance: Name of the Domo instance
        email: Email address of the user requesting password reset
        locale: Locale for the reset email (default: "en-us")
        debug_api: Enable API debugging
        session: HTTP client session
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object confirming password reset request

    Raises:
        User_GET_Error: If password reset request fails
    """
    url = f"https://{domo_instance}.domo.com/api/domoweb/auth/sendReset"

    params = {"email": email, "local": locale}

    res = await gd.get_data(
        url=url,
        method="GET",
        params=params,
        auth=None,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_GET_Error(
            res=res,
            message=f"unable to change password {res.response}",
        )

    return res


@gd.route_function
async def download_avatar(
    user_id,
    auth: DomoAuth,
    pixels: int = 300,
    folder_path="./images",
    img_name=None,
    is_download_image: bool = True,
    debug_api: bool = False,
    return_raw: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
):
    """Download a user's avatar image.

    Args:
        user_id: ID of the user whose avatar to download
        auth: Authentication object
        pixels: Size of the avatar in pixels (default: 300)
        folder_path: Path to save the avatar image (default: "./images")
        img_name: Custom name for the image file (optional)
        is_download_image: Whether to save image to disk (default: True)
        debug_api: Enable API debugging
        return_raw: Return raw API response without processing
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        session: HTTP client session

    Returns:
        ResponseGetData object containing avatar data

    Raises:
        DownloadAvatar_Error: If avatar download fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/avatar/USER/{user_id}?size={pixels}"

    res = await gd.get_data_stream(
        url=url,
        method="GET",
        auth=auth,
        debug_api=debug_api,
        headers={"accept": "image/png;charset=utf-8"},
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if res.status != 200:
        raise DownloadAvatar_Error(
            res=res,
            user_id=user_id,
        )

    if is_download_image:
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        if img_name:
            img_name = img_name.replace(".png", "")

        img_name = f"{img_name or user_id}.png"

        file_path = os.path.join(folder_path, img_name)

        with open(file_path, "wb") as out_file:
            out_file.write(res.response)

    res.is_success = True

    return res


def generate_avatar_bytestr(img_bytestr, img_type):
    """Generate base64 encoded avatar byte string for upload.

    Args:
        img_bytestr: Image data as bytes or base64 string
        img_type: Image type ('jpg' or 'png')

    Returns:
        str: Base64 encoded image string with data URI prefix
    """
    if isinstance(img_bytestr, str):
        img_bytestr = img_bytestr.encode("utf-8")

    if not uimg.isBase64(img_bytestr):
        img_bytestr = base64.b64encode(img_bytestr)

    img_bytestr = img_bytestr.decode("utf-8")

    html_encoding = f"data:image/{img_type};base64,"

    if not img_bytestr.startswith(html_encoding):
        img_bytestr = html_encoding + img_bytestr

    return img_bytestr


@gd.route_function
async def upload_avatar(
    auth: DomoAuth,
    user_id: int,
    img_bytestr: bytes,
    img_type: str,  #'jpg or png'
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    return_raw: bool = False,
):
    """Upload an avatar image for a user.

    Args:
        auth: Authentication object
        user_id: ID of the user to update avatar for
        img_bytestr: Image data as bytes
        img_type: Image type ('jpg' or 'png')
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        session: HTTP client session
        parent_class: Name of calling class for debugging
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object confirming avatar upload

    Raises:
        User_CRUD_Error: If avatar upload fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/avatar/bulk"

    body = {
        "base64Image": generate_avatar_bytestr(img_bytestr, img_type),
        "encodedImage": generate_avatar_bytestr(img_bytestr, img_type),
        "isOpen": False,
        "entityIds": [user_id],
        "entityType": "USER",
    }

    # return body

    res = await gd.get_data(
        url=url,
        method="POST",
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        auth=auth,
        parent_class=None,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_CRUD_Error(
            operation="upload_avatar",
            user_id=str(user_id),
            res=res,
        )

    return res


@gd.route_function
async def delete_user(
    auth: DomoAuth,
    user_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Delete a user from the Domo instance.

    Args:
        auth: Authentication object
        user_id: ID of the user to delete
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        session: HTTP client session
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object confirming user deletion

    Raises:
        DeleteUser_Error: If user deletion fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/users/{user_id}"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="DELETE",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise DeleteUser_Error(res=res)

    return res


@gd.route_function
async def user_is_allowed_direct_signon(
    auth: DomoAuth,
    user_ids: List[str],
    is_allow_dso: bool = True,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Manage direct sign-on permissions for users.

    Args:
        auth: Authentication object
        user_ids: List of user IDs to modify
        is_allow_dso: Whether to allow direct sign-on (default: True)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        session: HTTP client session
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object confirming permission changes

    Raises:
        User_CRUD_Error: If direct sign-on permission update fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/content/v3/users/directSignOn"
    params = {"value": is_allow_dso}

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=user_ids if isinstance(user_ids, list) else [user_ids],
        params=params,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_CRUD_Error(
            operation="update_direct_signon",
            res=res
        )

    return res