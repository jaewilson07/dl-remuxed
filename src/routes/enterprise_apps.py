__all__ = [
    "App_API_Exception",
    "get_all_designs",
    "get_design_by_id",
    "get_design_versions",
    "Design_GET_Assets",
    "get_design_source_code_by_version",
    "get_design_permissions",
    "set_design_admins",
    "add_design_admin",
]

import os
from typing import List

import httpx

from ..client import auth as dmda
from ..client import exceptions as dmde
from ..client import get_data as gd
from ..client import response as rgd
from ..utils import files as dmfi


class App_API_Exception(dmde.RouteError):
    def __init__(self, res: rgd.ResponseGetData):
        super().__init__(res=res)


@gd.route_function
async def get_all_designs(
    auth: DomoAuth,
    parts: str = "owners,creator,thumbnail,versions,cards",
    return_raw: bool = False,
    debug_loop: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/apps/v1/designs"

    params = {
        "checkAdminAuthority": True,
        "deleted": False,
        "direction": "desc",
        "parts": parts,
        "search": "",
        "withPermission": "ADMIN",
    }

    offset_paramse = {
        "limit": "limit",
        "offset": "offset",
    }

    res = await gd.looper(
        url=url,
        method="get",
        fixed_params=params,
        offset_params=offset_paramse,
        offset_params_in_body=False,
        auth=auth,
        debug_api=debug_api,
        debug_loop=debug_loop,
        timeout=10,
        limit=30,
        return_raw=return_raw,
        arr_fn=lambda x: x.response,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise App_API_Exception(res=res)

    if return_raw:
        return res

    return res


@gd.route_function
async def get_design_by_id(
    auth: DomoAuth,
    design_id: str,
    parts="owners,cards,versions,creator",
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/apps/v1/designs/{design_id}"

    res = await gd.get_data(
        url=url,
        method="get",
        params={"parts": parts},
        auth=auth,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise App_API_Exception(res=res)

    return res


@gd.route_function
async def get_design_versions(
    auth: DomoAuth,
    design_id,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/domoapps/designs/{design_id}/versions"

    res = await gd.get_data(
        url=url,
        auth=auth,
        method="get",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise App_API_Exception(res=res)

    return res


class Design_GET_Assets(DomoError):
    def __init__(self, res, design_id, message=None):
        message = message or f"unable to download assets for {design_id}"
        super().__init__(res=res, message=message)


@gd.route_function
async def get_design_source_code_by_version(
    auth: DomoAuth,
    design_id,
    version,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
    download_path: str = None,  # location to download file to
    is_unpack_archive=True,
    return_raw: bool = False,
):
    url = f"http://{auth.domo_instance}.domo.com/domoapps/designs/{design_id}/versions/{version}/assets"

    res = await gd.get_data_stream(
        url=url,
        method="get",
        auth=auth,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success and res.response == "Not Found":
        raise Design_GET_Assets(res=res, design_id=design_id, message="Not Found")

    if not res.is_success:
        raise Design_GET_Assets(res=res, design_id=design_id)

    if download_path:
        archive_path = os.path.join(download_path, "archive.zip")

        dmfi.download_zip(
            output_folder=archive_path,
            zip_bytes_content=res.response,
            is_unpack_archive=False,
        )

        if is_unpack_archive:
            dmfi.download_zip(
                output_folder=download_path,
                zip_bytes_content=res.response,
                is_unpack_archive=True,
            )

    return res


@gd.route_function
async def get_design_permissions(
    design_id: str,
    auth: DomoAuth,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
):
    res = await get_design_by_id(
        auth=auth,
        design_id=design_id,
        parts="owners",
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        session=session,
        parent_class=parent_class,
    )

    res.response = res.response["owners"]
    return res


async def set_design_admins(
    design_id,
    auth: DomoAuth,
    user_ids: List[str],
    debug_api: bool = False,
    return_raw: bool = False,
):
    url = f"https://{auth.domo_instance}.domo.com/api/apps/v1/designs/{design_id}/permissions/ADMIN"

    res = await gd.get_data(
        url=url,
        method="POST",
        auth=auth,
        debug_api=debug_api,
        body=user_ids,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise App_API_Exception(res=res)

    res.response = f"successfully set design_id {design_id} admins to {user_ids}"

    return res


async def add_design_admin(
    design_id: str, auth: DomoAuth, user_ids: List[int], debug_api: bool = False
):
    user_ids = user_ids if isinstance(user_ids, list) else [user_ids]

    res = await get_design_permissions(
        design_id=design_id, auth=auth, debug_api=debug_api
    )

    user_ids = list(set([owner["id"] for owner in res.response] + user_ids))

    return await set_design_admins(
        design_id=design_id, auth=auth, debug_api=debug_api, user_ids=user_ids
    )
