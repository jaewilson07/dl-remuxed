__all__ = ["GetGrants_Error", "get_grants"]

import httpx

from ..client import DomoAuth as dmda
from ..client import DomoError as de
from ..client import ResponseGetData as rgd
from ..client import get_data as gd


class GetGrants_Error(de.RouteError):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


async def get_grants(
    auth: dmda.DomoAuth, debug_api: bool = False, session: httpx.AsyncClient = None
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/authorization/v1/authorities"

    res = await gd.get_data(
        auth=auth, url=url, method="GET", debug_api=debug_api, session=session
    )

    if not res.is_success:
        raise GetGrants_Error(res=res)

    if len(res.response) == 0:
        raise GetGrants_Error(
            res=res,
            message=f"{len(res.response)} grants returned",
        )

    return res
