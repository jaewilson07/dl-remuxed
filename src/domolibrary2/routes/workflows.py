__all__ = [
    "Workflow_GET_Error",
    "Workflow_CRUD_Error",
    "get_workflow",
    "generate_trigger_workflow_body",
    "trigger_workflow",
    "get_workflow_trigger_history",
    "get_workflow_executions",
]

from typing import Optional

import httpx

from ..client import (
    get_data as gd,
    response as rgd,
)
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError


class Workflow_GET_Error(RouteError):
    """Raised when workflow retrieval operations fail."""

    def __init__(
        self,
        workflow_id: Optional[str] = None,
        message: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message or "Workflow retrieval failed",
            entity_id=workflow_id,
            res=res,
            **kwargs,
        )


class Workflow_CRUD_Error(RouteError):
    """Raised when workflow create, update, delete, or trigger operations fail."""

    def __init__(
        self,
        operation: str,
        workflow_id: Optional[str] = None,
        message: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"Workflow {operation} operation failed",
            entity_id=workflow_id,
            res=res,
            **kwargs,
        )


@gd.route_function
async def get_workflow(
    auth: DomoAuth,
    model_id: str,
    version_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: httpx.AsyncClient | None = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/workflow/v1/models/{model_id}/versions/{version_id}"
    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if not res.is_success:
        raise Workflow_GET_Error(workflow_id=model_id, res=res)

    return res


def generate_trigger_workflow_body(
    starting_tile, model_id, version_id, execution_params: dict
):
    return {
        "messageName": starting_tile,
        "version": version_id,
        "modelId": model_id,
        "data": execution_params,
    }


@gd.route_function
async def trigger_workflow(
    auth: DomoAuth,
    starting_tile: str,
    model_id: str,
    version_id: str,
    execution_parameters: Optional[dict] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: httpx.AsyncClient | None = None,
) -> rgd.ResponseGetData:
    body = generate_trigger_workflow_body(
        starting_tile=starting_tile,
        model_id=model_id,
        execution_params=execution_parameters,
        version_id=version_id,
    )

    url = f"https://{auth.domo_instance}.domo.com/api/workflow/v1/instances/message"

    res = await gd.get_data(
        method="POST",
        url=url,
        body=body,
        auth=auth,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if not res.is_success:
        raise Workflow_CRUD_Error(operation="trigger", workflow_id=model_id, res=res)

    return res


@gd.route_function
async def get_workflow_trigger_history(
    auth: DomoAuth,
    model_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: httpx.AsyncClient | None = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/workflow/v2/executions/{model_id}"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if not res.is_success:
        raise Workflow_GET_Error(workflow_id=model_id, res=res)

    return res


@gd.route_function
async def get_workflow_executions(
    auth: DomoAuth,
    model_id: str,
    version_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: httpx.AsyncClient | None = None,
) -> rgd.ResponseGetData:
    params = {
        "modelId": model_id,
        #   "triggerTypes" : "ALERT,API,APP_STUDIO,CUSTOM_APP,MANUAL,TIMER,WORKFLOW"
        "version": version_id,
        # "status"  : "IN_PROGRESS"
    }

    url = f"https://{auth.domo_instance}.domo.com/api/workflow/v2/executions"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        debug_api=debug_api,
        params=params,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    if not res.is_success:
        raise Workflow_GET_Error(workflow_id=model_id, res=res)

    return res
