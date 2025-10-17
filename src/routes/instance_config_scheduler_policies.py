__all__ = [
    "Scheduler_Policies_Error",
    "get_scheduler_policies",
    "get_scheduler_policy_by_id",
    "create_scheduler_policy",
    "update_scheduler_policy",
    "delete_policy",
]

from typing import Any, Optional

import httpx

from ..client import DomoAuth as dmda
from ..client import DomoError as dmde
from ..client import get_data as gd
from ..client import ResponseGetData as rgd


class Scheduler_Policies_Error(dmde.RouteError):
    def __init__(
        self, res: rgd.ResponseGetData, policy_id: str = "", message: str = ""
    ):
        super().__init__(res=res, message=message, entity_id=policy_id)


@gd.route_function
async def get_scheduler_policies(
    auth: dmda.DomoAuth,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
    return_raw: bool = False,
):
    """
    Retrieves a list of all the scheduler policies.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/metrics/v1/usage/policies"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )
    if return_raw:
        return res

    if res.status == 403 and res.response.startswith("Forbidden"):
        raise Scheduler_Policies_Error(
            res=res,
            message="error retrieving permissions, is the feature switch enabled?",
        )

    if res and not res.is_success:
        raise Scheduler_Policies_Error(res=res)
    return res


@gd.route_function
async def get_scheduler_policy_by_id(
    auth: dmda.DomoAuth,
    policy_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Wrapper function to retrieve a specific Scheduler Policy by ID. Direct get is not available.
    """

    res = await get_scheduler_policies(
        auth=auth,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    match_policy = next(
        (policy for policy in res.response if policy["id"] == policy_id), None
    )

    if not match_policy:
        raise Scheduler_Policies_Error(
            res=rgd.ResponseGetData(
                status=404,
                response=f"Policy with ID {policy_id} not found",
                is_success=False,
            )
        )

    res.response = match_policy
    return res


@gd.route_function
async def create_scheduler_policy(
    auth: dmda.DomoAuth,
    create_body: dict[str, Any],
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
    return_raw: bool = False,
):
    """
    Creates a new Scheduler Policy.
    """

    # basic input validation for clearer error messages
    if not isinstance(create_body["frequencies"], dict) or not all(
        isinstance(v, int) for v in create_body["frequencies"].values()
    ):
        raise Scheduler_Policies_Error(
            res=rgd.ResponseGetData(
                status=400,
                response="frequencies must be a dict[str, int]",
                is_success=False,
            )
        )

    if not isinstance(create_body["members"], list) or not all(
        isinstance(m, dict) and "type" in m and "id" in m
        for m in create_body["members"]
    ):
        raise Scheduler_Policies_Error(
            res=rgd.ResponseGetData(
                status=400,
                response="members must be a list of dicts with 'type' and 'id'",
                is_success=False,
            )
        )

    url = f"https://{auth.domo_instance}.domo.com/api/metrics/v1/usage/policies"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=create_body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
        return_raw=return_raw,
    )

    if return_raw:
        return res

    if res and not res.is_success:
        raise Scheduler_Policies_Error(res=res)

    return res


@gd.route_function
async def update_scheduler_policy(
    auth: dmda.DomoAuth,
    policy_id: str,
    update_body: dict[str, Any],
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Updates a Scheduler Policy.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/metrics/v1/usage/policies/{policy_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=update_body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
        return_raw=return_raw,
    )

    if return_raw:
        return res

    if res and not res.is_success:
        raise Scheduler_Policies_Error(res=res)

    return res


@gd.route_function
async def delete_policy(
    auth: dmda.DomoAuth,
    policy_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Deletes a Cloud Amplifier integration.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/metrics/v1/usage/policies/{policy_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="DELETE",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if res and not res.is_success:
        raise Scheduler_Policies_Error(res=res)
    return res