"""
Core Account Route Functions

This module provides core account retrieval functions for both regular and OAuth accounts.

Functions:
    get_available_data_providers: Retrieve available data providers
    get_accounts: Retrieve all accounts user has access to
    get_account_by_id: Retrieve specific account by ID
"""

from typing import Optional, Union

import httpx

from ...client import (
    get_data as gd,
    response as rgd,
)
from ...client.auth import DomoAuth
from .exceptions import Account_GET_Error, Account_NoMatch


@gd.route_function
async def get_available_data_providers(
    auth: DomoAuth,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve available data providers from Domo.

    Args:
        auth: Authentication object
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing available data providers

    Raises:
        Account_GET_Error: If data provider retrieval fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/providers"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Account_GET_Error(res=res)

    return res


@gd.route_function
async def get_accounts(
    auth: DomoAuth,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve a list of all accounts the user has read access to.

    Note: Users with "Manage all accounts" permission will retrieve all account objects.

    Args:
        auth: Authentication object for API requests
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing account list

    Raises:
        Account_GET_Error: If account retrieval fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/accounts"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Account_GET_Error(res=res)
    return res


@gd.route_function
async def get_account_by_id(
    auth: DomoAuth,
    account_id: Union[int, str],
    is_unmask: bool = False,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve metadata about a specific account.

    Args:
        auth: Authentication object for API requests
        account_id: The ID of the account to retrieve
        is_unmask: Whether to unmask encrypted values in response
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing account metadata

    Raises:
        Account_NoMatch: If account is not found or not accessible
        Account_GET_Error: If account retrieval fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/accounts/{account_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        timeout=20,  # occasionally this API has a long response time
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        params={"unmask": is_unmask},
    )

    if return_raw:
        return res

    if not res.is_success and (
        res.response == "Forbidden" or res.response == "Not Found"
    ):
        raise Account_NoMatch(account_id=str(account_id), res=res)

    if not res.is_success:
        raise Account_GET_Error(entity_id=str(account_id), res=res)

    return res
