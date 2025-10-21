__all__ = [
    "CodeEngine_API_Error",
    "get_packages",
    "CodeEngine_Package_Parts",
    "CodeEngine_FunctionCallError",
    "get_codeengine_package_by_id",
    "get_package_versions",
    "get_codeengine_package_by_id_and_version",
    "test_package_is_released",
    "test_package_is_identical",
]

from enum import Enum
import httpx

from ..client import auth as dmda
from ..client import exceptions as dmde
from ..client import get_data as gd
from ..client import response as rgd
from ..client.entities import DomoEnumMixin


class CodeEngine_API_Error(dmde.RouteError):
    def __init__(self, res: rgd.ResponseGetData):
        super().__init__(res=res)


@gd.route_function
async def get_packages(
    auth: DomoAuth,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
):
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
        raise CodeEngine_API_Error(res=res)

    return res


class CodeEngine_Package_Parts(DomoEnumMixin, Enum):
    VERSIONS = "versions"
    FUNCTIONS = "functions"
    CODE = "code"


class CodeEngine_FunctionCallError(DomoError):
    def __init__(self, message: str, auth: DomoAuth):
        super().__init__(message=message, domo_instance=auth.domo_instance)


@gd.route_function
async def get_codeengine_package_by_id(
    package_id,
    auth: DomoAuth,
    debug_api: bool = False,
    params: dict = None,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
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
        raise CodeEngine_API_Error(res=res)

    return res


@gd.route_function
async def get_package_versions(
    auth: DomoAuth,
    package_id,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
):
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
        raise CodeEngine_API_Error(res=res)

    return res


@gd.route_function
async def get_codeengine_package_by_id_and_version(
    package_id,
    version,
    auth: DomoAuth,
    debug_api: bool = False,
    params: dict = None,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
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
        raise CodeEngine_API_Error(res=res)

    return res


async def test_package_is_released(
    package_id,
    version,
    auth: DomoAuth,
    existing_package=None,
    debug_api: bool = False,
    params: dict = None,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
):
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
    package_id,
    version,
    auth: DomoAuth,
    existing_package=None,
    new_package=None,
    new_code=None,
    debug_api: bool = False,
    params: dict = None,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
):
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
