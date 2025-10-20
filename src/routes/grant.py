__all__ = ["Grant_GET_Error", "get_grants"]

from typing import Optional

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd


class Grant_GET_Error(RouteError):
    """Raised when grant retrieval operations fail."""

    def __init__(
        self, message: Optional[str] = None, response_data=None, **kwargs
    ):
        super().__init__(
            message=message or "Grant retrieval failed",
            response_data=response_data,
            **kwargs,
        )


@gd.route_function
async def get_grants(
    auth: DomoAuth,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/authorization/v1/authorities"

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
        raise Grant_GET_Error(response_data=res)

    if len(res.response) == 0:
        raise Grant_GET_Error(
            message=f"{len(res.response)} grants returned",
            response_data=res,
        )

    return res
