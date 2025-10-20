__all__ = [
    "Stream_GET_Error",
    "Stream_CRUD_Error",
    "get_streams",
    "get_stream_by_id",
    "update_stream",
    "create_stream",
    "execute_stream",
]

from typing import Optional

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd


class Stream_GET_Error(RouteError):
    """Raised when stream retrieval operations fail."""

    def __init__(
        self,
        stream_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or "Stream retrieval failed",
            entity_id=stream_id,
            response_data=response_data,
            **kwargs,
        )


class Stream_CRUD_Error(RouteError):
    """Raised when stream create, update, delete, or execute operations fail."""

    def __init__(
        self,
        operation: str,
        stream_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"Stream {operation} operation failed",
            entity_id=stream_id,
            response_data=response_data,
            **kwargs,
        )


@gd.route_function
async def get_streams(
    auth: DomoAuth,
    loop_until_end: bool = True,
    session: Optional[httpx.AsyncClient] = None,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    debug_api: bool = False,
    debug_loop: bool = False,
    return_raw: bool = False,
    skip: int = 0,
    maximum: int = 1000,
) -> rgd.ResponseGetData:
    """
    streams do not appear to be recycled, not recommended for use as will return a virtually limitless number of streams
    instead use get_stream_by_id
    """

    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/streams/"

    def arr_fn(res):
        return res.response

    res = await gd.looper(
        auth=auth,
        session=session,
        url=url,
        offset_params={"limit": "limit", "offset": "offet"},
        arr_fn=arr_fn,
        loop_until_end=loop_until_end,
        method="GET",
        offset_params_in_body=False,
        limit=500,
        skip=skip,
        maximum=maximum,
        debug_api=debug_api,
        debug_loop=debug_loop,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        return_raw=return_raw,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Stream_GET_Error(response_data=res)

    return res


@gd.route_function
async def get_stream_by_id(
    auth: DomoAuth,
    stream_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/streams/{stream_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise Stream_GET_Error(stream_id=stream_id, response_data=res)

    return res


@gd.route_function
async def update_stream(
    auth: DomoAuth,
    stream_id: str,
    body: dict,
    session: Optional[httpx.AsyncClient] = None,
    debug_num_stacks_to_drop: int = 1,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/streams/{stream_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        body=body,
        method="PUT",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise Stream_CRUD_Error(
            operation="update", stream_id=stream_id, response_data=res
        )

    return res


@gd.route_function
async def create_stream(
    auth: DomoAuth,
    body: dict,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/streams"

    res = await gd.get_data(
        auth=auth,
        url=url,
        body=body,
        method="POST",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise Stream_CRUD_Error(operation="create", response_data=res)

    return res


@gd.route_function
async def execute_stream(
    auth: DomoAuth,
    stream_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/streams/{stream_id}/executions"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise Stream_CRUD_Error(
            operation="execute", stream_id=stream_id, response_data=res
        )

    return res
