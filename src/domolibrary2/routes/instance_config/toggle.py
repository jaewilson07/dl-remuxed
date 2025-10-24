__all__ = [
    "ToggleConfig_CRUD_Error",
    "get_is_invite_social_users_enabled",
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
from typing import Optional

from ...client import (
    get_data as gd,
    response as rgd,
)
from ...client.auth import DomoAuth
from ...utils.convert import convert_string_to_bool
from .exceptions import Config_CRUD_Error, Config_GET_Error


class ToggleConfig_CRUD_Error(Config_CRUD_Error):
    def __init__(self, res: rgd.ResponseGetData, message=None):
        super().__init__(res=res, message=message)


@gd.route_function
async def get_is_invite_social_users_enabled(
    auth: DomoAuth,
    customer_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    parent_class=None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:
    # must pass the customer as the short form API endpoint (without customer_id) does not support a GET request
    # url = f"https://{auth.domo_instance}.domo.com/api/content/v3/customers/features/free-invite"

    url = f"https://{auth.domo_instance}.domo.com/api/content/v3/customers/{customer_id}/features/free-invite"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
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
async def get_is_user_invite_notifications_enabled(
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    parent_class=None,
    debug_num_stacks_to_drop=1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/user.invite.email.enabled"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_GET_Error(res=res)

    res.response = {
        "name": "user.invite.email.enabled",
        "is_enabled": convert_string_to_bool(res.response["value"]),
    }

    return res


@gd.route_function
async def toggle_is_user_invite_enabled(
    auth: DomoAuth,
    is_enabled: bool,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    return_raw: bool = False,
    parent_class=None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:
    """
    Admin > Company Settings > Notifications
    """

    url = f"https://{auth.domo_instance}.domo.com/api/customer/v1/properties/user.invite.email.enabled"

    body = {"value": is_enabled}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ToggleConfig_CRUD_Error(res=res, message=res.response)

    if return_raw:
        return res

    return await get_is_user_invite_notifications_enabled(
        auth=auth,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )


@gd.route_function
async def get_is_weekly_digest_enabled(
    auth: DomoAuth,
    return_raw: bool = False,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/come-back-to-domo-all-users"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
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
    return_raw: bool = False,
    debug_api: bool = False,
    is_enabled: bool = True,
    session: Optional[httpx.AsyncClient] = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/customer-states/come-back-to-domo-all-users"

    body = {"name": "come-back-to-domo-all-users", "value": is_enabled}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Config_CRUD_Error(res=res)

    return await get_is_weekly_digest_enabled(
        auth=auth,
        debug_api=debug_api,
        parent_class=parent_class,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )


@gd.route_function
async def get_is_left_nav_enabled_v1(
    auth: DomoAuth,
    return_raw: bool = False,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    """
    2025-09-15 -- deprecated
    """

    url = f"https://{auth.domo_instance}.domo.com/api/nav/v1/leftnav/customer"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
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
    return_raw: bool = False,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    """
    2025-09-15 current version of leftnav enabled
    """

    url = f"https://{auth.domo_instance}.domo.com/api/nav/v1/leftnav/enabled"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
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
    return_raw: bool = False,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    """
    2025-09-15 -- deprecated
    """

    url = f"https://{auth.domo_instance}.domo.com/api/nav/v1/leftnav/customer"

    params = {"use-left-nav": is_use_left_nav}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        params=params,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
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
    return_raw: bool = False,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    """
    2025-09-15 -- switched to new leftnav API
    """

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
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
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
