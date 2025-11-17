__all__ = [
    "Config_GET_Error",
    "get_allowlist",
    "AllowlistUnableToUpdate",
    "set_allowlist",
    "get_allowlist_is_filter_all_traffic_enabled",
    "toggle_allowlist_is_filter_all_traffic_enabled",
]


from typing import Optional

import httpx

from ... import auth as dmda
from ...auth import DomoAuth
from ...base import exceptions as dmde
from ...client import (
    get_data as gd,
    response as rgd,
)
from ...client.context import RouteContext
from ...utils.convert import convert_string_to_bool
from .exceptions import Config_GET_Error


class AllowlistUnableToUpdate(dmde.RouteError):
    def __init__(self, res: rgd.ResponseGetData, reason: str = "", message: str = ""):
        if reason:
            reason_str = f"unable to update allowlist: {reason}"
            if message:
                message += f" | {reason_str}"

        super().__init__(
            res=res,
            message=message,
        )


@gd.route_function
async def get_allowlist(
    auth: DomoAuth,
    *,  # Make following params keyword-only
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    return_raw: bool = False,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    """Get the IP allowlist for the Domo instance.

    Args:
        auth: Authentication object
        context: Route context with execution parameters (overrides individual params if provided)
        session: Optional httpx client session
        return_raw: Return raw response without processing
        debug_api: Enable API debugging
        parent_class: Parent class name for logging
        debug_num_stacks_to_drop: Stack frames to drop in logging

    Returns:
        ResponseGetData with list of allowed IP addresses

    Raises:
        Config_GET_Error: If retrieval fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/admin/companysettings/whitelist"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        headers={"accept": "*/*"},
        context=context,
        is_follow_redirects=True,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_GET_Error(res=res)

    res.response = (
        res.response.get("addresses", []) if isinstance(res.response, dict) else []
    )

    if res.response == [""]:
        res.response = []

    return res


@gd.route_function
async def set_allowlist(
    auth: DomoAuth,
    ip_address_ls: list[str],
    *,  # Make following params keyword-only
    context: RouteContext | None = None,
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient | None = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    """Set the IP allowlist for the Domo instance.

    Note: companysettings/whitelist API only allows users to SET the allowlist,
    does not allow INSERT or UPDATE operations.

    Args:
        auth: Authentication object
        ip_address_ls: List of IP addresses or CIDR blocks to set as allowlist
        context: Route context with execution parameters (overrides individual params if provided)
        debug_api: Enable API debugging
        return_raw: Return raw response without processing
        session: Optional httpx client session
        parent_class: Parent class name for logging
        debug_num_stacks_to_drop: Stack frames to drop in logging

    Returns:
        ResponseGetData with operation result

    Raises:
        AllowlistUnableToUpdate: If update fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/admin/companysettings/whitelist"

    body = {"addresses": ip_address_ls}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        context=context,
        is_follow_redirects=True,
        headers={"accept": "text/plain"},
    )
    if return_raw:
        return res

    if not res.is_success:
        raise AllowlistUnableToUpdate(res=res, reason=str(res.response))

    return res


@gd.route_function
async def get_allowlist_is_filter_all_traffic_enabled(
    auth: DomoAuth,
    *,  # Make following params keyword-only
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    return_raw: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    """Get whether ALL traffic is filtered through the allowlist or just browser traffic.

    This endpoint determines if ALL traffic is filtered through the allowlist
    or just browser traffic. Located at: Admin > Company Settings > Security > IP Allowlist

    Args:
        auth: Authentication object
        context: Route context with execution parameters (overrides individual params if provided)
        session: Optional httpx client session
        debug_api: Enable API debugging
        return_raw: Return raw response without processing
        parent_class: Parent class name for logging
        debug_num_stacks_to_drop: Stack frames to drop in logging

    Returns:
        ResponseGetData with is_enabled (bool) and feature name
        - True: all traffic is filtered
        - False: only browser traffic is filtered

    Raises:
        Config_GET_Error: If retrieval fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/ip.whitelist.mobile.enabled"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
        is_follow_redirects=True,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_GET_Error(res=res)

    res.response = {
        "is_enabled": (
            convert_string_to_bool(res.response.get("value", False))
            if isinstance(res.response, dict)
            else False
        ),
        "feature": "ip.whitelist.mobile.enabled",
    }

    return res


@gd.route_function
async def toggle_allowlist_is_filter_all_traffic_enabled(
    auth: dmda.DomoFullAuth,
    is_enabled: bool,
    *,  # Make following params keyword-only
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    return_raw: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    """Toggle whether ALL traffic is filtered through the allowlist or just browser traffic.

    This endpoint determines if ALL traffic is filtered through the allowlist
    or just browser traffic. Located at: Admin > Company Settings > Security > IP Allowlist

    Args:
        auth: Full authentication object (requires admin credentials)
        is_enabled: True to filter all traffic, False to filter only browser traffic
        context: Route context with execution parameters (overrides individual params if provided)
        session: Optional httpx client session
        debug_api: Enable API debugging
        return_raw: Return raw response without processing
        parent_class: Parent class name for logging
        debug_num_stacks_to_drop: Stack frames to drop in logging

    Returns:
        ResponseGetData with updated setting (or raw response if return_raw=True)

    Raises:
        AllowlistUnableToUpdate: If update fails
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/ip.whitelist.mobile.enabled"

    body = {"value": is_enabled}

    res = await gd.get_data(
        auth=auth,  # type: ignore[arg-type]
        url=url,
        method="PUT",
        body=body,
        context=context,
        is_follow_redirects=True,
    )

    if not res.is_success:
        raise AllowlistUnableToUpdate(res=res, reason=str(res.response))

    if return_raw:
        return res

    return await get_allowlist_is_filter_all_traffic_enabled(
        auth=auth,
        context=context,
    )
