__all__ = [
    "AppStudio_API_Error",
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

from typing import List

import httpx

from ..client import auth as dmda
from ..client import exceptions as dmde
from ..client import get_data as gd
from ..client import response as rgd


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
        )


class AppStudioSharing_Error(dmde.RouteError):
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
        )


@gd.route_function
async def get_appstudio_by_id(
    auth: DomoAuth,
    appstudio_id: str,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 1,  # for traceback_details.  use 1 for route functions, 2 for class method
    parent_class: str = None,  # pass in self.__class__.__name__ into function
) -> (
    rgd.ResponseGetData
):  # returns ResponseGetData on success or raise Exception on error
    """retrieves a page or throws an error"""

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

    if not res.is_success:
        raise AppStudio_API_Error(
            res=res,
            appstudio_id=appstudio_id,
        )

    return res


@gd.route_function
async def get_appstudio_access(
    auth,
    appstudio_id,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
):
    """retrieves accesslist, which users and groups a page is shared with"""
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

    if not res.is_success:
        raise AppStudio_API_Error(
            res=res,
            appstudio_id=appstudio_id,
        )

    return res


@gd.route_function
async def get_appstudios_adminsummary(
    auth: DomoAuth,
    limit=35,
    debug_loop: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
):
    """retrieves all pages in instance user is able to see (but may not have been explicitly shared)"""

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
        raise AppStudio_API_Error(res=res)

    return res


def generate_body_add_page_owner_appstudios(
    appstudio_id_ls: List[int],
    group_id_ls: List[int] = None,
    user_id_ls: List[int] = None,
    note: str = "",
    send_email: bool = False,
) -> dict:
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
    group_ids: list = None,
    user_ids: list = None,
    message: str = None,
) -> dict:
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
    group_ids: List[int] = None,
    user_ids: List[int] = None,
    message: str = None,  # email to user
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    return_raw: bool = False,
):
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
    if return_raw:
        return res

    if not res.is_success:
        raise AppStudioSharing_Error(res=res)

    res.response = f"{appstudio_ids} appstudios successfully shared with {', '.join([recipient['id'] for recipient in body['recipients']])}"

    return res
