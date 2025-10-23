"""
Enterprise Apps Route Functions

This module provides functions for managing Domo enterprise applications (custom apps)
including design retrieval, version management, and permission administration.

Functions:
    get_all_designs: Retrieve all app designs for the authenticated instance
    get_design_by_id: Retrieve a specific app design by ID
    get_design_versions: Get all versions for an app design
    get_design_source_code_by_version: Download source code for a specific version
    get_design_permissions: Get permission settings for an app design
    set_design_admins: Set admin permissions for an app design
    add_design_admin: Add an admin to an app design

Exception Classes:
    EnterpriseApp_GET_Error: Raised when app retrieval fails
    EnterpriseApp_CRUD_Error: Raised when app create/update/delete operations fail
    EnterpriseAppAssets_GET_Error: Raised when app asset retrieval fails
"""

__all__ = [
    "EnterpriseApp_GET_Error",
    "EnterpriseApp_CRUD_Error",
    "EnterpriseAppAssets_GET_Error",
    "get_all_designs",
    "get_design_by_id",
    "get_design_versions",
    "get_design_source_code_by_version",
    "get_design_permissions",
    "set_design_admins",
    "add_design_admin",
]

import os
from typing import Optional

import httpx

from ..client import get_data as gd, response as rgd
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..utils import files as dmfi


class EnterpriseApp_GET_Error(RouteError):
    """
    Raised when enterprise app retrieval operations fail.

    This exception is used for failures during GET operations on enterprise apps,
    including API errors and unexpected response formats.
    """

    def __init__(
        self,
        entity_id: Optional[str] = None,
        res: Optional[rgd.ResponseGetData] = None,
        message: Optional[str] = None,
        **kwargs,
    ):
        if not message:
            if entity_id:
                message = f"Failed to retrieve enterprise app {entity_id}"
            else:
                message = "Failed to retrieve enterprise apps"

        super().__init__(message=message, entity_id=entity_id, res=res, **kwargs)


class EnterpriseApp_CRUD_Error(RouteError):
    """
    Raised when enterprise app create, update, or delete operations fail.

    This exception is used for failures during app modification operations,
    including permission changes and admin assignments.
    """

    def __init__(
        self,
        operation: str,
        entity_id: Optional[str] = None,
        res: Optional[rgd.ResponseGetData] = None,
        message: Optional[str] = None,
        **kwargs,
    ):
        if not message:
            if entity_id:
                message = f"Enterprise app {operation} failed for app {entity_id}"
            else:
                message = f"Enterprise app {operation} operation failed"

        super().__init__(
            message=message,
            entity_id=entity_id,
            res=res,
            additional_context={"operation": operation},
            **kwargs,
        )


class EnterpriseAppAssets_GET_Error(RouteError):
    """
    Raised when enterprise app asset retrieval operations fail.

    This exception is used for failures when downloading app source code,
    archives, or other asset files.
    """

    def __init__(
        self,
        entity_id: Optional[str] = None,
        res: Optional[rgd.ResponseGetData] = None,
        message: Optional[str] = None,
        **kwargs,
    ):
        if not message:
            if entity_id:
                message = f"Unable to download assets for enterprise app {entity_id}"
            else:
                message = "Enterprise app asset download failed"

        super().__init__(message=message, entity_id=entity_id, res=res, **kwargs)


@gd.route_function
async def get_all_designs(
    auth: DomoAuth,
    parts: str = "owners,creator,thumbnail,versions,cards",
    debug_loop: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Retrieve all enterprise app designs for the authenticated instance.

    Fetches a list of all app designs with pagination support. Returns design metadata
    including owners, creator, thumbnails, versions, and associated cards.

    Args:
        auth: Authentication object containing instance and credentials
        parts: Comma-separated list of design parts to include (default: "owners,creator,thumbnail,versions,cards")
        debug_loop: Enable detailed pagination loop logging
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing list of enterprise app designs

    Raises:
        EnterpriseApp_GET_Error: If app design retrieval fails or API returns an error

    Example:
        >>> designs_response = await get_all_designs(auth)
        >>> for design in designs_response.response:
        ...     print(f"Design: {design['id']}, Name: {design.get('name')}")
    """
    url = f"https://{auth.domo_instance}.domo.com/api/apps/v1/designs"

    params = {
        "checkAdminAuthority": True,
        "deleted": False,
        "direction": "desc",
        "parts": parts,
        "search": "",
        "withPermission": "ADMIN",
    }

    offset_params = {
        "limit": "limit",
        "offset": "offset",
    }

    res = await gd.looper(
        url=url,
        method="get",
        fixed_params=params,
        offset_params=offset_params,
        offset_params_in_body=False,
        auth=auth,
        debug_api=debug_api,
        debug_loop=debug_loop,
        timeout=10,
        limit=30,
        return_raw=return_raw,
        arr_fn=lambda x: x.response,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise EnterpriseApp_GET_Error(
            res=res, message="Failed to retrieve enterprise app designs"
        )

    return res


@gd.route_function
async def get_design_by_id(
    auth: DomoAuth,
    design_id: str,
    parts: str = "owners,cards,versions,creator",
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Retrieve a specific enterprise app design by its ID.

    Fetches details for a single app design identified by its unique ID.
    Returns design metadata including specified parts like owners, cards, versions, and creator.

    Args:
        auth: Authentication object containing instance and credentials
        design_id: Unique identifier for the app design to retrieve
        parts: Comma-separated list of design parts to include (default: "owners,cards,versions,creator")
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing the specific app design data

    Raises:
        EnterpriseApp_GET_Error: If app design retrieval fails

    Example:
        >>> design_response = await get_design_by_id(auth, "8c16c8ab-c068-4110-940b-f738d7146efc")
        >>> design_data = design_response.response
        >>> print(f"Design Name: {design_data.get('name')}")
    """
    url = f"https://{auth.domo_instance}.domo.com/api/apps/v1/designs/{design_id}"

    res = await gd.get_data(
        url=url,
        method="get",
        params={"parts": parts},
        auth=auth,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise EnterpriseApp_GET_Error(entity_id=design_id, res=res)

    return res


@gd.route_function
async def get_design_versions(
    auth: DomoAuth,
    design_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Get all versions for an enterprise app design.

    Retrieves the version history for a specific app design, including
    version numbers, creation dates, and other version metadata.

    Args:
        auth: Authentication object containing instance and credentials
        design_id: Unique identifier for the app design
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing list of design versions

    Raises:
        EnterpriseApp_GET_Error: If version retrieval fails

    Example:
        >>> versions_response = await get_design_versions(auth, design_id="8c16c8ab-c068-4110-940b-f738d7146efc")
        >>> for version in versions_response.response:
        ...     print(f"Version: {version['version']}, Created: {version.get('createdAt')}")
    """
    url = f"https://{auth.domo_instance}.domo.com/domoapps/designs/{design_id}/versions"

    res = await gd.get_data(
        url=url,
        auth=auth,
        method="get",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise EnterpriseApp_GET_Error(
            entity_id=design_id,
            res=res,
            message=f"Failed to retrieve versions for design {design_id}",
        )

    return res


@gd.route_function
async def get_design_source_code_by_version(
    auth: DomoAuth,
    design_id: str,
    version: str,
    download_path: Optional[str] = None,
    is_unpack_archive: bool = True,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Download source code for a specific app design version.

    Retrieves the source code assets as a ZIP archive for a particular version
    of an app design. Optionally downloads and unpacks the archive to a local path.

    Args:
        auth: Authentication object containing instance and credentials
        design_id: Unique identifier for the app design
        version: Version number or identifier to download
        download_path: Optional local path to save the downloaded archive
        is_unpack_archive: Whether to unpack the downloaded ZIP archive (default: True)
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing the ZIP archive bytes

    Raises:
        EnterpriseAppAssets_GET_Error: If asset download fails or version not found

    Example:
        >>> asset_response = await get_design_source_code_by_version(
        ...     auth,
        ...     design_id="8c16c8ab-c068-4110-940b-f738d7146efc",
        ...     version="1",
        ...     download_path="/tmp/app_source"
        ... )
        >>> print(f"Downloaded {len(asset_response.response)} bytes")
    """
    url = f"http://{auth.domo_instance}.domo.com/domoapps/designs/{design_id}/versions/{version}/assets"

    res = await gd.get_data_stream(
        url=url,
        method="get",
        auth=auth,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        if res.response == "Not Found":
            raise EnterpriseAppAssets_GET_Error(
                entity_id=design_id,
                res=res,
                message=f"Assets not found for design {design_id} version {version}",
            )
        raise EnterpriseAppAssets_GET_Error(entity_id=design_id, res=res)

    if download_path:
        archive_path = os.path.join(download_path, "archive.zip")

        dmfi.download_zip(
            output_folder=archive_path,
            zip_bytes_content=res.response,
            is_unpack_archive=False,
        )

        if is_unpack_archive:
            dmfi.download_zip(
                output_folder=download_path,
                zip_bytes_content=res.response,
                is_unpack_archive=True,
            )

    return res


@gd.route_function
async def get_design_permissions(
    design_id: str,
    auth: DomoAuth,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
):
    res = await get_design_by_id(
        auth=auth,
        design_id=design_id,
        parts="owners",
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        session=session,
        parent_class=parent_class,
    )

    res.response = res.response["owners"]
    return res


async def set_design_admins(
    design_id,
    auth: DomoAuth,
    user_ids: List[str],
    debug_api: bool = False,
    return_raw: bool = False,
):
    url = f"https://{auth.domo_instance}.domo.com/api/apps/v1/designs/{design_id}/permissions/ADMIN"

    res = await gd.get_data(
        url=url,
        method="POST",
        auth=auth,
        debug_api=debug_api,
        body=user_ids,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise App_API_Exception(res=res)

    res.response = f"successfully set design_id {design_id} admins to {user_ids}"

    return res


async def add_design_admin(
    design_id: str, auth: DomoAuth, user_ids: List[int], debug_api: bool = False
):
    user_ids = user_ids if isinstance(user_ids, list) else [user_ids]

    res = await get_design_permissions(
        design_id=design_id, auth=auth, debug_api=debug_api
    )

    user_ids = list(set([owner["id"] for owner in res.response] + user_ids))

    return await set_design_admins(
        design_id=design_id, auth=auth, debug_api=debug_api, user_ids=user_ids
    )
