"""
Account Sharing Route Functions

This module provides account sharing and access management functions.

Functions:
    get_account_accesslist: Get account access list
    get_oauth_account_accesslist: Get OAuth account access list
    share_account: Share account with users/groups (v2 API)
    share_oauth_account: Share OAuth account
    share_account_v1: Legacy account sharing (v1 API)

Classes:
    ShareAccount: Abstract base class for sharing enums
    ShareAccount_AccessLevel: v2 API sharing permissions
    ShareAccount_V1_AccessLevel: v1 API sharing permissions (legacy)
"""

from enum import Enum
from typing import Optional, Union

import httpx

from ...client.auth import DomoAuth
from ...client import get_data as gd
from ...client import response as rgd
from .exceptions import AccountSharing_Error


class ShareAccount_V1_AccessLevel(Enum):
    """Legacy v1 API sharing permissions (users only)."""

    CAN_VIEW = "READ"
    CAN_EDIT = "WRITE"
    OWNER = "OWNER"

    def generate_payload(self, user_id: int, **kwargs):
        """Generate v1 sharing payload for users only."""
        return {"type": "USER", "id": int(user_id), "permissions": [self.value]}

    @classmethod
    def get(cls, value):
        """Get enum member by case-insensitive string lookup."""
        if not isinstance(value, str):
            return cls.CAN_VIEW

        for member in cls:
            if member.name.lower() == value.lower():
                return member

        return cls.CAN_VIEW


class ShareAccount_AccessLevel(Enum):
    """v2 API sharing permissions (users and groups)."""

    CAN_VIEW = "CAN_VIEW"
    CAN_EDIT = "CAN_EDIT"
    CAN_SHARE = "CAN_SHARE"
    OWNER = "OWNER"
    NO_ACCESS = "NONE"

    def generate_payload(self, user_id: int = None, group_id: int = None, **kwargs):
        """Generate v2 sharing payload for users or groups."""
        if user_id:
            return {"type": "USER", "id": str(user_id), "accessLevel": self.value}
        if group_id:
            return {"type": "GROUP", "id": str(group_id), "accessLevel": self.value}

    @classmethod
    def get(cls, value):
        """Get enum member by case-insensitive string lookup."""
        if not isinstance(value, str):
            return cls.CAN_VIEW

        for member in cls:
            if member.name.lower() == value.lower():
                return member

        return cls.CAN_VIEW


class Account_Share_Error(AccountSharing_Error):
    """Raised when account sharing operations fail."""

    def __init__(
        self,
        account_id: Optional[str] = None,
        response_data=None,
        message: Optional[str] = None,
        **kwargs,
    ):
        if not message:
            message = "Account sharing operation failed"
        super().__init__(
            operation="share",
            account_id=account_id,
            response_data=response_data,
            message=message,
            **kwargs,
        )


class Account_AlreadyShared_Error(AccountSharing_Error):
    """Raised when attempting to share account that is already shared."""

    def __init__(
        self,
        account_id: Optional[str] = None,
        response_data=None,
        message: Optional[str] = None,
        **kwargs,
    ):
        if not message:
            message = "Account is already shared with this user/group"
        super().__init__(
            operation="share (already exists)",
            account_id=account_id,
            response_data=response_data,
            message=message,
            **kwargs,
        )


@gd.route_function
async def get_account_accesslist(
    auth: DomoAuth,
    account_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get access list for an account.

    Args:
        auth: Authentication object for API requests
        account_id: ID of the account to get access list for
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing account access list

    Raises:
        AccountSharing_Error: If access list retrieval fails
    """
    url = (
        f"https://{auth.domo_instance}.domo.com/api/data/v2/accounts/{account_id}/share"
    )

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise AccountSharing_Error(
            operation="get access list", account_id=account_id, response_data=res
        )

    return res


@gd.route_function
async def get_oauth_account_accesslist(
    auth: DomoAuth,
    account_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get access list for an OAuth account.

    Args:
        auth: Authentication object for API requests
        account_id: ID of the OAuth account to get access list for
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing OAuth account access list

    Raises:
        AccountSharing_Error: If OAuth access list retrieval fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/data/v2/accounts/templates/{account_id}/share"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise AccountSharing_Error(
            operation="get OAuth access list", account_id=account_id, response_data=res
        )

    return res


@gd.route_function
async def share_account(
    auth: DomoAuth,
    account_id: str,
    share_payload: dict,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Share account with users/groups using v2 API.

    Note: This uses the v2 API which should be deployed to all Domo instances as of DP24.

    Args:
        auth: Authentication object for API requests
        account_id: ID of the account to share
        share_payload: Sharing configuration (use ShareAccount_AccessLevel.generate_payload())
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object confirming sharing operation

    Raises:
        Account_AlreadyShared_Error: If account is already shared with target
        Account_Share_Error: If sharing operation fails
    """
    url = (
        f"https://{auth.domo_instance}.domo.com/api/data/v2/accounts/share/{account_id}"
    )

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=share_payload,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        debug_api=debug_api,
        session=session,
    )

    if return_raw:
        return res

    if res.status == 500 and res.response == "Internal Server Error":
        raise Account_AlreadyShared_Error(
            account_id=account_id,
            message=f"{res.response} - User may already have access to account",
            response_data=res,
        )

    if not res.is_success:
        raise Account_Share_Error(
            account_id=account_id,
            response_data=res,
        )

    return res


@gd.route_function
async def share_oauth_account(
    auth: DomoAuth,
    account_id: str,
    share_payload: dict,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Share OAuth account with users/groups.

    Args:
        auth: Authentication object for API requests
        account_id: ID of the OAuth account to share
        share_payload: Sharing configuration (use ShareAccount_AccessLevel.generate_payload())
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object confirming sharing operation

    Raises:
        Account_Share_Error: If OAuth sharing operation fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/data/v2/accounts/templates/share/{account_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=share_payload,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        debug_api=debug_api,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Account_Share_Error(
            account_id=account_id,
            response_data=res,
        )

    return res


@gd.route_function
async def share_account_v1(
    auth: DomoAuth,
    account_id: str,
    share_payload: dict,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Share account using legacy v1 API (users only).

    Note: V1 API allows sharing with users ONLY. It does not support sharing with groups
    and has a more limited set of share rights (owner or read). See ShareAccount_V1_AccessLevel
    vs ShareAccount_AccessLevel for differences.

    Args:
        auth: Authentication object for API requests
        account_id: ID of the account to share
        share_payload: Sharing configuration (use ShareAccount_V1_AccessLevel.generate_payload())
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object confirming sharing operation

    Raises:
        Account_AlreadyShared_Error: If account is already shared with user
        Account_Share_Error: If sharing operation fails
    """
    url = (
        f"https://{auth.domo_instance}.domo.com/api/data/v1/accounts/{account_id}/share"
    )

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=share_payload,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        debug_api=debug_api,
        session=session,
    )

    if return_raw:
        return res

    if res.status == 500 and res.response == "Internal Server Error":
        raise Account_AlreadyShared_Error(
            account_id=account_id,
            message=f"{res.response} - User may already have access to account",
            response_data=res,
        )

    if not res.is_success:
        raise Account_Share_Error(
            account_id=account_id,
            response_data=res,
        )

    return res


# Attach sharing methods to enum classes for convenience
ShareAccount_AccessLevel.share = staticmethod(share_account)
ShareAccount_V1_AccessLevel.share = staticmethod(share_account_v1)
