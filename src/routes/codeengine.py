__all__ = [
    "CodeEngine_GET_Error",
    "CodeEngine_CRUD_Error",
    "get_packages",
    "CodeEngine_Package_Parts",
    "CodeEngine_FunctionCallError",
    "get_codeengine_package_by_id",
    "get_package_versions",
    "get_codeengine_package_by_id_and_version",
    "test_package_is_released",
    "test_package_is_identical",
]

from typing import Optional

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd
from ..client.entities import DomoEnum


class CodeEngine_GET_Error(RouteError):
    """Raised when CodeEngine retrieval operations fail."""

    def __init__(
        self,
        codeengine_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or "CodeEngine retrieval failed",
            entity_id=codeengine_id,
            response_data=response_data,
            **kwargs,
        )


class CodeEngine_CRUD_Error(RouteError):
    """Raised when CodeEngine create, update, or delete operations fail."""

    def __init__(
        self,
        operation: str,
        codeengine_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"CodeEngine {operation} operation failed",
            entity_id=codeengine_id,
            response_data=response_data,
            **kwargs,
        )


@gd.route_function
async def get_packages(
    auth: DomoAuth,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    url = f"http://{auth.domo_instance}.domo.com/api/codeengine/v2/packages"

    res = await gd.get_data(
        url=url,
        auth=auth,
        method="get",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
        is_follow_redirects=True,
    )

    if not res.is_success:
        raise CodeEngine_GET_Error(response_data=res)

    return res


class CodeEngine_Package_Parts(DomoEnum):
    VERSIONS = "versions"
    FUNCTIONS = "functions"
    CODE = "code"


class CodeEngine_FunctionCallError(RouteError):
    def __init__(self, message: str, auth: DomoAuth):
        super().__init__(message=message, domo_instance=auth.domo_instance)


@gd.route_function
async def get_codeengine_package_by_id(
    package_id: str,
    auth: DomoAuth,
    debug_api: bool = False,
    params: Optional[dict] = None,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    url = (
        f"https://{auth.domo_instance}.domo.com/api/codeengine/v2/packages/{package_id}"
    )

    if not package_id:
        raise CodeEngine_FunctionCallError(
            message="Package ID must be provided.",
            auth=auth,
        )

    params = params or {"parts": "versions"}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        params=params,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise CodeEngine_GET_Error(codeengine_id=package_id, response_data=res)

    return res


@gd.route_function
async def get_package_versions(
    auth: DomoAuth,
    package_id: str,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    session: Optional[httpx.AsyncClient] = None,
) -> rgd.ResponseGetData:
    """each package can have one or many version"""

    if not package_id:
        raise CodeEngine_FunctionCallError(
            message="Package ID must be provided.",
            auth=auth,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/codeengine/v2/packages/{package_id}/versions/"

    params = {"parts": "functions,code"}

    res = await gd.get_data(
        url=url,
        method="get",
        auth=auth,
        params=params,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if not res.is_success:
        raise CodeEngine_GET_Error(codeengine_id=package_id, response_data=res)

    return res


@gd.route_function
async def get_codeengine_package_by_id_and_version(
    package_id: str,
    version: str,
    auth: DomoAuth,
    debug_api: bool = False,
    params: Optional[dict] = None,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    if not package_id or not version:
        raise CodeEngine_FunctionCallError(
            message=f"Package ID {package_id or 'not provided '} and version {version or ' not provided  '} must be provided.",
            auth=auth,
        )

    url = f"https://{auth.domo_instance}.domo.com/api/codeengine/v2/packages/{package_id}/versions/{version}"

    params = params or {"parts": "functions,code"}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        params=params,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise CodeEngine_GET_Error(codeengine_id=f"{package_id}/{version}", response_data=res)

    return res


async def test_package_is_released(
    package_id: str,
    version: str,
    auth: DomoAuth,
    existing_package: Optional[dict] = None,
    debug_api: bool = False,
    params: Optional[dict] = None,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> bool:
    """Return True if the package is already released."""
    existing_package = (
        existing_package
        or (
            await get_codeengine_package_by_id_and_version(
                package_id=package_id,
                version=version,
                auth=auth,
                debug_api=debug_api,
                params=params,
                session=session,
                parent_class=parent_class,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            )
        ).response
    )

    return existing_package.get("released")


async def test_package_is_identical(
    package_id: str,
    version: str,
    auth: DomoAuth,
    existing_package: Optional[dict] = None,
    new_package: Optional[dict] = None,
    new_code: Optional[str] = None,
    debug_api: bool = False,
    params: Optional[dict] = None,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
) -> bool:
    """Return True if the code in the new package matches the existing one."""
    existing_package = (
        existing_package
        or (
            await get_codeengine_package_by_id(
                package_id=package_id,
                version=version,
                auth=auth,
                debug_api=debug_api,
                params=params,
                session=session,
                parent_class=parent_class,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            )
        ).response
    )

    new_code = new_code or new_package.get("code")

    return existing_package.get("code") == new_package.get("code")
