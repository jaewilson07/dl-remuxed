"""
Datacenter Route Core Functions

This module provides core datacenter functions for searching, retrieving lineage,
and sharing resources in Domo.

Enums:
    Datacenter_Enum: Types of datacenter entities
    Dataflow_Type_Filter_Enum: Dataflow type filters
    Datacenter_Filter_Field_Enum: Fields for filtering datacenter searches
    Datacenter_Filter_Field_Certification_Enum: Certification states
    ShareResource_Enum: Resource types that can be shared

Utility Functions:
    generate_search_datacenter_filter: Generate filter for datacenter search
    generate_search_datacenter_filter_search_term: Generate search term filter
    generate_search_datacenter_body: Generate complete search body
    generate_search_datacenter_account_body: Generate account search body

Route Functions:
    search_datacenter: Search across datacenter entities
    get_connectors: Retrieve available connectors
    get_lineage_upstream: Get upstream lineage for an entity
    share_resource: Share a resource with users or groups
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, TypedDict, Union

import httpx

from ...client import (
    get_data as gd,
    response as rgd,
)
from ...client.auth import DomoAuth
from ...entities.base import DomoEnumMixin

from .exceptions import (
    Datacenter_GET_Error,
    SearchDatacenter_NoResultsFound,
    ShareResource_Error,
)


class Datacenter_Enum(DomoEnumMixin, Enum):
    ACCOUNT = "ACCOUNT"
    CARD = "CARD"
    DATAFLOW = "DATAFLOW"
    DATASET = "DATASET"
    GROUP = "GROUP"
    PAGE = "PAGE"
    USER = "USER"
    CONNECTOR = "CONNECTOR"
    PACKAGE = "PACKAGE"
    DATA_APP = "DATA_APP"
    default = "UNKNOWN"


class Dataflow_Type_Filter_Enum(DomoEnumMixin, Enum):
    ADR = {
        "filterType": "term",
        "field": "data_flow_type",
        "value": "ADR",
        "name": "ADR",
        "not": False,
    }

    MYSQL = {
        "filterType": "term",
        "field": "data_flow_type",
        "value": "MYSQL",
        "name": "MYSQL",
        "not": False,
    }

    REDSHIFT = {
        "filterType": "term",
        "field": "data_flow_type",
        "value": "MYSQL",
        "name": "MYSQL",
        "not": False,
    }

    MAGICV2 = {
        "filterType": "term",
        "field": "data_flow_type",
        "value": "MAGIC",
        "name": "Magic ETL v2",
        "not": False,
    }

    MAGIC = {
        "filterType": "term",
        "field": "data_flow_type",
        "value": "ETL",
        "name": "Magic ETL",
        "not": False,
    }


class Datacenter_Filter_Field_Enum(DomoEnumMixin, Enum):
    DATAPROVIDER = "dataprovidername_facet"
    CERTIFICATION = "certification.state"


class Datacenter_Filter_Field_Certification_Enum(DomoEnumMixin, Enum):
    CERTIFIED = "CERTIFIED"
    PENDING = "PENDING"
    REQUESTED = "REQUESTED"
    EXPIRED = "EXPIRED"


class ShareResource_Enum(DomoEnumMixin, Enum):
    PAGE = "page"
    CARD = "badge"


class LineageNode(TypedDict):
    type: str
    id: str
    complete: bool
    children: List[LineageNode]
    parents: List[LineageNode]
    descendantCounts: Optional[Dict[str, int]]
    ancestorCounts: Optional[Dict[str, int]]


def generate_search_datacenter_filter(
    field: Union[str, Enum],  # use Datacenter_Filter_Field_Enum
    value: Union[str, Enum],
    is_not: bool = False,  # to handle exclusion
):
    """Generate a filter object for datacenter search.

    Args:
        field: Field to filter on (string or enum)
        value: Value to filter for (string or enum)
        is_not: Whether to negate the filter

    Returns:
        Dictionary containing filter specification
    """
    field = field.value if isinstance(field, Enum) else field
    value = value.value if isinstance(value, Enum) else value

    return {
        "filterType": "term",
        "field": field,
        "value": value,
        "not": is_not,
    }


def generate_search_datacenter_filter_search_term(search_term: str) -> dict:
    """Generate a search term filter for datacenter search.

    Args:
        search_term: Text to search for

    Returns:
        Dictionary containing search term filter
    """
    return {"field": "name_sort", "filterType": "wildcard", "query": search_term}


def generate_search_datacenter_body(
    search_text: Optional[str] = None,
    entity_type: Union[
        str, Datacenter_Enum, List[Datacenter_Enum]
    ] = "DATASET",  # can accept one entity_type or a list of entity_types
    additional_filters_ls: Optional[list[dict]] = None,
    combineResults: bool = True,
    limit: int = 100,
    offset: int = 0,
):
    """Generate complete body for datacenter search request.

    Args:
        search_text: Optional search text to filter results
        entity_type: Type(s) of entities to search for
        additional_filters_ls: Additional filters to apply
        combineResults: Whether to combine results
        limit: Maximum number of results
        offset: Offset for pagination

    Returns:
        Dictionary containing complete search body

    Raises:
        ValueError: If entity_type is not a string or Datacenter_Enum
    """
    filters_ls = (
        [generate_search_datacenter_filter_search_term(search_text)]
        if search_text
        else []
    )

    if not isinstance(entity_type, list):
        entity_type = [entity_type]

    entity_type = [
        en.value if isinstance(en, Datacenter_Enum) else en for en in entity_type
    ]

    if not all(isinstance(en, str) for en in entity_type):
        raise ValueError("entity_type must be a string or Datacenter_Enum")

    if additional_filters_ls:
        if not isinstance(additional_filters_ls, list):
            additional_filters_ls = [additional_filters_ls]

        filters_ls += additional_filters_ls

    return {
        "entities": entity_type,
        "filters": filters_ls or [],
        "combineResults": combineResults,
        "query": "*",
        "count": limit,
        "offset": offset,
    }


def generate_search_datacenter_account_body(
    search_str: str, is_exact_match: bool = True
):
    """Generate body for datacenter account search.

    Args:
        search_str: String to search for
        is_exact_match: Whether to require exact match

    Returns:
        Dictionary containing account search body
    """
    return {
        "combineResults": False,
        "query": search_str if is_exact_match else f"*{search_str}*",
        "filters": [],
        "facetValuesToInclude": [
            "DATAPROVIDERNAME",
            "OWNED_BY_ID",
            "VALID",
            "USED",
            "LAST_MODIFIED_DATE",
        ],
        "queryProfile": "GLOBAL",
        "entityList": [["account"]],
        "sort": {"fieldSorts": [{"field": "display_name_sort", "sortOrder": "ASC"}]},
    }


@gd.route_function
async def search_datacenter(
    auth: DomoAuth,
    maximum: Optional[int] = None,
    body: Optional[
        dict
    ] = None,  # either pass a body or generate a body in the function using search_text, entity_type, and additional_filters parameters
    search_text: Optional[str] = None,
    entity_type: Union[
        str, list
    ] = "dataset",  # can accept one value or a list of values
    additional_filters_ls: Optional[list] = None,
    arr_fn: Optional[callable] = None,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_loop: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Search across datacenter entities.

    Args:
        auth: Authentication object
        maximum: Maximum number of results to return
        body: Pre-built search body (optional)
        search_text: Text to search for
        entity_type: Type(s) of entities to search
        additional_filters_ls: Additional filters to apply
        arr_fn: Function to extract array from response
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_loop: Enable loop debugging
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing search results

    Raises:
        SearchDatacenter_NoResultsFound: If search returns no results
        Datacenter_GET_Error: If search operation fails
    """
    limit = 100  # api enforced limit

    if not body:
        body = generate_search_datacenter_body(
            entity_type=entity_type,
            additional_filters_ls=additional_filters_ls,
            search_text=search_text,
            combineResults=False,
            limit=limit,
        )

    if not arr_fn:

        def arr_fn(res):
            return res.response.get("searchObjects")

    url = f"https://{auth.domo_instance}.domo.com/api/search/v1/query"

    res = await gd.looper(
        auth=auth,
        session=session,
        url=url,
        loop_until_end=True if not maximum else False,
        body=body,
        offset_params_in_body=True,
        offset_params={"offset": "offset", "limit": "count"},
        arr_fn=arr_fn,
        method="POST",
        maximum=maximum,
        limit=limit,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        debug_loop=debug_loop,
    )

    if return_raw:
        return res

    if res.is_success and len(res.response) == 0:
        raise SearchDatacenter_NoResultsFound(
            res=res, message="no results for query parameters"
        )

    if not res.is_success:
        raise Datacenter_GET_Error(res=res)

    return res


@gd.route_function
async def get_connectors(
    auth: DomoAuth,
    search_text: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    additional_filters_ls: Optional[List[dict]] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve available connectors from datacenter.

    Args:
        auth: Authentication object
        search_text: Optional text to filter connectors
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        additional_filters_ls: Additional filters to apply
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing connector list

    Raises:
        SearchDatacenter_NoResultsFound: If no connectors found
        Datacenter_GET_Error: If connector retrieval fails
    """
    additional_filters_ls = additional_filters_ls or []

    body = generate_search_datacenter_body(
        entity_type=Datacenter_Enum.CONNECTOR,
        additional_filters_ls=additional_filters_ls,
        combineResults=True,
    )

    res = await search_datacenter(
        auth=auth,
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        return_raw=True,  # Get raw response first to avoid raising errors
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Datacenter_GET_Error(res=res)

    if search_text:
        s = [
            r
            for r in res.response
            if search_text.lower() in r.get("label", "").lower()
            or search_text.lower() in r.get("title", "").lower()
        ]

        res.response = s

    return res


@gd.route_function
async def get_lineage_upstream(
    auth: DomoAuth,
    entity_type: str,
    entity_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Get upstream lineage for a datacenter entity.

    Args:
        auth: Authentication object
        entity_type: Type of entity (e.g., 'dataset', 'dataflow')
        entity_id: ID of the entity
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object containing lineage data

    Raises:
        Datacenter_GET_Error: If lineage retrieval fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/lineage/{entity_type}/{entity_id}"

    params = {"traverseDown": "false"}

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        params=params,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Datacenter_GET_Error(res=res)

    return res


@gd.route_function
async def share_resource(
    auth: DomoAuth,
    resource_ids: Union[list, str, int],
    resource_type: ShareResource_Enum,
    group_ids: Optional[Union[list, str, int]] = None,
    user_ids: Optional[Union[list, str, int]] = None,
    message: Optional[str] = None,  # email to user
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Share a page or card with users or groups.

    Args:
        auth: Authentication object
        resource_ids: ID(s) of resources to share
        resource_type: Type of resource (PAGE or CARD)
        group_ids: ID(s) of groups to share with
        user_ids: ID(s) of users to share with
        message: Optional message to include in notification email
        debug_api: Enable API debugging
        session: HTTP client session (optional)
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object with success message

    Raises:
        ShareResource_Error: If sharing operation fails

    Example body format:
        {
            "resources": [
                {
                    "type": "page",
                    "id": {page_id}
                }
            ],
            "recipients": [
                {
                    "type": "group",
                    "id": "{group_id}"
                }
            ],
            "message": "I thought you might find this page interesting."
        }
    """
    resource_ids = resource_ids if isinstance(resource_ids, list) else [resource_ids]
    if group_ids:
        group_ids = (
            group_ids and group_ids if isinstance(group_ids, list) else [group_ids]
        )

    if user_ids:
        user_ids = user_ids if isinstance(user_ids, list) else [user_ids]

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/share?sendEmail=false"

    recipient_ls = []

    if group_ids:
        for gid in group_ids:
            recipient_ls.append({"type": "group", "id": str(gid)})

    if user_ids:
        for uid in user_ids:
            recipient_ls.append({"type": "user", "id": str(uid)})

    resource_ls = [
        {"type": resource_type.value, "id": str(rid)} for rid in resource_ids
    ]

    body = {
        "resources": resource_ls,
        "recipients": recipient_ls,
        "message": message,
    }

    res = await gd.get_data(
        url,
        method="POST",
        auth=auth,
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise ShareResource_Error(
            message=res.response,
            domo_instance=auth.domo_instance,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
            res=res,
        )

    if res.is_success:
        res.response = f"{resource_type.value} {','.join([resource['id'] for resource in resource_ls])} successfully shared with {', '.join([recipient['id'] for recipient in recipient_ls])}"

    return res
