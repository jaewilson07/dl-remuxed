"""
Page Access Functions

This module provides functions for managing page access control and permissions.

Functions:
    get_page_access_test: Test page access permissions for the authenticated user
    get_page_access_list: Retrieve page access list showing which users and groups have access
    add_page_owner: Add owners to multiple pages
"""

__all__ = [
    "get_page_access_test",
    "get_page_access_list",
    "add_page_owner",
]

from typing import List, Optional, Union

import httpx

from ...client import (
    get_data as gd,
    response as rgd,
)
from ...client.auth import DomoAuth
from ...utils.logging import DomoEntityExtractor, DomoEntityResultProcessor
from dc_logger.decorators import log_call, LogDecoratorConfig
from .exceptions import (
    Page_CRUD_Error,
    Page_GET_Error,
    PageSharing_Error,
    SearchPage_NotFound,
)


@gd.route_function
@log_call(
    level_name="route",
    config=LogDecoratorConfig(
        entity_extractor=DomoEntityExtractor(),
        result_processor=DomoEntityResultProcessor()
    )
)
async def get_page_access_test(
    auth: DomoAuth,
    page_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Test page access permissions for the authenticated user.

    Args:
        auth: Authentication object containing credentials and instance info
        page_id: Unique identifier for the page
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing page access information

    Raises:
        Page_GET_Error: If access test fails
        SearchPage_NotFound: If page with specified ID doesn't exist
    """
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/pages/{page_id}/access"

    res = await gd.get_data(
        url,
        method="GET",
        auth=auth,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        if res.status == 404:
            raise SearchPage_NotFound(
                search_criteria=f"page_id: {page_id}",
                res=res,
            )
        raise Page_GET_Error(page_id=page_id, res=res)

    return res


@gd.route_function
@log_call(
    level_name="route",
    config=LogDecoratorConfig(
        entity_extractor=DomoEntityExtractor(),
        result_processor=DomoEntityResultProcessor()
    )
)
async def get_page_access_list(
    auth: DomoAuth,
    page_id: str,
    is_expand_users: bool = True,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve page access list showing which users and groups have access.

    Args:
        auth: Authentication object containing credentials and instance info
        page_id: Unique identifier for the page
        is_expand_users: Whether to expand group memberships to include individual users
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing access list with users and groups

    Raises:
        PageSharing_Error: If access list retrieval fails
        SearchPage_NotFound: If page with specified ID doesn't exist
    """

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/share/accesslist/page/{page_id}?expandUsers={is_expand_users}"

    res = await gd.get_data(
        url,
        method="GET",
        auth=auth,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        if res.status == 404:
            raise SearchPage_NotFound(
                search_criteria=f"page_id: {page_id}",
                res=res,
            )
        raise PageSharing_Error(
            operation="retrieve access list",
            page_id=page_id,
            res=res,
        )

    res.response["explicitSharedUserCount"] = len(res.response.get("users"))
    for user in res.response.get("users"):
        user.update({"isExplicitShare": True})

    # add group members to users response
    if is_expand_users:
        group_users = [
            {**user, "isExplicitShare": False}
            for group in res.response.get("groups")
            for user in group.get("users")
        ]
        users = res.response.get("users") + [
            group_user
            for group_user in group_users
            if group_user.get("id")
            not in [user.get("id") for user in res.response.get("users")]
        ]
        res.response.update({"users": users})

    return res


@gd.route_function
@log_call(
    level_name="route",
    config=LogDecoratorConfig(
        entity_extractor=DomoEntityExtractor(),
        result_processor=DomoEntityResultProcessor()
    )
)
async def add_page_owner(
    auth: DomoAuth,
    page_id_ls: List[Union[int, str]],
    group_id_ls: Optional[List[Union[int, str]]] = None,
    user_id_ls: Optional[List[Union[int, str]]] = None,
    note: str = "",
    send_email: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Add owners to multiple pages.

    Args:
        auth: Authentication object containing credentials and instance info
        page_id_ls: List of page IDs to add owners to
        group_id_ls: Optional list of group IDs to add as owners
        user_id_ls: Optional list of user IDs to add as owners
        note: Optional note to include with ownership changes
        send_email: Whether to send notification email
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing ownership update result

    Raises:
        Page_CRUD_Error: If adding page owners fails
    """
    page_id_ls = [str(ele) for ele in page_id_ls]
    group_id_ls = group_id_ls or []
    user_id_ls = user_id_ls or []

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/pages/bulk/owners"
    owners = []
    for group in group_id_ls:
        owners.append({"id": str(group), "type": "GROUP"})
    for user in user_id_ls:
        owners.append({"id": str(user), "type": "USER"})

    body = {
        "pageIds": page_id_ls,
        "owners": owners,
        "note": note,
        "sendEmail": send_email,
    }

    res = await gd.get_data(
        auth=auth,
        method="PUT",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Page_CRUD_Error(
            operation="add owners",
            message=f"Unable to add owners to pages {', '.join(page_id_ls)}",
            res=res,
        )

    res.response = f"Successfully added owners to pages {', '.join(page_id_ls)}"

    return res
