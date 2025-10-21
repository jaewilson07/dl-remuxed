__all__ = [
    "InstanceSwitcherMapping_GET_Error",
    "InstanceSwitcherMapping_CRUD_Error",
    "get_instance_switcher_mapping",
    "set_instance_switcher_mapping",
]

from typing import List, Optional

import httpx

from ..client import get_data as gd
from ..client import response as rgd
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError


class InstanceSwitcherMapping_GET_Error(RouteError):
    """Raised when instance switcher mapping retrieval operations fail."""

    def __init__(self, message: Optional[str] = None, res=None, **kwargs):
        super().__init__(
            message=message or "Instance switcher mapping retrieval failed",
            res=res,
            **kwargs,
        )


class InstanceSwitcherMapping_CRUD_Error(RouteError):
    """Raised when instance switcher mapping create, update, or delete operations fail."""

    def __init__(
        self,
        operation: str = "update",
        message: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message
            or f"Instance switcher mapping {operation} operation failed",
            res=res,
            **kwargs,
        )


# gets existing instance switcher mapping, response = list[dict]
@gd.route_function
async def get_instance_switcher_mapping(
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    timeout: int = 20,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/everywhere/admin/userattributeinstances"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        timeout=timeout,
    )

    if not res.is_success:
        raise InstanceSwitcherMapping_GET_Error(
            message=f"failed to retrieve instance switcher mapping - {res.response}",
            res=res,
        )

    return res


# update the instance switcher mappings
@gd.route_function
async def set_instance_switcher_mapping(
    auth: DomoAuth,
    mapping_payloads: List[dict],
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    timeout: int = 60,
) -> rgd.ResponseGetData:
    """
    accepts a list of instance_switcher_mappings format:
    mapping_payloads = [ {'userAttribute': 'test1','instance': 'test.domo.com'}]

    """

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/everywhere/admin/userattributeinstances"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        debug_api=debug_api,
        session=session,
        body=mapping_payloads,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        timeout=timeout,
    )

    if not res.is_success:
        raise InstanceSwitcherMapping_CRUD_Error(
            operation="update",
            message=f"failed to update instance switcher mappings - {res.response}",
            res=res,
        )

    res.response = "success: updated instance switcher mappings"
    return res
