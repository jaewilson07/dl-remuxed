__all__ = [
    "InstanceSwitcher_GET_Error",
    "InstanceSwitcher_CRUD_Error",
    "get_instance_switcher_mapping",
    "set_instance_switcher_mapping",
]

<<<<<<< HEAD
from typing import List, Optional

import httpx

<<<<<<<< HEAD:src/routes/instance_config_instance_switcher.py
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd
========
from ..client import get_data as gd, response as rgd
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
>>>>>>>> test:src/domolibrary2/routes/instance_config_instance_switcher.py


class InstanceSwitcherMapping_GET_Error(RouteError):
    """Raised when instance switcher mapping retrieval operations fail."""

<<<<<<<< HEAD:src/routes/instance_config_instance_switcher.py
    def __init__(
        self, message: Optional[str] = None, response_data=None, **kwargs
    ):
        super().__init__(
            message=message or "Instance switcher mapping retrieval failed",
            response_data=response_data,
========
    def __init__(self, message: Optional[str] = None, res=None, **kwargs):
        super().__init__(
            message=message or "Instance switcher mapping retrieval failed",
            res=res,
>>>>>>>> test:src/domolibrary2/routes/instance_config_instance_switcher.py
=======
from typing import Optional

import httpx

from ..client import (
    get_data as gd,
    response as rgd,
)
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError


class InstanceSwitcher_GET_Error(RouteError):
    """Raised when instance switcher mapping retrieval operations fail."""

    def __init__(
        self,
        entity_id: Optional[str] = None,
        res=None,
        message: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            message=message or "Instance switcher mapping retrieval failed",
            entity_id=entity_id,
            res=res,
>>>>>>> main
            **kwargs,
        )


<<<<<<< HEAD
class InstanceSwitcherMapping_CRUD_Error(RouteError):
=======
class InstanceSwitcher_CRUD_Error(RouteError):
>>>>>>> main
    """Raised when instance switcher mapping create, update, or delete operations fail."""

    def __init__(
        self,
<<<<<<< HEAD
        operation: str = "update",
        message: Optional[str] = None,
<<<<<<<< HEAD:src/routes/instance_config_instance_switcher.py
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"Instance switcher mapping {operation} operation failed",
            response_data=response_data,
========
        res=None,
=======
        operation: str,
        entity_id: Optional[str] = None,
        res=None,
        message: Optional[str] = None,
>>>>>>> main
        **kwargs,
    ):
        super().__init__(
            message=message
            or f"Instance switcher mapping {operation} operation failed",
<<<<<<< HEAD
            res=res,
>>>>>>>> test:src/domolibrary2/routes/instance_config_instance_switcher.py
=======
            entity_id=entity_id,
            res=res,
            additional_context={"operation": operation},
>>>>>>> main
            **kwargs,
        )


# gets existing instance switcher mapping, response = list[dict]
@gd.route_function
async def get_instance_switcher_mapping(
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
<<<<<<< HEAD
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    timeout: int = 20,
) -> rgd.ResponseGetData:
=======
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
    timeout: int = 20,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Retrieve instance switcher mapping configuration.

    Gets the existing instance switcher mappings which define how users are
    routed to different Domo instances based on user attributes.

    Args:
        auth: Authentication object containing instance and credentials
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing
        timeout: Request timeout in seconds (default: 20)

    Returns:
        ResponseGetData object containing list of instance switcher mappings

    Raises:
        InstanceSwitcher_GET_Error: If retrieval operation fails
    """
>>>>>>> main
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

<<<<<<< HEAD
    if not res.is_success:
        raise InstanceSwitcherMapping_GET_Error(
            message=f"failed to retrieve instance switcher mapping - {res.response}",
<<<<<<<< HEAD:src/routes/instance_config_instance_switcher.py
            response_data=res,
========
            res=res,
>>>>>>>> test:src/domolibrary2/routes/instance_config_instance_switcher.py
=======
    if return_raw:
        return res

    if not res.is_success:
        raise InstanceSwitcher_GET_Error(
            message=f"failed to retrieve instance switcher mapping - {res.response}",
            res=res,
>>>>>>> main
        )

    return res


# update the instance switcher mappings
@gd.route_function
async def set_instance_switcher_mapping(
    auth: DomoAuth,
<<<<<<< HEAD
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

=======
    mapping_payloads: list[dict],
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
    timeout: int = 60,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Update instance switcher mapping configuration.

    Sets or updates the instance switcher mappings which define how users are
    routed to different Domo instances based on user attributes.

    Args:
        auth: Authentication object containing instance and credentials
        mapping_payloads: List of mapping configurations, each with format:
            {'userAttribute': 'attribute_name', 'instance': 'instance.domo.com'}
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing
        timeout: Request timeout in seconds (default: 60)

    Returns:
        ResponseGetData object with success message

    Raises:
        InstanceSwitcher_CRUD_Error: If update operation fails

    Example:
        >>> mapping_payloads = [
        ...     {'userAttribute': 'test1', 'instance': 'test.domo.com'},
        ...     {'userAttribute': 'test2', 'instance': 'prod.domo.com'}
        ... ]
        >>> await set_instance_switcher_mapping(auth, mapping_payloads)
>>>>>>> main
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

<<<<<<< HEAD
    if not res.is_success:
        raise InstanceSwitcherMapping_CRUD_Error(
            operation="update",
            message=f"failed to update instance switcher mappings - {res.response}",
<<<<<<<< HEAD:src/routes/instance_config_instance_switcher.py
            response_data=res,
========
            res=res,
>>>>>>>> test:src/domolibrary2/routes/instance_config_instance_switcher.py
=======
    if return_raw:
        return res

    if not res.is_success:
        raise InstanceSwitcher_CRUD_Error(
            operation="update",
            message=f"failed to update instance switcher mappings - {res.response}",
            res=res,
>>>>>>> main
        )

    res.response = "success: updated instance switcher mappings"
    return res
