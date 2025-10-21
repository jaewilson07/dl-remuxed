__all__ = [
    "CodeEnginePackageBuilder",
    "deploy_code_engine_package",
    "CodeEngine_InvalidPackage",
    "create_code_engine_package",
    "increment_version",
    "upsert_code_engine_package_version",
    "upsert_package",
]


# from ..utils.CodeEngineUtils import (
#     CodeEngineScriptAnalyzer,
#     CodeEnginePackageBuilder
# )

import httpx

from ..client import auth as dmda
from ..client import exceptions as dmde
from ..client import get_data as gd
from ..client import response as rgd
from . import codeengine as codeengine_routes
from .codeengine import CodeEngine_API_Error


class CodeEnginePackageBuilder:
    def __init__(self):
        pass


@gd.route_function
async def deploy_code_engine_package(
    package_id,
    version,
    auth: DomoAuth,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/codeengine/v2/packages/{package_id}/versions/{version}/release"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise CodeEngine_API_Error(res=res)

    return res


class CodeEngine_InvalidPackage(DomoError):
    def __init__(self, message: str, auth: DomoAuth):
        super().__init__(message=message, domo_instance=auth.domo_instance)


@gd.route_function
async def create_code_engine_package(
    payload: dict,
    auth: DomoAuth,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/codeengine/v2/packages"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        body=payload,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise CodeEngine_API_Error(res=res)

    return res


# class CodeEngine_PackageNotFound(dmde.RouteError):
#     def __init__(self, res, message: str, auth: DomoAuth):
#         super().__init__(res = res, message=message, domo_instance=auth.domo_instance)


# class CodeEngine_PackageAlreadyDeployed(DomoError):
#     def __init__(self, message: str, auth: DomoAuth):
#         super().__init__(message=message, domo_instance=auth.domo_instance)
def increment_version(version: str) -> str:
    parts = version.split(".")
    # Increment the last part
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


@gd.route_function
async def upsert_code_engine_package_version(
    auth: DomoAuth,
    payload: dict,
    version: str = None,
    auto_increment_version: bool = True,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
    debug_api: bool = False,
    debug_prn: bool = False,
) -> rgd.ResponseGetData:
    package_id = payload.get("id")
    version = version or payload.get("version")

    try:
        existing_pkg = await codeengine_routes.get_codeengine_package_by_id_and_version(
            package_id,
            version,
            auth=auth,
            params={"parts": "code"},
            debug_api=debug_api,
            session=session,
            parent_class=parent_class,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )
        if await codeengine_routes.test_package_is_released(
            existing_pkg=existing_pkg, package_id=package_id, version=version, auth=auth
        ):
            if not auto_increment_version:
                raise CodeEngine_InvalidPackage(
                    message=f"Package {package_id} v{version} already deployed",
                    auth=auth,
                )

            version = increment_version(version)

        if await codeengine_routes.test_package_is_identical(
            existing_pkg=existing_pkg, package_id=package_id, version=version, auth=auth
        ):
            if debug_prn:
                print(f"Package {package_id} v{version} is identical; skipping update.")
            return existing_pkg

    except CodeEngine_API_Error:
        pass  # Not found, continue to create

    return await create_code_engine_package(
        payload=payload,
        auth=auth,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )


@gd.route_function
async def upsert_package(
    payload: dict,
    auth: DomoAuth,
    check_different: bool = True,
    create_new_version: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    debug_prn: bool = False,
) -> rgd.ResponseGetData:
    package_id = payload.get("id")

    if not package_id:
        if debug_prn:
            print("No Package ID found, creating new package...")

        return await create_code_engine_package(
            payload=payload,
            auth=auth,
            debug_api=debug_api,
            session=session,
            parent_class=parent_class,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

    try:
        await codeengine_routes.get_codeengine_package_by_id(
            package_id,
            auth=auth,
            debug_api=debug_api,
            session=session,
            parent_class=parent_class,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )
    except CodeEngine_API_Error:
        return await create_code_engine_package(
            payload,
            auth=auth,
            debug_api=debug_api,
            session=session,
            parent_class=parent_class,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

    return await upsert_code_engine_package_version(
        payload=payload,
        auth=auth,
        increment_version=True,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )
