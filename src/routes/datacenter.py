from __future__ import annotations

from typing import Dict, List, Optional, TypedDict, Union

import httpx

from ..client import DomoAuth as dmda
from ..client import DomoError as de
from ..client import get_data as gd
from ..client import ResponseGetData as rgd
from ..client.DomoEntity import DomoEnum

__all__ = [
    "Datacenter_Enum",
    "Dataflow_Type_Filter_Enum",
    "Datacenter_Filter_Field_Enum",
    "Datacenter_Filter_Field_Certification_Enum",
    "generate_search_datacenter_filter",
    "generate_search_datacenter_filter_search_term",
    "generate_search_datacenter_body",
    "generate_search_datacenter_account_body",
    "SearchDatacenter_NoResultsFound",
    "SearchDatacenter_GET_Error",
    "search_datacenter",
    "get_connectors",
    "LineageNode",
    "get_lineage_upstream",
    "ShareResource_Error",
    "ShareResource_Enum",
    "share_resource",
]


class Datacenter_Enum(DomoEnum):
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


class Dataflow_Type_Filter_Enum(DomoEnum):
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


class Datacenter_Filter_Field_Enum(DomoEnum):
    DATAPROVIDER = "dataprovidername_facet"
    CERTIFICATION = "certification.state"


class Datacenter_Filter_Field_Certification_Enum(DomoEnum):
    CERTIFIED = "CERTIFIED"
    PENDING = "PENDING"
    REQUESTED = "REQUESTED"
    EXPIRED = "EXPIRED"


def generate_search_datacenter_filter(
    field: Union[str, DomoEnum],  # use Datacenter_Filter_Field_Enum
    value: Union[str, DomoEnum],
    is_not: bool = False,  # to handle exclusion
):
    field = field.value if isinstance(field, DomoEnum) else field
    value = value.value if isinstance(value, DomoEnum) else value

    return {
        "filterType": "term",
        "field": field,
        "value": value,
        "not": is_not,
    }


def generate_search_datacenter_filter_search_term(search_term: str) -> dict:
    # if not "*" in search_term:
    #     search_term = f"*{search_term}*"

    return {"field": "name_sort", "filterType": "wildcard", "query": search_term}


def generate_search_datacenter_body(
    search_text: str = None,
    entity_type: Union[
        str, Datacenter_Enum, List[Datacenter_Enum]
    ] = "DATASET",  # can accept one entity_type or a list of entity_types
    additional_filters_ls: list[dict] = None,
    combineResults: bool = True,
    limit: int = 100,
    offset: int = 0,
):
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
        raise de.DomoError("entity_type must be a string or Datacenter_Enum")

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
    return {
        # "count": 100,
        # "offset": 0,
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


class SearchDatacenter_NoResultsFound(de.RouteError):
    def __init__(self, res, message=None):
        super().__init__(res=res, entity_id=res.auth.domo_instance, message=message)


class SearchDatacenter_GET_Error(de.RouteError):
    def __init__(self, res, message=None):
        super().__init__(res=res, entity_id=res.auth.domo_instance, message=message)


@gd.route_function
async def search_datacenter(
    auth: dmda.DomoAuth,
    maximum: int = None,
    body: dict = None,  # either pass a body or generate a body in the function using search_text, entity_type, and additional_filters parameters
    search_text=None,
    entity_type: Union[
        str, list
    ] = "dataset",  # can accept one value or a list of values
    additional_filters_ls=None,
    arr_fn: callable = None,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_loop: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
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

    if res.is_success and len(res.response) == 0:
        raise SearchDatacenter_NoResultsFound(
            res=res, message="no results for query parameters"
        )

    if not res.is_success:
        raise SearchDatacenter_GET_Error(res=res)

    return res


@gd.route_function
async def get_connectors(
    auth: dmda.DomoAuth,
    search_text: str = None,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    additional_filters_ls: List[dict] = None,
    return_raw: bool = False,
):
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
    )

    if return_raw:
        return res

    if search_text:
        s = [
            r
            for r in res.response
            if search_text.lower() in r.get("label", "").lower()
            or search_text.lower() in r.get("title", "").lower()
        ]

        res.response = s

    return res


class LineageNode(TypedDict):
    type: str
    id: str
    complete: bool
    children: List[LineageNode]
    parents: List[LineageNode]
    descendantCounts: Optional[Dict[str, int]]
    ancestorCounts: Optional[Dict[str, int]]


@gd.route_function
async def get_lineage_upstream(
    auth: dmda.DomoAuth,
    entity_type: str,
    entity_id: str,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
):
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

    if not res.is_success:
        raise SearchDatacenter_GET_Error(res=res)

    return res


class ShareResource_Error(de.DomoError):
    def __init__(
        self,
        message,
        domo_instance,
        parent_class: str = None,
        function_name: str = None,
    ):
        super().__init__(
            message=message,
            domo_instance=domo_instance,
            parent_class=parent_class,
            function_name=function_name,
        )


class ShareResource_Enum(DomoEnum):
    PAGE = "page"
    CARD = "badge"


@gd.route_function
async def share_resource(
    auth: dmda.DomoAuth,
    resource_ids: list,
    resource_type: ShareResource_Enum,
    group_ids: list = None,
    user_ids: list = None,
    message: str = None,  # email to user
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
):
    """shares page or card with users or groups

    body format:  {
        "resources": [
            {
                "type": "page",
                "id": {oage_id}
            }
        ],
        "recipients": [
            {
                "type": "group",
                "id": "{group_id}"
            }
        ],
        "message": "I thought you might find this page interesting."
    }"""

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

    if not res.is_success:
        raise ShareResource_Error(
            message=res.response,
            domo_instance=auth.domo_instance,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    if res.is_success:
        res.response = f"{resource_type.value} {','.join([resource['id'] for resource in  resource_ls])} successfully shared with {', '.join([recipient['id'] for recipient in recipient_ls])}"

    return res