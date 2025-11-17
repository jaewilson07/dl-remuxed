__all__ = [
    "GetDomainsNotFoundError",
    "GetAppDomainsNotFoundError",
    "get_authorized_domains",
    "set_authorized_domains",
    "get_authorized_custom_app_domains",
    "set_authorized_custom_app_domains",
]

from typing import Optional

import httpx

from ...auth import DomoAuth
from ...client import (
    get_data as gd,
    response as rgd,
)
from ...client.context import RouteContext
from .. import user as user_routes
from .exceptions import Config_CRUD_Error, Config_GET_Error


class GetDomainsNotFoundError(Config_GET_Error):
    def __init__(self, res: rgd.ResponseGetData, message: str = ""):
        super().__init__(res=res, message=message)


class GetAppDomainsNotFoundError(Config_GET_Error):
    def __init__(self, res: rgd.ResponseGetData, message: str = ""):
        super().__init__(res=res, message=message)


@gd.route_function
async def get_authorized_domains(
    auth: DomoAuth,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get authorized domains for the Domo instance.

    Args:
        auth: Authentication object containing credentials and instance info
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing authorized domains list

    Raises:
        GetDomainsNotFoundError: If domains retrieval fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-domains"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
    )

    if return_raw:
        return res

    # domo raises a 404 error even if the success is valid but there are no approved domains
    if res.status == 404 and res.response == "Not Found":
        res_test = await user_routes.get_all_users(auth=auth)

        if not res_test.is_success:
            raise GetDomainsNotFoundError(res=res)

        if res_test.is_success:
            res.status = 200
            res.is_success = True
            res.response = []

        return res

    if not res.is_success:
        raise GetDomainsNotFoundError(res=res)

    res.response = [domain.strip() for domain in res.response.get("value").split(",")]  # type: ignore
    return res


@gd.route_function
async def set_authorized_domains(
    auth: DomoAuth,
    authorized_domain_ls: list[str],
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    """Set authorized domains for the Domo instance.

    Args:
        auth: Authentication object containing credentials and instance info
        authorized_domain_ls: List of domain strings to authorize
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context

    Returns:
        ResponseGetData object containing updated authorized domains list

    Raises:
        Config_CRUD_Error: If setting domains fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-domains"

    body = {"name": "authorized-domains", "value": ",".join(authorized_domain_ls)}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        context=context,
    )

    if not res.is_success:
        raise Config_CRUD_Error(res=res)

    return await get_authorized_domains(
        auth=auth,
        context=context,
    )


@gd.route_function
async def get_authorized_custom_app_domains(
    auth: DomoAuth,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get authorized custom app domains for the Domo instance.

    Args:
        auth: Authentication object containing credentials and instance info
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing authorized custom app domains list

    Raises:
        GetAppDomainsNotFoundError: If app domains retrieval fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-app-domains"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
    )

    if return_raw:
        return res

    # domo raises a 404 error even if the success is valid but there are no approved domains
    if res.status == 404 and res.response == "Not Found":
        res_test = await user_routes.get_all_users(auth=auth)

        if not res_test.is_success:
            raise GetAppDomainsNotFoundError(res=res)

        if res_test.is_success:
            res.status = 200
            res.is_success = True
            res.response = []

        return res

    if not res.is_success:
        raise GetAppDomainsNotFoundError(res=res)

    res.response = [domain.strip() for domain in res.response.get("value").split(",")]  # type: ignore
    return res


@gd.route_function
async def set_authorized_custom_app_domains(
    auth: DomoAuth,
    authorized_custom_app_domain_ls: list[str],
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    """Set authorized custom app domains for the Domo instance.

    Args:
        auth: Authentication object containing credentials and instance info
        authorized_custom_app_domain_ls: List of custom app domain strings to authorize
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context

    Returns:
        ResponseGetData object containing updated authorized custom app domains list

    Raises:
        Config_CRUD_Error: If setting custom app domains fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/authorized-app-domains"

    body = {
        "name": "authorized-app-domains",
        "value": ",".join(authorized_custom_app_domain_ls),
    }

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        context=context,
    )

    if not res.is_success:
        raise Config_CRUD_Error(res=res)

    return await get_authorized_custom_app_domains(
        auth=auth,
        context=context,
    )
