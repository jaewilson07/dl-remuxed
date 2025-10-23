__all__ = [
    "AppStudio_GET_Error",
    "AppStudio_CRUD_Error",
    "AppStudioSharing_Error",
    "get_appstudio_by_id",
    "get_appstudio_access",
    "get_appstudios_adminsummary",
    "generate_body_add_page_owner_appstudios",
    "generate_body_share_appstudio",
    "add_page_owner",
    "share",
]

<<<<<<< HEAD
from typing import List

import httpx

<<<<<<<< HEAD:src/routes/appstudio.py
from ..client import auth as dmda
from ..client import exceptions as dmde
from ..client import get_data as gd
from ..client import response as rgd
========
from ..client import exceptions as dmde, get_data as gd, response as rgd
>>>>>>>> test:src/domolibrary2/routes/appstudio.py


class AppStudio_API_Error(dmde.RouteError):
    def __init__(
        self, res: rgd.ResponseGetData, appstudio_id: int = None, message: str = None
    ):
        super().__init__(message=message, res=res, entity_id=appstudio_id)


class AppStudio_CRUD_Error(dmde.RouteError):
    def __init__(
        self, res: rgd.ResponseGetData, appstudio_id=None, message: str = None
    ):
        super().__init__(
            message=message,
            res=res,
            entity_id=appstudio_id,
=======
from typing import List, Optional

import httpx

from ..client.auth import DomoAuth
from ..client import exceptions as dmde, get_data as gd, response as rgd


class AppStudio_GET_Error(dmde.RouteError):
    """Raised when AppStudio retrieval operations fail."""

    def __init__(
        self,
        appstudio_id: Optional[str] = None,
        res: Optional[rgd.ResponseGetData] = None,
        message: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message or "AppStudio retrieval failed",
            entity_id=appstudio_id,
            res=res,
            **kwargs
        )


class AppStudio_CRUD_Error(dmde.RouteError):
    """Raised when AppStudio create, update, or delete operations fail."""

    def __init__(
        self,
        operation: str = "operation",
        appstudio_id: Optional[str] = None,
        res: Optional[rgd.ResponseGetData] = None,
        message: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message or f"AppStudio {operation} operation failed",
            entity_id=appstudio_id,
            res=res,
            **kwargs
>>>>>>> main
        )


class AppStudioSharing_Error(dmde.RouteError):
<<<<<<< HEAD
    def __init__(
        self,
        res: rgd.ResponseGetData,
        message: str = None,
        appstudio_id: int = None,
    ):
        super().__init__(
            res=res,
            message=message,
            entity_id=appstudio_id,
=======
    """Raised when AppStudio sharing operations fail."""

    def __init__(
        self,
        appstudio_id: Optional[str] = None,
        res: Optional[rgd.ResponseGetData] = None,
        message: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message or "AppStudio sharing operation failed",
            entity_id=appstudio_id,
            res=res,
            **kwargs
>>>>>>> main
        )


@gd.route_function
async def get_appstudio_by_id(
    auth: DomoAuth,
    appstudio_id: str,
<<<<<<< HEAD
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 1,  # for traceback_details.  use 1 for route functions, 2 for class method
    parent_class: str = None,  # pass in self.__class__.__name__ into function
) -> (
    rgd.ResponseGetData
):  # returns ResponseGetData on success or raise Exception on error
    """retrieves a page or throws an error"""

=======
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieves an AppStudio page by ID.

    Args:
        auth: Authentication object
        appstudio_id: AppStudio identifier
        session: Optional HTTP session
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Number of stack frames to drop in traceback
        parent_class: Name of the calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object

    Raises:
        AppStudio_GET_Error: If retrieval fails
    """
>>>>>>> main
    # 9/21/2023 - the domo UI uses /cards to get page info
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/dataapps/{appstudio_id}?authoring=true&includeHiddenViews=true"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

<<<<<<< HEAD
    if not res.is_success:
        raise AppStudio_API_Error(
            res=res,
            appstudio_id=appstudio_id,
=======
    if return_raw:
        return res

    if not res.is_success:
        raise AppStudio_GET_Error(
            appstudio_id=appstudio_id,
            res=res,
>>>>>>> main
        )

    return res


@gd.route_function
async def get_appstudio_access(
<<<<<<< HEAD
    auth,
    appstudio_id,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
):
    """retrieves accesslist, which users and groups a page is shared with"""
=======
    auth: DomoAuth,
    appstudio_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieves access list for an AppStudio page.

    Args:
        auth: Authentication object
        appstudio_id: AppStudio identifier
        session: Optional HTTP session
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Number of stack frames to drop in traceback
        parent_class: Name of the calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing users and groups the page is shared with

    Raises:
        AppStudio_GET_Error: If retrieval fails
    """
>>>>>>> main
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/dataapps/{appstudio_id}/access"

    res = await gd.get_data(
        url,
        method="GET",
        auth=auth,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

<<<<<<< HEAD
    if not res.is_success:
        raise AppStudio_API_Error(
            res=res,
            appstudio_id=appstudio_id,
=======
    if return_raw:
        return res

    if not res.is_success:
        raise AppStudio_GET_Error(
            appstudio_id=appstudio_id,
            res=res,
>>>>>>> main
        )

    return res


@gd.route_function
async def get_appstudios_adminsummary(
    auth: DomoAuth,
<<<<<<< HEAD
    limit=35,
    debug_loop: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
):
    """retrieves all pages in instance user is able to see (but may not have been explicitly shared)"""

=======
    limit: int = 35,
    session: Optional[httpx.AsyncClient] = None,
    debug_loop: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieves all AppStudio pages in instance user is able to see.

    Args:
        auth: Authentication object
        limit: Maximum number of items per page
        session: Optional HTTP session
        debug_loop: Enable loop debugging
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Number of stack frames to drop in traceback
        parent_class: Name of the calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing all accessible AppStudio pages

    Raises:
        AppStudio_GET_Error: If retrieval fails
    """
>>>>>>> main
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/dataapps/adminsummary"

    offset_params = {
        "offset": "skip",
        "limit": "limit",
    }

    body = {"orderBy": "title", "ascending": True}

    def arr_fn(res):
        return res.response.get("dataAppAdminSummaries")

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        arr_fn=arr_fn,
        offset_params=offset_params,
        session=session,
        loop_until_end=True,
        body=body,
        limit=limit,
        debug_loop=debug_loop,
        debug_api=debug_api,
        parent_class=parent_class,
        return_raw=return_raw,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
<<<<<<< HEAD
        raise AppStudio_API_Error(res=res)
=======
        raise AppStudio_GET_Error(res=res)
>>>>>>> main

    return res


def generate_body_add_page_owner_appstudios(
    appstudio_id_ls: List[int],
<<<<<<< HEAD
    group_id_ls: List[int] = None,
    user_id_ls: List[int] = None,
    note: str = "",
    send_email: bool = False,
) -> dict:
=======
    group_id_ls: Optional[List[int]] = None,
    user_id_ls: Optional[List[int]] = None,
    note: str = "",
    send_email: bool = False,
) -> dict:
    """Generates request body for adding page owners to AppStudio pages.

    Args:
        appstudio_id_ls: List of AppStudio IDs
        group_id_ls: Optional list of group IDs
        user_id_ls: Optional list of user IDs
        note: Optional note to include
        send_email: Whether to send email notifications

    Returns:
        Dictionary containing the request body
    """
>>>>>>> main
    group_id_ls = group_id_ls or []
    user_id_ls = user_id_ls or []
    owners = []

    for group in group_id_ls:
        owners.append({"id": group, "type": "GROUP"})
    for user in user_id_ls:
        owners.append({"id": user, "type": "USER"})

    body = {
        "entityIds": appstudio_id_ls,
        "owners": owners,
        "note": note,
        "sendEmail": send_email,
    }

    return body


def generate_body_share_appstudio(
    appstudio_ids: List[int],
<<<<<<< HEAD
    group_ids: list = None,
    user_ids: list = None,
    message: str = None,
) -> dict:
=======
    group_ids: Optional[List[int]] = None,
    user_ids: Optional[List[int]] = None,
    message: Optional[str] = None,
) -> dict:
    """Generates request body for sharing AppStudio pages.

    Args:
        appstudio_ids: List of AppStudio IDs to share
        group_ids: Optional list of group IDs
        user_ids: Optional list of user IDs
        message: Optional message to include

    Returns:
        Dictionary containing the request body
    """
>>>>>>> main
    group_ids = group_ids or []
    user_ids = user_ids or []

    appstudio_ids = (
        appstudio_ids if isinstance(appstudio_ids, list) else [appstudio_ids]
    )
    if group_ids:
        group_ids = (
            group_ids and group_ids if isinstance(group_ids, list) else [group_ids]
        )

    if user_ids:
        user_ids = user_ids if isinstance(user_ids, list) else [user_ids]

    recipient_ls = []

    if group_ids:
        for gid in group_ids:
            recipient_ls.append({"type": "group", "id": str(gid)})

    if user_ids:
        for uid in user_ids:
            recipient_ls.append({"type": "user", "id": str(uid)})

    body = {
        "dataAppIds": appstudio_ids,
        "recipients": recipient_ls,
        "message": message,
    }

    return body


@gd.route_function
async def add_page_owner(
    auth: DomoAuth,
    appstudio_id_ls: List[int],
<<<<<<< HEAD
    group_id_ls: List[int] = None,
    user_id_ls: List[int] = None,
    note: str = "",
    send_email: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
=======
    group_id_ls: Optional[List[int]] = None,
    user_id_ls: Optional[List[int]] = None,
    note: str = "",
    send_email: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Adds page owners to AppStudio pages.

    Args:
        auth: Authentication object
        appstudio_id_ls: List of AppStudio IDs
        group_id_ls: Optional list of group IDs to add as owners
        user_id_ls: Optional list of user IDs to add as owners
        note: Optional note to include with the change
        send_email: Whether to send email notifications
        session: Optional HTTP session
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Number of stack frames to drop in traceback
        parent_class: Name of the calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object

    Raises:
        AppStudioSharing_Error: If sharing operation fails
    """
>>>>>>> main
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/dataapps/bulk/owners"

    body = generate_body_add_page_owner_appstudios(
        appstudio_id_ls=appstudio_id_ls,
        group_id_ls=group_id_ls,
        user_id_ls=user_id_ls,
        note=note,
        send_email=send_email,
    )

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
        raise AppStudioSharing_Error(res=res)

    res.response = f"{appstudio_id_ls} appstudios successfully shared with {', '.join([recipient['id'] for recipient in body['owners']])} as owners"

    return res


@gd.route_function
async def share(
    auth: DomoAuth,
    appstudio_ids: List[int],
<<<<<<< HEAD
    group_ids: List[int] = None,
    user_ids: List[int] = None,
    message: str = None,  # email to user
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    return_raw: bool = False,
):
=======
    group_ids: Optional[List[int]] = None,
    user_ids: Optional[List[int]] = None,
    message: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Shares AppStudio pages with users or groups.

    Args:
        auth: Authentication object
        appstudio_ids: List of AppStudio IDs to share
        group_ids: Optional list of group IDs to share with
        user_ids: Optional list of user IDs to share with
        message: Optional message to include in email notification
        session: Optional HTTP session
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Number of stack frames to drop in traceback
        parent_class: Name of the calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object

    Raises:
        AppStudioSharing_Error: If sharing operation fails
    """
>>>>>>> main
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/dataapps/share?sendEmail=false"

    body = generate_body_share_appstudio(
        appstudio_ids=appstudio_ids,
        group_ids=group_ids,
        user_ids=user_ids,
        message=message,
    )

    res = await gd.get_data(
        url,
        method="POST",
        auth=auth,
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )
<<<<<<< HEAD
=======

>>>>>>> main
    if return_raw:
        return res

    if not res.is_success:
        raise AppStudioSharing_Error(res=res)

    res.response = f"{appstudio_ids} appstudios successfully shared with {', '.join([recipient['id'] for recipient in body['recipients']])}"

    return res
