__all__ = [
    "Sandbox_GET_Error",
    "get_is_allow_same_instance_promotion_enabled",
    "Sandbox_ToggleSameInstancePromotion_Error",
    "toggle_allow_same_instance_promotion",
    "get_shared_repos",
    "get_repo_from_id",
]

from typing import List

import httpx

from ..client import DomoAuth as dmda
from ..client import DomoError as dmde
from ..client import ResponseGetData as rgd
from ..client import get_data as gd


class Sandbox_GET_Error(dmde.RouteError):
    def __init(self, res: rgd.ResponseGetData, message: str = None):
        super().__init__(res=res, message=message)


@gd.route_function
async def get_is_allow_same_instance_promotion_enabled(
    auth: dmda.DomoAuth,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop: int = 1,
    debug_api: bool = False,
    parent_class: str = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/version/v1/settings"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Sandbox_GET_Error(res=res)

    res.response = {
        "name": "allow_same_instance_promotion",
        "is_enabled": res.response["allowSelfPromotion"],
    }

    return res


class Sandbox_ToggleSameInstancePromotion_Error(dmde.RouteError):
    def __init__(self, res: rgd.ResponseGetData, message: str = None, **kwargs):
        super().__init__(res=res, message=message, **kwargs)


@gd.route_function
async def toggle_allow_same_instance_promotion(
    is_enabled: bool,
    auth: dmda.DomoAuth,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 1,
    debug_api: bool = False,
    parent_class: str = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/version/v1/settings"

    body = {"allowSelfPromotion": is_enabled}

    res = await gd.get_data(
        auth=auth,
        method="POST",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Sandbox_ToggleSameInstancePromotion_Error(res=res)

    return res


@gd.route_function
async def get_shared_repos(
    auth: dmda.DomoAuth,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    parent_class: str = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/version/v1/repositories/search"

    body = {
        "query": {
            "offset": 0,
            "limit": 50,
            "fieldSearchMap": {},
            "sort": "lastCommit",
            "order": "desc",
            "filters": {"userId": None},
            "dateFilters": {},
        },
        "shared": False,
    }

    def arr_fn(res: rgd.ResponseGetData) -> List[dict]:
        return res.response["repositories"]

    offset_params = {"offset": "offset", "limit": "limit"}

    def body_fn(skip, limit, body):
        body["query"].update({"offset": skip, "limit": limit})
        return body

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        arr_fn=arr_fn,
        body_fn=body_fn,
        body=body,
        loop_until_end=True,
        offset_params=offset_params,
        offset_params_in_body=True,
        session=session,
        return_raw=return_raw,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Sandbox_GET_Error(res=res)

    return res


@gd.route_function
async def get_repo_from_id(
    auth: dmda.DomoAuth,
    repository_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/version/v1/repositories/{repository_id}"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        parent_class=parent_class,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )

    if not res.is_success:
        raise Sandbox_GET_Error(res=res)

    return res
