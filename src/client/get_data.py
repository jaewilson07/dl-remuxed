__all__ = [
    "GetData_Error",
    "get_data",
    "get_data_stream",
    "LooperError",
    "looper",
    "RouteFunction_ResponseTypeError",
    "route_function",
]

import time
from functools import wraps
from pprint import pprint
from typing import Any, Callable, Optional, Tuple, Union

import httpx
import json

from . import auth as dmda
from .exceptions import DomoError
from . import Logger as dl
from . import response as rgd
from ..utils import chunk_execution as dmce


class GetData_Error(DomoError):
    def __init__(self, message, url):
        super().__init__(message=message, domo_instance=url)


def create_headers(
    auth: Optional[
        "dmda.DomoAuth"
    ],  # The authentication object containing the Domo API token.
    content_type: Optional[
        str
    ] = None,  # The content type for the request. Defaults to None.
    headers: Optional[
        dict
    ] = None,  # Any additional headers for the request. Defaults to None.
) -> dict:  # The headers for the request.
    """
    Creates default headers for interacting with Domo APIs.
    """

    if headers is None:
        headers = {}

    headers = {
        "Content-Type": content_type or "application/json",
        "Connection": "keep-alive",
        "accept": "application/json, text/plain",
        **headers,
    }
    if auth:
        headers.update(**auth.auth_header)
    return headers


def create_httpx_session(
    session: Optional[httpx.AsyncClient] = None, is_verify: bool = False
) -> Tuple[httpx.AsyncClient, bool]:
    """Creates or reuses an asynchronous HTTPX session.

    Args:
        session: An optional existing HTTPX AsyncClient session.
        is_verify: Boolean flag for SSL verification.

    Returns:
        A tuple containing the HTTPX session and a boolean indicating if the session should be closed.
    """
    is_close_session = False

    if session is None:
        is_close_session = True
        session = httpx.AsyncClient(verify=is_verify)
    return session, is_close_session


@dmce.run_with_retry()
async def get_data(
    url: str,
    method: str,
    auth: Optional["dmda.DomoAuth"] = None,
    content_type: Optional[str] = None,
    headers: Optional[dict] = None,
    body: Union[dict, list, str, None] = None,
    params: Optional[dict] = None,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    return_raw: bool = False,
    is_follow_redirects: bool = False,
    timeout: int = 20,
    parent_class: Optional[str] = None,  # noqa: ARG001
    num_stacks_to_drop: int = 2,  # noqa: ARG001
    debug_traceback: bool = False,  # noqa: ARG001
    is_verify: bool = False,
) -> rgd.ResponseGetData:
    """Asynchronously performs an HTTP request to retrieve data from a Domo API endpoint."""

    if debug_api:
        print(f"🐛 Debugging get_data: {method} {url}")

    headers = create_headers(
        auth=auth, content_type=content_type, headers=headers or {}
    )

    session, is_close_session = create_httpx_session(
        session=session, is_verify=is_verify
    )
    if not isinstance(body, str):
        body = json.dumps(body)

    # Create request metadata
    request_metadata = rgd.RequestMetadata(
        url=url,
        headers=headers,
        body=body,
        params=params,
    )

    # Create additional information with parent_class and traceback_details
    additional_information = {}
    if parent_class:
        additional_information["parent_class"] = parent_class
    if debug_traceback:
        traceback_details = dl.get_traceback(
            num_stacks_to_drop=num_stacks_to_drop,
            root_module="<module>",
            parent_class=parent_class or "",
            debug_traceback=debug_traceback,
        )
        additional_information["traceback_details"] = traceback_details

    try:
        response = await session.request(
            method=method,
            url=url,
            headers=headers,
            json=body if isinstance(body, dict) else None,
            content=body if isinstance(body, str) else None,
            params=params,
            follow_redirects=is_follow_redirects,
            timeout=timeout,
        )

        if debug_api:
            print(f"Response Status: {response.status_code}")

        # Check for VPN block
        if response.status_code in range(200, 400):
            if "<title>Domo - Blocked</title>" in response.text:
                ip_address = rgd.find_ip(response.text)
                # Create a custom response for VPN block with 403 status
                vpn_response = rgd.ResponseGetData(
                    status=403,  # Forbidden - blocked by VPN
                    response=f"Blocked by VPN: {ip_address}",
                    is_success=False,
                    request_metadata=request_metadata,
                    additional_information=additional_information,
                )
                return vpn_response

        # Return raw response if requested
        if return_raw:
            return rgd.ResponseGetData(
                status=response.status_code,
                response=response,
                is_success=True,
                request_metadata=request_metadata,
                additional_information=additional_information,
            )

        # Process response into ResponseGetData using from_httpx_response
        return rgd.ResponseGetData.from_httpx_response(
            res=response,
            request_metadata=request_metadata,
            additional_information=additional_information,
        )

    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    finally:
        if is_close_session:
            await session.aclose()


@dmce.run_with_retry()
async def get_data_stream(
    url: str,
    auth: dmda.DomoAuth,
    method: str = "GET",
    content_type: Optional[str] = None,
    headers: Optional[dict] = None,
    # body: Union[dict, str, None] = None,
    params: Optional[dict] = None,
    debug_api: bool = False,
    timeout: int = 10,  # noqa: ARG001
    parent_class: Optional[str] = None,  # name of the parent calling class
    num_stacks_to_drop: int = 2,  # number of stacks to drop from the stack trace.  see `domolibrary.client.Logger.TracebackDetails`.  use 2 with class > route structure.  use 1 with route based approach
    debug_traceback: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    is_verify: bool = False,
    is_follow_redirects: bool = True,
) -> rgd.ResponseGetData:
    """Asynchronously streams data from a Domo API endpoint.

    Args:
        url: API endpoint URL.
        auth: Authentication object for Domo APIs.
        method: HTTP method to use, default is GET.
        content_type: Optional content type header.
        headers: Additional HTTP headers.
        params: Query parameters for the request.
        debug_api: Enable debugging information.
        timeout: Maximum time to wait for a response (in seconds).
        parent_class: (Optional) Name of the calling class.
        num_stacks_to_drop: Number of stack frames to drop in the traceback.
        debug_traceback: Enable detailed traceback debugging.
        session: Optional HTTPX session to be used.
        is_verify: SSL verification flag.
        is_follow_redirects: Follow HTTP redirects if True.

    Returns:
        An instance of ResponseGetData containing the streamed response data.
    """

    create_httpx_session(session=session, is_verify=is_verify)
    if debug_api:
        print("🐛 debugging get_data")

    if auth and not auth.token:
        await auth.get_auth_token()

    if headers is None:
        headers = {}

    headers = {
        "Content-Type": content_type or "application/json",
        "Connection": "keep-alive",
        "accept": "application/json, text/plain",
        **headers,
    }

    if auth:
        headers.update(**auth.auth_header)

    # Create request metadata
    request_metadata = rgd.RequestMetadata(
        url=url,
        headers=headers,
        body=None,  # No body in stream function
        params=params,
    )

    # Create additional information with parent_class and traceback_details
    additional_information = {}
    if parent_class:
        additional_information["parent_class"] = parent_class

    traceback_details = dl.get_traceback(
        num_stacks_to_drop=num_stacks_to_drop,
        root_module="<module>",
        parent_class=parent_class or "",
        debug_traceback=debug_traceback,
    )
    additional_information["traceback_details"] = traceback_details

    if debug_api:
        pprint(
            {
                "method": method,
                "url": url,
                "headers": headers,
                # "body": body,
                "params": params,
                "traceback_details": traceback_details,
            }
        )

    try:
        async with session or httpx.AsyncClient(verify=False) as client:
            async with client.stream(
                method,
                url=url,
                headers=headers,
                follow_redirects=is_follow_redirects,
                timeout=timeout,
            ) as res:
                if res.status_code != 200:
                    return rgd.ResponseGetData(
                        status=res.status_code,
                        response=res.text if hasattr(res, "text") else str(res.content),
                        is_success=False,
                        request_metadata=request_metadata,
                        additional_information=additional_information,
                    )

                content = bytearray()
                async for chunk in res.aiter_bytes():
                    content += chunk

                return rgd.ResponseGetData(
                    status=res.status_code,
                    response=content,
                    is_success=True,
                    request_metadata=request_metadata,
                    additional_information=additional_information,
                )

    except httpx.TransportError as e:
        raise GetData_Error(url=url, message=e) from e


class LooperError(DomoError):
    def __init__(self, loop_stage: str, message):
        super().__init__(message=f"{loop_stage} - {message}")


async def looper(
    auth: dmda.DomoAuth,
    session: Optional[httpx.AsyncClient],
    url,
    offset_params,
    arr_fn: Callable,
    loop_until_end: bool = False,  # usually you'll set this to true.  it will override maximum
    method="POST",
    body: Optional[dict] = None,
    fixed_params: Optional[dict] = None,
    offset_params_in_body: bool = False,
    body_fn=None,
    limit=1000,
    skip=0,
    maximum=0,
    debug_api: bool = False,
    debug_loop: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    timeout: int = 10,
    wait_sleep: int = 0,
    is_verify: bool = False,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Iteratively retrieves paginated data from a Domo API endpoint.

    Args:
        auth: Authentication object for Domo APIs.
        session: HTTPX AsyncClient session used for making requests.
        url: API endpoint URL for data retrieval.
        offset_params: Dictionary specifying the pagination keys (e.g., 'offset', 'limit').
        arr_fn: Function to extract records from the API response.
        loop_until_end: If True, continues fetching until no new records are returned.
        method: HTTP method to use (default is POST).
        body: Request payload (if required).
        fixed_params: Fixed query parameters to include in every request.
        offset_params_in_body: Whether to include pagination parameters inside the request body.
        body_fn: Function to modify the request body before each request.
        limit: Number of records to retrieve per request.
        skip: Initial offset value.
        maximum: Maximum number of records to retrieve.
        debug_api: Enable debugging output for API calls.
        debug_loop: Enable debugging output for the looping process.
        debug_num_stacks_to_drop: Number of stack frames to drop in traceback for debugging.
        parent_class: (Optional) Name of the calling class.
        timeout: Request timeout value.
        wait_sleep: Time to wait between consecutive requests (in seconds).
        is_verify: SSL verification flag.
        return_raw: Flag to return the raw response instead of processed data.

    Returns:
        An instance of ResponseGetData containing the aggregated data and pagination metadata.
    """
    is_close_session = False

    session, is_close_session = create_httpx_session(session, is_verify=is_verify)

    allRows = []
    isLoop = True

    res: Optional[rgd.ResponseGetData] = None

    if maximum and maximum <= limit and not loop_until_end:
        limit = maximum

    while isLoop:
        params = fixed_params or {}

        if offset_params_in_body:
            if body is None:
                body = {}
            body.update(
                {offset_params.get("offset"): skip, offset_params.get("limit"): limit}
            )

        else:
            params.update(
                {offset_params.get("offset"): skip, offset_params.get("limit"): limit}
            )

        if body_fn:
            try:
                body = body_fn(skip, limit, body)

            except Exception as e:
                await session.aclose()
                raise LooperError(
                    loop_stage="processing body_fn", message=str(e)
                ) from e

        if debug_loop:
            print(f"\n🚀 Retrieving records {skip} through {skip + limit} via {url}")
            # pprint(params)

        res = await get_data(
            auth=auth,
            url=url,
            method=method,
            params=params,
            session=session,
            body=body,
            debug_api=debug_api,
            timeout=timeout,
            parent_class=parent_class,
            num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if not res or not res.is_success:
            if is_close_session:
                await session.aclose()

            return res or rgd.ResponseGetData(
                status=500, response="No response", is_success=False
            )

        if return_raw:
            return res

        try:
            newRecords = arr_fn(res)

        except Exception as e:
            await session.aclose()
            raise LooperError(loop_stage="processing arr_fn", message=str(e)) from e

        allRows += newRecords

        if len(newRecords) == 0:
            isLoop = False

        if maximum and len(allRows) >= maximum and not loop_until_end:
            isLoop = False

        if debug_loop:
            print({"all_rows": len(allRows), "new_records": len(newRecords)})
            print(f"skip: {skip}, limit: {limit}")

        if maximum and skip + limit > maximum and not loop_until_end:
            limit = maximum - len(allRows)

        skip += len(newRecords)
        time.sleep(wait_sleep)

    if debug_loop:
        print(
            f"\n🎉 Success - {len(allRows)} records retrieved from {url} in query looper\n"
        )

    if is_close_session:
        await session.aclose()

    if not res:
        return rgd.ResponseGetData(
            status=500, response="No response received", is_success=False
        )

    return await rgd.ResponseGetData.from_looper(res=res, array=allRows)


class RouteFunction_ResponseTypeError(TypeError):
    def __init__(self, result):
        super().__init__(
            f"Expected function to return an instance of ResponseGetData got {type(result)} instead.  Refactor function to return ResponseGetData class"
        )


def route_function(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator for route functions to ensure they receive certain arguments.
    If these arguments are not provided, default values are used.

    Args:
        func (Callable[..., Any]): The function to decorate.

    Returns:
        Callable[..., Any]: The decorated function.

    The decorated function takes the following arguments:
        *args (Any): Positional arguments for the decorated function.
        parent_class (str, optional): The parent class. Defaults to None.
        debug_num_stacks_to_drop (int, optional): The number of stacks to drop for debugging. Defaults to 1.
        debug_api (bool, optional): Whether to debug the API. Defaults to False.
        session (httpx.AsyncClient, optional): The HTTPX client session. Defaults to None.
        **kwargs (Any): Additional keyword arguments for the decorated function.
    """

    @wraps(func)
    async def wrapper(
        *args: Any,
        parent_class: Optional[str] = None,
        debug_num_stacks_to_drop: int = 1,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        **kwargs: Any,
    ) -> Any:
        result = await func(
            *args,
            parent_class=parent_class,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            debug_api=debug_api,
            session=session,
            **kwargs,
        )

        if not isinstance(result, rgd.ResponseGetData):
            raise RouteFunction_ResponseTypeError(result)

        return result

    return wrapper
