__all__ = [
    "BeastMode_GET_Error",
    "BeastMode_CRUD_Error",
    "Search_BeastModeLink",
    "generate_beastmode_body",
    "search_beastmodes",
    "lock_beastmode",
    "get_beastmode_by_id",
    "get_card_beastmodes",
    "get_dataset_beastmodes",
    "get_page_beastmodes",
]

from typing import Optional

import httpx

from ..client import get_data as gd
from ..client import response as rgd
from ..client.auth import DomoAuth
from ..client.entities import DomoEnum
from ..client.exceptions import RouteError
from ..utils import chunk_execution as dmce


class BeastMode_GET_Error(RouteError):
    """Raised when BeastMode retrieval operations fail."""

    def __init__(
        self,
        beastmode_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or "BeastMode retrieval failed",
            entity_id=beastmode_id,
            response_data=response_data,
            **kwargs,
        )


class BeastMode_CRUD_Error(RouteError):
    """Raised when BeastMode create, update, or delete operations fail."""

    def __init__(
        self,
        operation: str,
        beastmode_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"BeastMode {operation} operation failed",
            entity_id=beastmode_id,
            response_data=response_data,
            **kwargs,
        )


class Search_BeastModeLink(DomoEnum):
    CARD = "CARD"
    DATASOURCE = "DATA_SOURCE"


def generate_beastmode_body(
    name: Optional[str] = None,
    filters: Optional[list[dict]] = None,
    is_unlocked: Optional[bool] = None,
    is_not_variable: Optional[bool] = None,
    link: Optional[Search_BeastModeLink] = None,
):
    filters = filters or []

    body = {}
    if name:
        body.update({"name": name})

    return {
        "name": "",
        "filters": [{"field": "notvariable"}, *filters],
        "sort": {"field": "name", "ascending": True},
    }


@gd.route_function
async def search_beastmodes(
    auth: DomoAuth,
    filters: Optional[list[dict]] = None,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    debug_loop: bool = False,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    offset_params = {
        "offset": "offset",
        "limit": "limit",
    }
    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/functions/search"

    body = generate_beastmode_body(filters)

    def arr_fn(res) -> list[dict]:
        return res.response["results"]

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        arr_fn=arr_fn,
        body=body,
        offset_params_in_body=True,
        offset_params=offset_params,
        loop_until_end=True,
        session=session,
        debug_loop=debug_loop,
        debug_api=debug_api,
        return_raw=return_raw,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise BeastMode_GET_Error(response_data=res)

    return res


@gd.route_function
async def lock_beastmode(
    beastmode_id: str,
    is_locked: bool,
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/functions/template/{beastmode_id}"

    body = {"locked": is_locked}

    res = await gd.get_data(
        auth=auth,
        method="PUT",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise BeastMode_CRUD_Error(
            operation="lock", beastmode_id=beastmode_id, response_data=res
        )

    return res


@gd.route_function
async def get_beastmode_by_id(
    beastmode_id: str,
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/functions/template/{beastmode_id}"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise BeastMode_GET_Error(beastmode_id=beastmode_id, response_data=res)

    return res


async def get_card_beastmodes(
    card_id: str,
    auth: DomoAuth,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    debug_num_stacks_to_drop: int = 2,
    return_raw: bool = False,
):
    res = await search_beastmodes(
        auth=auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    all_bms = res.response

    filter_bms = [
        bm
        for bm in all_bms
        if any(
            [
                True
                for link in bm["links"]
                if link["resource"]["type"] == "CARD"
                and link["resource"]["id"] == card_id
            ]
        )
    ]

    return [
        {
            "id": bm["id"],
            "name": bm["name"],
            "locked": bm["locked"],
            "legacyId": bm["legacyId"],
            "status": bm["status"],
            "links": bm["links"],
        }
        for bm in filter_bms
    ]


async def get_dataset_beastmodes(
    dataset_id: str,
    auth: DomoAuth,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    debug_num_stacks_to_drop: int = 2,
    return_raw: bool = False,
):
    all_bms = (
        await search_beastmodes(
            auth=auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )
    ).response

    filter_bms = [
        bm
        for bm in all_bms
        if any(
            [
                True
                for link in bm["links"]
                if link["resource"]["type"] == "DATA_SOURCE"
                and link["resource"]["id"] == dataset_id
            ],
        )
    ]

    if return_raw:
        return filter_bms

    return [
        {
            "id": bm["id"],
            "name": bm["name"],
            "locked": bm["locked"],
            "legacyId": bm["legacyId"],
            "status": bm["status"],
            "links": bm["links"],
        }
        for bm in filter_bms
    ]


async def get_page_beastmodes(page_id: str, auth: DomoAuth):
    from . import page as page_routes

    page_definition = (
        await page_routes.get_page_definition(page_id=page_id, auth=auth)
    ).response

    card_ids = [card["id"] for card in page_definition["cards"]]

    # the gather_with_concurrency returns a list (cards in the page) of lists (bms in the card).  use list comprehension to make one big list
    page_card_bms = await dmce.gather_with_concurrency(
        *[get_card_beastmodes(card_id=card_id, auth=auth) for card_id in card_ids], n=5
    )
    page_card_bms = [
        bm for card_bms in page_card_bms for bm in card_bms
    ]  # flattens list

    bms = []
    for bm in page_card_bms:
        if bm["id"] in [f["id"] for f in bms]:
            bms.append(bm)

    return bms
