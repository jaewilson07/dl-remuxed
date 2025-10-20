__all__ = [
    "ENGINES",
    "create_integration_body",
    "Cloud_Amplifier_Error",
    "get_integrations",
    "get_integration_by_id",
    "get_integration_permissions",
    "check_for_colliding_datasources",
    "get_federated_source_metadata",
    "get_integration_warehouses",
    "get_databases",
    "get_schemas",
    "get_tables",
    "convert_federated_to_cloud_amplifier",
    "create_integration",
    "update_integration_warehouses",
    "update_integration",
    "delete_integration",
]

from typing import Any, Literal, Optional

import httpx

from ..client import auth as dmda
from ..client import DomoError as dmde
from ..client import get_data as gd
from ..client import response as rgd

# TODO: Expand to include all engines
ENGINES = Literal["SNOWFLAKE", "BIGQUERY"]


def create_integration_body(
    engine: ENGINES,
    description: str,
    friendly_name: str,
    service_account_id: str,
    auth_method: str,
    admin_auth_method: str,
):
    body = {
        "engine": engine,
        "properties": {
            "friendlyName": {
                "key": "friendlyName",
                "configType": "CONFIG",
                "value": friendly_name,
            },
            "description": {
                "key": "description",
                "configType": "CONFIG",
                "value": description,
            },
            "serviceAccountId": {
                "key": "serviceAccountId",
                "configType": "CONFIG",
                "value": service_account_id,
            },
            "AUTH_METHOD": {
                "key": "AUTH_METHOD",
                "configType": "CONFIG",
                "value": auth_method,
            },
            "ADMIN_AUTH_METHOD": {
                "key": "ADMIN_AUTH_METHOD",
                "configType": "CONFIG",
                "value": admin_auth_method,
            },
        },
    }
    return body


class Cloud_Amplifier_Error(dmde.RouteError):
    def __init__(
        self, res: rgd.ResponseGetData, account_id: str = "", message: str = ""
    ):
        super().__init__(res=res, message=message, entity_id=account_id)


@gd.route_function
async def get_integrations(
    auth: dmda.DomoAuth,
    integration_engine: Optional[ENGINES] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Retrieves a list of all the integrations.
    """

    api_type = "data"
    params = None

    if integration_engine:  # Change to query if engine is provided to filter by engine
        api_type = "query"
        params = {"deviceEngine": integration_engine}

    url = f"https://{auth.domo_instance}.domo.com/api/{api_type}/v1/byos/accounts"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
        params=params,
    )

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def get_integration_by_id(
    auth: dmda.DomoAuth,
    integration_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Retrieves a list of all the integrations.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/accounts/{integration_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )
    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)
    return res


@gd.route_function
async def get_integration_permissions(
    auth: dmda.DomoAuth,
    user_id: str = None,
    integration_ids: list[str] = [],
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Retrieves a list of all the integrations.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/accounts/permissions/list"

    body = {}

    if user_id:
        body.update({"userId": user_id})

    if integration_ids:
        body.update({"integrationIds": integration_ids})

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )
    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)
    return res


@gd.route_function
async def check_for_colliding_datasources(
    auth: dmda.DomoAuth,
    dataset_id: str,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Checks for Cloud Amplifier integrations that collide with an existing Domo Dataset.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/migration/integrations/datasource/{dataset_id}"

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

    # A 400 may be returned if no federated metadata exists for the dataset
    if res.status == 400:
        raise Cloud_Amplifier_Error(
            res=res,
            message=f"No federated metadata exists for the datasource {dataset_id}",
        )

    if not res.is_success and res.status != 400:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def get_federated_source_metadata(
    auth: dmda.DomoAuth,
    dataset_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Retrieves federated source metadata for a dataset.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/federated/v1/config/datasources/{dataset_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    # A 404 may be returned if no federated metadata exists for the dataset
    if res.status == 404:
        raise Cloud_Amplifier_Error(
            res=res,
            message=f"Could not find a federated datasource with id: {dataset_id}",
        )

    if not res.is_success and res.status != 404:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def get_integration_warehouses(
    auth: dmda.DomoAuth,
    integration_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Lists available compute warehouses for a Cloud Amplifier integration. User must have permission to view the integration.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/warehouses/{integration_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )
    if res.status == 403:
        raise Cloud_Amplifier_Error(
            res=res,
            message=f"User may not have permission to view the warehouses - {integration_id}",
        )

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def get_databases(
    auth: dmda.DomoAuth,
    integration_id: str,
    page: int = 0,
    rows: int = 5000,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Retrieves a list of all the databases for a Cloud Amplifier integration.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/accounts/{integration_id}/databases"

    params = {"page": page, "rows": rows}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
        params=params,
    )

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def get_schemas(
    auth: dmda.DomoAuth,
    integration_id: str,
    database: str,
    page: int = 0,
    rows: int = 5000,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Retrieves a list of all the schemas for a Cloud Amplifier integration.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/accounts/{integration_id}/databases/{database}/schemas"

    params = {"page": page, "rows": rows}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
        params=params,
    )

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def get_tables(
    auth: dmda.DomoAuth,
    integration_id: str,
    database: str,
    schema: str,
    page: int = 0,
    rows: int = 5000,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Retrieves a list of all the tables for a Cloud Amplifier integration.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/accounts/{integration_id}/databases/{database}/schemas/{schema}/objects"

    params = {"page": page, "rows": rows}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        params=params,
        session=session,
    )

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def convert_federated_to_cloud_amplifier(
    auth: dmda.DomoAuth,
    federated_dataset_id: str,
    cloud_amplifier_integration_id: str,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Converts a federated dataset to use a Cloud Amplifier integration.
    """

    url = (
        f"https://{auth.domo_instance}.domo.com/api/query/migration/federated/to/amplifier/"
        f"{federated_dataset_id}/integrations/{cloud_amplifier_integration_id}"
    )

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body={},
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def create_integration(
    auth: dmda.DomoAuth,
    engine: ENGINES,
    friendly_name: str,
    service_account_id: str,
    auth_method: str,
    description: str = "",
    admin_auth_method: Optional[str] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Creates a new Cloud Amplifier integration.
    """

    if admin_auth_method is None:
        admin_auth_method = auth_method

    body = create_integration_body(
        engine=engine,
        friendly_name=friendly_name,
        service_account_id=service_account_id,
        auth_method=auth_method,
        admin_auth_method=admin_auth_method,
        description=description,
    )

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/accounts"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)

    return res


@gd.route_function
async def update_integration_warehouses(
    auth: dmda.DomoAuth,
    integration_id: str,
    warehouses: list[dict[str, Any]],
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Updates the compute warehouses for a Cloud Amplifier integration.
    Expects a list of warehouse dicts as returned by the GET warehouses endpoint.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/warehouses/{integration_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=warehouses,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if res and not res.is_success:
        # Using POST error class for non-GET write operations
        raise Cloud_Amplifier_Error(res=res)
    return res


@gd.route_function
async def update_integration(
    auth: dmda.DomoAuth,
    integration_id: str,
    update_body: dict[str, Any],
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Updates a Cloud Amplifier integration.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/byos/accounts/{integration_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=update_body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if return_raw:
        return res

    if res and not res.is_success:
        raise Cloud_Amplifier_Error(res=res)
    return res


@gd.route_function
async def delete_integration(
    auth: dmda.DomoAuth,
    integration_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
):
    """
    Deletes a Cloud Amplifier integration.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/byos/accounts/{integration_id}"

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
        raise Cloud_Amplifier_Error(res=res)
    return res
