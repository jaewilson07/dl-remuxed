"""
Application Route Functions

This module provides functions for managing Domo applications including retrieval,
job management, and execution operations. Applications in Domo are containers for
scheduled jobs that perform various automated tasks.

Functions:
    get_applications: Retrieve all applications in the instance
    get_application_by_id: Retrieve a specific application by ID
    get_application_jobs: Retrieve all jobs for a specific application
    get_application_job_by_id: Retrieve a specific application job by ID
    create_application_job: Create a new job in an application
    update_application_job: Update an existing application job
    update_application_job_trigger: Update a job trigger configuration
    execute_application_job: Execute a specific application job
    get_available_rds_reports_step1: Get available RDS reports (step 1)
    get_available_rds_reports_step2: Get available RDS reports (step 2)
    generate_remote_domostats: Generate remote domostats configuration
    generate_body_watchdog_generic: Generate watchdog job configuration

Exception Classes:
    Application_GET_Error: Raised when application retrieval fails
    SearchApplication_NotFound: Raised when application search returns no results
    Application_CRUD_Error: Raised when application create/update/delete operations fail
"""

__all__ = [
    "Application_GET_Error",
    "SearchApplication_NotFound",
    "Application_CRUD_Error",
    "get_applications",
    "get_application_by_id",
    "get_application_jobs",
    "get_application_job_by_id",
    "generate_remote_domostats",
    "generate_body_watchdog_generic",
    "create_application_job",
    "update_application_job",
    "update_application_job_trigger",
    "execute_application_job",
    "get_available_rds_reports_step1",
    "get_available_rds_reports_step2",
]

from pprint import pprint
from typing import Optional, Union

import httpx

from ..client import get_data as gd, response as rgd
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError


class Application_GET_Error(RouteError):
    """
    Raised when application retrieval operations fail.

    This exception is used for failures during GET operations on applications,
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
                message = f"Failed to retrieve application {entity_id}"
            else:
                message = "Failed to retrieve applications"

        super().__init__(message=message, entity_id=entity_id, res=res, **kwargs)


class SearchApplication_NotFound(RouteError):
    """
    Raised when application search operations return no results.

    This exception is used when searching for specific applications that
    don't exist or when search criteria match no applications.
    """

    def __init__(
        self,
        search_criteria: str,
        res: Optional[rgd.ResponseGetData] = None,
        **kwargs,
    ):
        message = f"No applications found matching: {search_criteria}"
        super().__init__(
            message=message,
            res=res,
            **kwargs,
        )


class Application_CRUD_Error(RouteError):
    """
    Raised when application create, update, or delete operations fail.

    This exception is used for failures during application job creation,
    modification, or execution operations.
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
                message = f"Application {operation} failed for application {entity_id}"
            else:
                message = f"Application {operation} operation failed"

        super().__init__(
            message=message,
            entity_id=entity_id,
            res=res,
            **kwargs,
        )


@gd.route_function
async def get_applications(
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Retrieve all applications for the authenticated instance.

    Fetches a list of all applications in the current Domo instance.
    Applications are containers for scheduled jobs that perform automated tasks.

    Args:
        auth: Authentication object containing instance and credentials
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing list of applications

    Raises:
        Application_GET_Error: If application retrieval fails or API returns an error

    Example:
        >>> apps_response = await get_applications(auth)
        >>> for app in apps_response.response:
        ...     print(f"Application: {app['name']}")
    """
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Application_GET_Error(res=res)

    return res


@gd.route_function
async def get_application_by_id(
    auth: DomoAuth,
    application_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """
    Retrieve a specific application by its ID.

    Fetches details for a single application identified by its unique ID.

    Args:
        auth: Authentication object containing instance and credentials
        application_id: Unique identifier for the application to retrieve
        session: Optional HTTP client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to omit in debug output
        parent_class: Name of calling class for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing the specific application data

    Raises:
        Application_GET_Error: If application retrieval fails
        SearchApplication_NotFound: If no application with the specified ID exists

    Example:
        >>> app_response = await get_application_by_id(auth, "app-123")
        >>> app_data = app_response.response
        >>> print(f"Application Name: {app_data['name']}")
    """
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        if res.status == 404:
            raise SearchApplication_NotFound(
                search_criteria=f"ID: {application_id}",
                res=res,
            )
        else:
            raise Application_GET_Error(
                entity_id=application_id,
                res=res,
            )

    return res


class ApplicationError_NoJobRetrieved(DomoError):
    def __init__(
        self,
        domo_instance,
        application_id=None,
        parent_class=None,
        function_name=None,
    ):
        message = f"no jobs retrieved from application - {application_id}"

        super().__init__(
            message=message,
            parent_class=parent_class,
            function_name=function_name,
            domo_instance=domo_instance,
        )


gd.route_function


async def get_application_jobs(
    auth: DomoAuth,
    application_id: str,
    parent_class: str = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
) -> rgd.ResponseGetData:
    offset_params = {"offset": "offset", "limit": "limit"}

    url = f"https://{auth.domo_instance}.domo.com/api/executor/v2/applications/{application_id}/jobs"

    def arr_fn(res) -> list[dict]:
        return res.response.get("jobs")

    res = await gd.looper(
        auth=auth,
        method="GET",
        url=url,
        arr_fn=arr_fn,
        loop_until_end=True,
        offset_params=offset_params,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ApplicationError_NoJobRetrieved(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


@gd.route_function
async def get_application_job_by_id(
    auth: DomoAuth,
    application_id: str,
    job_id: str,
    parent_class: str = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ApplicationError_NoneRetrieved(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
            job_id=job_id,
        )

    return res


def generate_remote_domostats(
    target_instance: str,
    report_dict: dict,
    output_dataset_id: str,
    account_id: str,
    schedule_ls: list,
    execution_timeout: int = 1440,
    debug_api: bool = False,
):
    instance_url = f"{target_instance}.domo.com"

    body = {
        "jobName": instance_url,
        "jobDescription": f"Get Remote stat from {instance_url}",
        "executionTimeout": execution_timeout,
        "executionPayload": {
            "remoteInstance": instance_url,
            "policies": report_dict,
            "metricsDatasetId": output_dataset_id,
        },
        "accounts": [account_id],
        "executionClass": "com.domo.executor.subscriberstats.SubscriberStatsExecutor",
        "resources": {"requests": {"memory": "256M"}, "limits": {"memory": "256M"}},
        "triggers": schedule_ls,
    }

    if debug_api:
        pprint(body)

    return body


def generate_body_watchdog_generic(
    job_name: str,
    notify_user_ids_ls: list,
    notify_group_ids_ls: list,
    notify_emails_ls: list,
    log_dataset_id: str,
    schedule_ls: list,
    watchdog_parameter_body: dict,
    execution_timeout=1440,
    debug_api: bool = False,
):
    body = {
        "jobName": job_name,
        "jobDescription": f"Watchdog for {job_name}",
        "executionTimeout": execution_timeout,
        "accounts": [],
        "executionPayload": {
            "notifyUserIds": notify_user_ids_ls or [],
            "notifyGroupIds": notify_group_ids_ls or [],
            "notifyEmailAddresses": notify_emails_ls or [],
            "watcherParameters": watchdog_parameter_body,
            "metricsDatasetId": log_dataset_id,
        },
        "resources": {"requests": {"memory": "256Mi"}, "limits": {"memory": "256Mi"}},
        "triggers": schedule_ls,
    }

    if debug_api:
        pprint(body)

    return body


class CRUD_ApplicationJob_Error(DomoError):
    def __init__(
        self, domo_instance, application_id, message, parent_class, function_name
    ):
        super().__init__(
            self,
            domo_instance=domo_instance,
            entity_id=application_id,
            parent_class=parent_class,
            function_name=function_name,
            message=message,
        )


# create the new RemoteDomostats job


@gd.route_function
async def create_application_job(
    auth: DomoAuth,
    body: dict,
    application_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    parent_class: str = None,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise CRUD_ApplicationJob_Error(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            message=res.response,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


# update the job
@gd.route_function
async def update_application_job(
    auth: DomoAuth,
    body: dict,
    job_id: str,
    application_id: str,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}"

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success:
        raise CRUD_ApplicationJob_Error(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            message=res.response,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


@gd.route_function
async def update_application_job_trigger(
    auth: DomoAuth,
    body: dict,
    job_id: str,
    trigger_id: str,
    application_id: str,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: Union[httpx.AsyncClient, httpx.AsyncClient, None] = None,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}/triggers/{trigger_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise CRUD_ApplicationJob_Error(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            message=res.response,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


@gd.route_function
async def execute_application_job(
    auth: DomoAuth,
    application_id,
    job_id,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}/executions"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body={},
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise CRUD_ApplicationJob_Error(
            domo_instance=auth.domo_instance,
            application_id=application_id,
            message=res.response,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res


@gd.route_function
async def get_available_rds_reports_step1(
    auth: DomoAuth,
    application_id,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/executions"

    body = {"executionPayload": {"retrieveAvailableReports": True}}

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise Application_GET_Error(res=res)

    return res


@gd.route_function
async def get_available_rds_reports_step2(
    auth: DomoAuth,
    application_id,
    job_id,
    execution_id,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class: str = None,
    session: httpx.AsyncClient = None,
):
    url = f"https://{auth.domo_instance}.domo.com/api/executor/v1/applications/{application_id}/jobs/{job_id}/executions/{execution_id}?includeTransient=true"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise Application_GET_Error(res=res)

    return res
