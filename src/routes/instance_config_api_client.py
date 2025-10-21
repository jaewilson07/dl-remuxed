__all__ = [
    "ApiClient_GET_Error",
    "get_api_clients",
    "get_client_by_id",
    "ApiClient_CRUD_Error",
    "ApiClient_ScopeEnum",
    "create_api_client",
    "ApiClient_RevokeError",
    "revoke_api_client",
]

from enum import Enum
import datetime as dt
from typing import List

import httpx

from ..client import auth as dmda
from ..client import exceptions as dmde
from ..client import get_data as gd
from ..client import response as rgd
from ..client.entities import DomoEnumMixin


class ApiClient_GET_Error(dmde.RouteError):
    def __init__(self, res: rgd.ResponseGetData, message=None):
        super().__init__(res=res, message=message)


@gd.route_function
async def get_api_clients(
    auth: DomoAuth,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
    # return_raw: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/developer-tokens"

    res = await gd.get_data(
        url=url,
        method="GET",
        auth=auth,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )
    if not res.is_success:
        raise ApiClient_GET_Error(res=res)

    # if return_raw:
    #     return res

    # API response change 6/10/2025
    # res.response = res.response["entries"]

    return res


@gd.route_function
async def get_client_by_id(
    auth: DomoAuth,
    client_id: int,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    res = await get_api_clients(
        auth=auth,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        session=session,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    client = next(obj for obj in res.response if obj.get("id") == int(client_id))
    res.response = client
    return res


### NOT SUPPORTED

# @gd.route_function
# async def get_client_by_id(
#     auth: DomoAuth,
#     client_id : str,
#     debug_api: bool = False,
#     debug_num_stacks_to_drop=1,
#     parent_class=None,
#     session: httpx.AsyncClient = None,
#     return_raw: bool = False,
# ) -> rgd.ResponseGetData:

#     url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/developer-tokens/{client_id}"

#     res = await gd.get_data(
#         url=url,
#         method="GET",
#         auth=auth,
#         debug_api=debug_api,
#         parent_class=parent_class,
#         num_stacks_to_drop=debug_num_stacks_to_drop,
#         session=session,
#     )
#     if not res.is_success:
#         raise ApiClient_GET_Error(res=res)

#     if return_raw:
#         return res

#     res.response = res.response["entries"]

#     return res


class ApiClient_CRUD_Error(dmde.RouteError):
    def __init__(self, res: rgd.ResponseGetData, message: str = None):
        super().__init__(res=res, message=message)


class ApiClient_ScopeEnum(DomoEnumMixin, Enum):
    DATA = "data"
    WORKFLOW = "workflow"
    AUDIT = "audit"
    BUZZ = "buzz"
    USER = "user"
    ACCOUNT = "account"
    DASHBOARD = "dashboard"


@gd.route_function
async def create_api_client(
    auth: dmda.DomoFullAuth,  # usernme and password (full) auth required for this API
    client_name: str,
    client_description: str = f"generated via DL {str(dt.date.today()).replace('-', '')}",
    scope: List[ApiClient_ScopeEnum] = None,  # defaults to [data, audit]
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
) -> rgd.ResponseGetData:
    if not isinstance(auth, dmda.DomoFullAuth):
        raise dmda.InvalidAuthTypeError(required_auth_type=dmda.DomoFullAuth)

    if scope and isinstance(scope, list) and isinstance(scope[0], ApiClient_ScopeEnum):
        scope = [sc.value for sc in scope]

    if not scope:
        scope = ["data", "audit"]

    url = "https://api.domo.com/clients"

    headers = {"X-DOMO-CustomerDomain": f"{auth.domo_instance}.domo.com"}

    res = await gd.get_data(
        url=url,
        method="POST",
        auth=auth,
        body={"name": client_name, "description": client_description, "scope": scope},
        headers=headers,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )

    if not res.is_success:
        if res.status == 400:
            raise ApiClient_CRUD_Error(
                res, message=f"{res.response} -- does the client already exist?"
            )

        # if res.status == 403: # invalid auth type, but will be caught by the earlier test

        raise ApiClient_CRUD_Error(res)

    return res


class ApiClient_RevokeError(dmde.RouteError):
    def __init__(
        self,
        res: rgd.ResponseGetData,
        client_id: str = None,
        message: str = None,
    ):
        super().__init__(
            res=res,
            message=message or f"error revoking client {client_id}",
        )


@gd.route_function
async def revoke_api_client(
    auth: DomoAuth,
    client_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/developer-tokens/{client_id}"

    res = await gd.get_data(
        url=url,
        method="DELETE",
        auth=auth,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )
    if not res.is_success:
        if res.status == 400:
            raise ApiClient_RevokeError(
                message=f"error revoking client {client_id}, validate that it exists.",
                res=res,
            )
        raise ApiClient_RevokeError(client_id=client_id, res=res)

    res.response = f"client {client_id} revoked"

    return res
