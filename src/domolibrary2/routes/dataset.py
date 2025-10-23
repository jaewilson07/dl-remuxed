__all__ = [
    "DatasetNotFoundError",
    "Dataset_GetError",
    "Dataset_CRUDError",
    "QueryRequestError",
    "query_dataset_public",
    "query_dataset_private",
    "get_dataset_by_id",
    "get_schema",
    "alter_schema",
    "alter_schema_descriptions",
    "set_dataset_tags",
    "UploadDataError",
    "upload_dataset_stage_1",
    "upload_dataset_stage_2_file",
    "upload_dataset_stage_2_df",
    "upload_dataset_stage_3",
    "index_dataset",
    "index_status",
    "generate_list_partitions_body",
    "list_partitions",
    "generate_create_dataset_body",
    "create",
    "generate_enterprise_toolkit_body",
    "generate_remote_domostats_body",
    "create_dataset_enterprise_tookit",
    "delete_partition_stage_1",
    "delete_partition_stage_2",
    "delete",
    "ShareDataset_AccessLevelEnum",
    "generate_share_dataset_payload",
    "ShareDataset_Error",
    "share_dataset",
    "get_permissions",
]

import io
from enum import Enum
from typing import List, Optional

import httpx
import pandas as pd


from ..entities.base import DomoEnumMixin
from ..client import auth as dmda, exceptions as de, get_data as gd, response as rgd
from ..client.auth import DomoAuth


class DatasetNotFoundError(de.RouteError):
    def __init__(self, dataset_id, res: rgd.ResponseGetData, message: str = None):
        message = message or f"dataset - {dataset_id} not found"

        super().__init__(message=message, res=res, entity_id=dataset_id)


class Dataset_GetError(de.DomoError):
    def __init__(
        self,
        dataset_id,
        res: rgd.ResponseGetData,
        message=None,
    ):
        super().__init__(message=message, res=res, entity_id=dataset_id)


class Dataset_CRUDError(de.DomoError):
    def __init__(
        self,
        res: rgd.ResponseGetData,
        dataset_id=None,
        message=None,
    ):
        super().__init__(message=message, res=res, entity_id=dataset_id)


class QueryRequestError(de.RouteError):
    def __init__(
        self,
        res: rgd.ResponseGetData,
        sql,
        dataset_id,
        message=None,
    ):
        message = message or f"{res.response} - Check your SQL \n {sql}"

        super().__init__(message=message, res=res, entity_id=dataset_id)


# typically do not use
@gd.route_function
async def query_dataset_public(
    dev_auth: dmda.DomoDeveloperAuth,
    dataset_id: str,
    sql: str,
    session: httpx.AsyncClient,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
):
    """query for hitting public apis, requires client_id and secret authentication"""

    url = f"https://api.domo.com/v1/datasets/query/execute/{dataset_id}?IncludeHeaders=true"

    body = {"sql": sql}

    res = await gd.get_data(
        auth=dev_auth,
        url=url,
        method="POST",
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


gd.route_function


async def query_dataset_private(
    auth: DomoAuth,
    dataset_id: str,
    sql: str,
    loop_until_end: bool = False,  # retrieve all available rows
    limit=100,  # maximum rows to return per request.  refers to PAGINATION
    skip=0,
    maximum=100,  # equivalent to the LIMIT or TOP clause in SQL, the number of rows to return total
    filter_pdp_policy_id_ls: List[int] = None,
    timeout: int = 10,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    parent_class=None,
    debug_loop: bool = False,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/execute/{dataset_id}"

    offset_params = {
        "offset": "offset",
        "limit": "limit",
    }

    # def body_fn(skip, limit):
    #     return {"sql": f"{sql} limit {limit} offset {skip}"}

    def body_fn(skip, limit, body=None):
        body = {"sql": f"{sql} limit {limit} offset {skip}"}

        if filter_pdp_policy_id_ls:
            body.update(
                {
                    "context": {
                        "dataControlContext": {
                            "filterGroupIds": filter_pdp_policy_id_ls,
                            "previewPdp": True,
                        }
                    }
                }
            )

        return body

    def arr_fn(res) -> pd.DataFrame:
        rows_ls = res.response.get("rows")
        columns_ls = res.response.get("columns")
        output = []
        for row in rows_ls:
            new_row = {}
            for index, column in enumerate(columns_ls):
                new_row[column] = row[index]
            output.append(new_row)
            # pd.DataFrame(data=res.response.get('rows'), columns=res.response.get('columns'))
        return output

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        arr_fn=arr_fn,
        offset_params=offset_params,
        limit=limit,
        skip=skip,
        maximum=maximum,
        body_fn=body_fn,
        loop_until_end=loop_until_end,
        timeout=timeout,
        session=session,
        debug_loop=debug_loop,
        parent_class=parent_class,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if res.status == 404 and res.response == "Not Found":
        raise DatasetNotFoundError(
            dataset_id=dataset_id,
            res=res,
        )

    if res.status == 400 and res.response == "Bad Request":
        raise QueryRequestError(dataset_id=dataset_id, sql=sql, res=res)

    if not res.is_success:
        raise QueryRequestError(dataset_id=dataset_id, sql=sql, res=res)

    return res


@gd.route_function
async def get_dataset_by_id(
    dataset_id: str,  # dataset id from URL
    auth: Optional[DomoAuth] = None,  # requires full authentication
    debug_api: bool = False,  # for troubleshooting API request
    session: Optional[httpx.AsyncClient] = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:  # returns metadata about a dataset
    """retrieve dataset metadata"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if res.status == 404 and res.response == "Not Found":
        raise DatasetNotFoundError(dataset_id=dataset_id, res=res)

    if not res.is_success:
        raise Dataset_GetError(dataset_id=dataset_id, res=res)

    return res


@gd.route_function
async def get_schema(
    auth: DomoAuth,
    dataset_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
) -> rgd.ResponseGetData:
    """retrieve the schema for a dataset"""

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/schema/indexed?includeHidden=false"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )

    if not res.is_success:
        raise Dataset_GetError(dataset_id=dataset_id, res=res)

    return res


@gd.route_function
async def alter_schema(
    auth: DomoAuth,
    schema_obj: dict,
    dataset_id: str,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
    session=httpx.AsyncClient(),
) -> rgd.ResponseGetData:
    """alters the schema for a dataset BUT DOES NOT ALTER THE DESCRIPTION"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v2/datasources/{dataset_id}/schemas"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=schema_obj,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


@gd.route_function
async def alter_schema_descriptions(
    auth: DomoAuth,
    schema_obj: dict,
    dataset_id: str,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
    session=httpx.AsyncClient(),
) -> rgd.ResponseGetData:
    """alters the description of the schema columns // as seen in DataCenter > Dataset > Schema"""

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/wrangle"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=schema_obj,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


@gd.route_function
async def set_dataset_tags(
    auth: DomoAuth,
    tag_ls: List[str],  # complete list of tags for dataset
    dataset_id: str,
    return_raw: bool = False,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
):
    """REPLACE tags on this dataset with a new list"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/ui/v3/datasources/{dataset_id}/tags"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        debug_api=debug_api,
        body=tag_ls,
        session=session,
        return_raw=return_raw,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if res.status == 200:
        res.set_response(
            response=f"Dataset {dataset_id} tags updated to [{', '.join(tag_ls)}]"
        )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


class UploadDataError(de.RouteError):
    """raise if unable to upload data to Domo"""

    def __init__(
        self,
        stage_num: int,
        dataset_id: str,
        res: rgd.ResponseGetData,
        message: str = None,
    ):
        message = f"error uploading data during Stage {stage_num} - {message}"

        super().__init__(entity_id=dataset_id, message=message, res=res)


@gd.route_function
async def upload_dataset_stage_1(
    auth: DomoAuth,
    dataset_id: str,
    #  restate_data_tag: str = None, # deprecated
    partition_tag: str = None,  # synonymous with data_tag
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    return_raw: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
) -> rgd.ResponseGetData:
    """preps dataset for upload by creating an upload_id (upload session key) pass to stage 2 as a parameter"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads"

    # base body assumes no paritioning
    body = {"action": None, "appendId": None}

    params = None

    if partition_tag:
        # params = {'dataTag': restate_data_tag or data_tag} # deprecated
        params = {"dataTag": partition_tag}
        body.update({"appendId": "latest"})

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        session=session,
        debug_api=debug_api,
        params=params,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise UploadDataError(stage_num=1, dataset_id=dataset_id, res=res)

    if return_raw:
        return res

    upload_id = res.response.get("uploadId")

    if not upload_id:
        raise UploadDataError(
            stage_num=1,
            dataset_id=dataset_id,
            res=res,
            message="no upload_id",
        )

    res.response = upload_id

    return res


@gd.route_function
async def upload_dataset_stage_2_file(
    auth: DomoAuth,
    dataset_id: str,
    upload_id: str,  # must originate from  a stage_1 upload response
    data_file: Optional[io.TextIOWrapper] = None,
    session: Optional[httpx.AsyncClient] = None,
    # only necessary if streaming multiple files into the same partition (multi-part upload)
    part_id: str = 2,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads/{upload_id}/parts/{part_id}"

    body = data_file

    res = await gd.get_data(
        url=url,
        method="PUT",
        auth=auth,
        content_type="text/csv",
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise UploadDataError(stage_num=2, dataset_id=dataset_id, res=res)

    res.upload_id = upload_id
    res.dataset_id = dataset_id
    res.part_id = part_id

    return res


@gd.route_function
async def upload_dataset_stage_2_df(
    auth: DomoAuth,
    dataset_id: str,
    upload_id: str,  # must originate from  a stage_1 upload response
    upload_df: pd.DataFrame,
    session: Optional[httpx.AsyncClient] = None,
    part_id: str = 2,  # only necessary if streaming multiple files into the same partition (multi-part upload)
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads/{upload_id}/parts/{part_id}"

    body = upload_df.to_csv(header=False, index=False)

    # if debug:
    #     print(body)

    res = await gd.get_data(
        url=url,
        method="PUT",
        auth=auth,
        content_type="text/csv",
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise UploadDataError(stage_num=2, dataset_id=dataset_id, res=res)

    res.upload_id = upload_id
    res.dataset_id = dataset_id
    res.part_id = part_id

    return res


@gd.route_function
async def upload_dataset_stage_3(
    auth: DomoAuth,
    dataset_id: str,
    upload_id: str,  # must originate from  a stage_1 upload response
    update_method: str = "REPLACE",  # accepts REPLACE or APPEND
    partition_tag: str = None,  # synonymous with data_tag
    is_index: bool = False,  # index after uploading
    #  restate_data_tag: str = None, # deprecated
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
) -> rgd.ResponseGetData:
    """commit will close the upload session, upload_id.  this request defines how the data will be loaded into Adrenaline, update_method
    has optional flag for indexing dataset.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads/{upload_id}/commit"

    body = {"index": is_index, "action": update_method}

    if partition_tag:
        body.update(
            {
                "action": "APPEND",
                #  'dataTag': restate_data_tag or data_tag,
                #  'appendId': 'latest' if (restate_data_tag or data_tag) else None,
                "dataTag": partition_tag,
                "appendId": "latest" if partition_tag else None,
                "index": is_index,
            }
        )

    res = await gd.get_data(
        auth=auth,
        method="PUT",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise UploadDataError(stage_num=3, dataset_id=dataset_id, res=res)

    res.upload_id = upload_id
    res.dataset_id = dataset_id

    return res


@gd.route_function
async def index_dataset(
    auth: DomoAuth,
    dataset_id: str,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
) -> rgd.ResponseGetData:
    """manually index a dataset"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/indexes"

    body = {"dataIds": []}

    res = await gd.get_data(
        auth=auth,
        method="POST",
        body=body,
        url=url,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


@gd.route_function
async def index_status(
    auth: DomoAuth,
    dataset_id: str,
    index_id: str,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
) -> rgd.ResponseGetData:
    """get the completion status of an index"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/indexes/{index_id}/statuses"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Dataset_GetError(dataset_id=dataset_id, res=res)

    return res


def generate_list_partitions_body(limit=100, offset=0):
    return {
        "paginationFields": [
            {
                "fieldName": "datecompleted",
                "sortOrder": "DESC",
                "filterValues": {"MIN": None, "MAX": None},
            }
        ],
        "limit": limit,
        "offset": offset,
    }


gd.route_function


async def list_partitions(
    auth: DomoAuth,
    dataset_id: str,
    body: dict = None,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_loop: bool = False,
    debug_num_stacks_to_drop=2,
    parent_class=None,
):
    body = body or generate_list_partitions_body()

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/partition/list"

    offset_params = {
        "offset": "offset",
        "limit": "limit",
    }

    def arr_fn(res) -> list[dict]:
        return res.response

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        arr_fn=arr_fn,
        body=body,
        offset_params_in_body=True,
        offset_params=offset_params,
        loop_until_end=True,
        session=session,
        debug_loop=debug_loop,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if res.status == 404 and res.response == "Not Found":
        raise DatasetNotFoundError(dataset_id=dataset_id, res=res)

    if not res.is_success:
        raise Dataset_GetError(dataset_id=dataset_id, res=res)

    return res


def generate_create_dataset_body(
    dataset_name: str, dataset_type: str = "API", schema: dict = None
):
    schema = schema or {
        "columns": [
            {"type": "STRING", "name": "Friend"},
            {"type": "STRING", "name": "Attending"},
        ]
    }

    return {
        "userDefinedType": dataset_type,
        "dataSourceName": dataset_name,
        "schema": schema,
    }


@gd.route_function
async def create(
    auth: DomoAuth,
    dataset_name: str,
    dataset_type: str = "api",
    schema: dict = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
):
    body = generate_create_dataset_body(
        dataset_name=dataset_name, dataset_type=dataset_type, schema=schema
    )

    url = f"https://{auth.domo_instance}.domo.com/api/data/v2/datasources"

    res = await gd.get_data(
        auth=auth,
        method="POST",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Dataset_CRUDError(res=res)

    return res


def generate_enterprise_toolkit_body(
    dataset_name, dataset_description, datasource_type, columns_schema: List[dict]
):
    return {
        "dataSourceName": dataset_name,
        "dataSourceDescription": dataset_description,
        "dataSourceType": datasource_type,
        "schema": {"columns": columns_schema},
    }


def generate_remote_domostats_body(
    dataset_name, dataset_description, columns_schema: List[dict] = None
):
    return generate_enterprise_toolkit_body(
        dataset_name=dataset_name,
        dataset_description=dataset_description,
        columns_schema=columns_schema
        or [{"type": "STRING", "name": "Remote Domo Stats"}],
        datasource_type="ObservabilityMetrics",
    )


@gd.route_function
async def create_dataset_enterprise_tookit(
    auth: DomoAuth,
    payload: dict,  # call generate_enterprise_toolkit_body
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/datasets"

    res = await gd.get_data(
        auth=auth,
        method="POST",
        url=url,
        body=payload,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Dataset_CRUDError(res=res)

    return res


@gd.route_function
async def delete_partition_stage_1(
    auth: DomoAuth,
    dataset_id: str,
    dataset_partition_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
):
    """Delete partition has 3 stages
    # Stage 1. This marks the data version associated with the partition tag as deleted.
    It does not delete the partition tag or remove the association between the partition tag and data version.
    There should be no need to upload an empty file – step #3 will remove the data from Adrenaline.
    # update on 9/9/2022 based on the conversation with Greg Swensen"""

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/tag/{dataset_partition_id}/data"

    res = await gd.get_data(
        auth=auth,
        method="DELETE",
        url=url,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


@gd.route_function
async def delete_partition_stage_2(
    auth: DomoAuth,
    dataset_id: str,
    dataset_partition_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
):
    """This will remove the partition association so that it doesn’t show up in the list call.
    Technically, this is not required as a partition against a deleted data version will not count against the 400 partition limit
    but as the current partitions api doesn’t make that clear, cleaning these up will make it much easier for you to manage.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/partition/{dataset_partition_id}"

    res = await gd.get_data(
        auth=auth,
        method="DELETE",
        url=url,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


@gd.route_function
async def delete(
    auth: DomoAuth,
    dataset_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}?deleteMethod=hard"

    res = await gd.get_data(
        auth=auth,
        method="DELETE",
        url=url,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise Dataset_CRUDError(dataset_id=dataset_id, res=res)

    return res


class ShareDataset_AccessLevelEnum(DomoEnumMixin, Enum):
    CO_OWNER = "CO_OWNER"
    CAN_EDIT = "CAN_EDIT"
    CAN_SHARE = "CAN_SHARE"


def generate_share_dataset_payload(
    entity_type,  # USER or GROUP
    entity_id,
    access_level: ShareDataset_AccessLevelEnum = ShareDataset_AccessLevelEnum.CAN_SHARE,
    is_send_email: bool = False,
):
    return {
        "permissions": [
            {"type": entity_type, "id": entity_id, "accessLevel": access_level.value}
        ],
        "sendEmail": is_send_email,
    }


class ShareDataset_Error(de.DomoError):
    def __init__(self, dataset_id, res: rgd.ResponseGetData, message: str = None):
        message = message or res.response

        super().__init__(message=message, res=res, entity_id=dataset_id)


@gd.route_function
async def share_dataset(
    auth: DomoAuth,
    dataset_id: str,
    body: dict,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/share"

    res = await gd.get_data(
        auth=auth,
        method="POST",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ShareDataset_Error(dataset_id=dataset_id, res=res)

    update_user_ls = [f"{user['type']} - {user['id']}" for user in body["permissions"]]

    res.response = (
        f"updated access list {', '.join(update_user_ls)} added to {dataset_id}"
    )
    return res


@gd.route_function
async def get_permissions(
    auth: DomoAuth,
    dataset_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
    session: httpx.AsyncClient = None,
) -> rgd.ResponseGetData:
    """retrieve the schema for a dataset"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/permissions"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
    )

    if not res.is_success:
        raise Dataset_GetError(dataset_id=dataset_id, res=res)

    return res
