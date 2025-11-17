__all__ = [
    "ToggleConfig_CRUD_Error",
    "get_is_invite_social_users_enabled",
    "toggle_is_invite_social_users_enabled",
    "get_is_user_invite_notifications_enabled",
    "toggle_is_user_invite_enabled",
    "get_is_weekly_digest_enabled",
    "toggle_is_weekly_digest_enabled",
    "get_is_left_nav_enabled_v1",
    "get_is_left_nav_enabled",
    "toggle_is_left_nav_enabled_v1",
    "toggle_is_left_nav_enabled",
]


import httpx

from ...auth import DomoAuth
from ...client import (
    get_data as gd,
    response as rgd,
)
from ...client.context import RouteContext
from ...utils.convert import convert_string_to_bool
from .exceptions import Config_CRUD_Error, Config_GET_Error


class ToggleConfig_CRUD_Error(Config_CRUD_Error):
    def __init__(self, res: rgd.ResponseGetData, message=None):
        super().__init__(res=res, message=message)


@gd.route_function
async def get_is_invite_social_users_enabled(
    auth: DomoAuth,
    customer_id: str,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get whether social user invites are enabled.

    Args:
        auth: Authentication object
        customer_id: Customer ID for the instance
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with invite configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    # must pass the customer as the short form API endpoint (without customer_id) does not support a GET request
    # url = f"https://{auth.domo_instance}.domo.com/api/content/v3/customers/features/free-invite"

    url = f"https://{auth.domo_instance}.domo.com/api/content/v3/customers/{customer_id}/features/free-invite"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_GET_Error(
            res=res,
        )

    res.response = {"name": "free-invite", "is_enabled": res.response["enabled"]}

    return res


@gd.route_function
async def toggle_is_invite_social_users_enabled(
    auth: DomoAuth,
    customer_id: str,
    is_enabled: bool,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Toggle whether social users can be invited to the instance.

    Args:
        auth: Authentication object
        customer_id: Customer ID for the instance
        is_enabled: True to enable social user invites, False to disable
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with the updated configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/content/v3/customers/{customer_id}/features/free-invite"

    body = {"enabled": is_enabled}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise ToggleConfig_CRUD_Error(
            res=res,
            message=f"Failed to toggle social user invites to {is_enabled}",
        )

    res.response = {"name": "free-invite", "is_enabled": is_enabled}

    return res


@gd.route_function
async def get_is_user_invite_notifications_enabled(
    auth: DomoAuth,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get whether user invite notifications are enabled.

    Args:
        auth: Authentication object
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with notification configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/user.invite.email.enabled"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_GET_Error(res=res)

    res.response = {
        "name": "user.invite.email.enabled",
        "is_enabled": (
            convert_string_to_bool(res.response.get("value", False))
            if isinstance(res.response, dict)
            else False
        ),
    }

    return res


@gd.route_function
async def toggle_is_user_invite_enabled(
    auth: DomoAuth,
    is_enabled: bool,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Toggle user invite notifications.

    Admin > Company Settings > Notifications

    Args:
        auth: Authentication object
        is_enabled: True to enable notifications, False to disable
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with updated configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/user.invite.email.enabled"

    body = {"value": is_enabled}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        context=context,
    )

    if not res.is_success:
        raise ToggleConfig_CRUD_Error(res=res, message=str(res.response))

    if return_raw:
        return res

    return await get_is_user_invite_notifications_enabled(
        auth=auth,
        context=context,
    )


@gd.route_function
async def get_is_weekly_digest_enabled(
    auth: DomoAuth,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get whether weekly digest emails are enabled.

    Args:
        auth: Authentication object
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with weekly digest configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/come-back-to-domo-all-users"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
    )

    if return_raw:
        return res

    if res.status == 404 and res.response == "Not Found":
        raise Config_CRUD_Error(res=res)

    if not res.is_success:
        raise Config_CRUD_Error(res=res)

    res.response = {
        "is_enabled": convert_string_to_bool(res.response["value"]),
        "feature": "come-back-to-domo-all-users",
    }

    return res


@gd.route_function
async def toggle_is_weekly_digest_enabled(
    auth: DomoAuth,
    is_enabled: bool = True,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Toggle weekly digest emails.

    Args:
        auth: Authentication object
        is_enabled: True to enable weekly digest, False to disable
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with updated configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/come-back-to-domo-all-users"

    body = {"name": "come-back-to-domo-all-users", "value": is_enabled}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_CRUD_Error(res=res)

    return await get_is_weekly_digest_enabled(
        auth=auth,
        context=context,
    )


@gd.route_function
async def get_is_left_nav_enabled_v1(
    auth: DomoAuth,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get whether left navigation is enabled (deprecated v1 API).

    2025-09-15 -- deprecated

    Args:
        auth: Authentication object
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with left nav configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/nav/v1/leftnav/customer"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_GET_Error(res=res)

    res.response = {
        "is_enabled": res.response or False,
        "feature": "use-left-nav",
    }

    return res


@gd.route_function
async def get_is_left_nav_enabled(
    auth: DomoAuth,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get whether left navigation is enabled (current API).

    2025-09-15 current version of leftnav enabled

    Args:
        auth: Authentication object
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with left nav configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/nav/v1/leftnav/enabled"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_GET_Error(res=res)

    res.response = {
        "is_enabled": res.response or False,
        "feature": "use-left-nav",
    }

    return res


@gd.route_function
async def toggle_is_left_nav_enabled_v1(
    auth: DomoAuth,
    is_use_left_nav: bool = True,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Toggle left navigation (deprecated v1 API).

    2025-09-15 -- deprecated

    Args:
        auth: Authentication object
        is_use_left_nav: True to enable left nav, False to disable
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with updated configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/nav/v1/leftnav/customer"

    params = {"use-left-nav": is_use_left_nav}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        params=params,
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise ToggleConfig_CRUD_Error(res=res)

    res.response = {
        "is_enabled": res.response,
        "feature": "use-left-nav",
    }

    return res


@gd.route_function
async def toggle_is_left_nav_enabled(
    auth: DomoAuth,
    is_use_left_nav: bool = True,
    *,
    context: RouteContext | None = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class=None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Toggle left navigation (current API).

    2025-09-15 -- switched to new leftnav API

    Args:
        auth: Authentication object
        is_use_left_nav: True to enable left nav, False to disable
        context: Optional RouteContext for consolidated parameters
        session: Optional httpx session
        debug_api: Enable debug output
        debug_num_stacks_to_drop: Stack frames to drop in error messages
        parent_class: Name of calling class
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData with updated configuration
    """
    if context is None:
        context = RouteContext(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/nav/v1/leftnav/customer-settings"

    if is_use_left_nav:
        body = {"enabled": "CUSTOMER"}
    else:
        body = {"enabled": "NONE"}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        context=context,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise ToggleConfig_CRUD_Error(res=res)

    res.response = {
        "is_enabled": res.response,
        "feature": "use-left-nav",
    }

    return res
