"""Authentication routes and error handling for Domo API access.

This module provides authentication functions and custom exception classes
for various Domo authentication methods including username/password,
developer tokens, and access tokens.
"""

__all__ = [
    "AuthError",
    "InvalidCredentialsError",
    "AccountLockedError",
    "InvalidAuthTypeError",
    "InvalidInstanceError",
    "NoAccessTokenReturned",
    "get_full_auth",
    "get_developer_auth",
    "who_am_i",
    "elevate_user_otp",
]

from typing import Any, Optional

import httpx
from dc_logger.decorators import LogDecoratorConfig, log_call

from ..client import response as rgd
from ..client.exceptions import AuthError, RouteError
from ..utils.logging import ResponseGetDataProcessor


class InvalidCredentialsError(RouteError):
    """Raised when invalid credentials are provided to the API."""

    def __init__(self, res=None, **kwargs):
        super().__init__(
            res=res,
            message="Invalid credentials provided",
            **kwargs,
        )


class AccountLockedError(RouteError):
    """Raised when the user account is locked."""

    def __init__(self, res=None, **kwargs):
        super().__init__(
            res=res,
            message="User account is locked",
            **kwargs,
        )


class InvalidAuthTypeError(RouteError):
    """Raised when an invalid authentication type is used for an API call."""

    def __init__(
        self,
        res=None,
        required_auth_type: Optional[Any] = None,
        required_auth_type_ls: Optional[list[Any]] = None,
        **kwargs,
    ):
        # Convert class types to strings
        if required_auth_type:
            required_types = [required_auth_type.__name__]
        elif required_auth_type_ls:
            required_types = [auth_type.__name__ for auth_type in required_auth_type_ls]
        else:
            required_types = ["Unknown"]

        # Build message
        auth_list = ", ".join(required_types)
        message = f"This API requires: {auth_list}"

        super().__init__(
            res=res,
            message=message,
            **kwargs,
        )


class InvalidInstanceError(RouteError):
    """Raised when an invalid Domo instance is provided."""

    def __init__(self, res=None, domo_instance: Optional[str] = None, **kwargs):
        message = (
            f"Invalid Domo instance: {domo_instance}"
            if domo_instance
            else "Invalid Domo instance"
        )

        super().__init__(
            res=res,
            message=message,
            **kwargs,
        )


class NoAccessTokenReturnedError(RouteError):
    """Raised when no access token is returned from the authentication API."""

    def __init__(self, res=None, **kwargs):
        super().__init__(
            res=res,
            message="No access token returned from authentication API",
            **kwargs,
        )


@log_call(
    level_name="route",
    config=LogDecoratorConfig(result_processor=ResponseGetDataProcessor()),
)
async def get_full_auth(
    domo_instance: str,  # domo_instance.domo.com
    domo_username: str,  # email address
    domo_password: str,
    auth: Optional[Any] = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Authenticate using username and password to retrieve a full_auth access token.

    This function uses Domo's standard username/password authentication to obtain
    a session token that can be used for subsequent API calls.

    Args:
        domo_instance (str): The Domo instance identifier
        domo_username (str): User's email address
        domo_password (str): User's password
        auth (Optional[Any]): Existing auth object (optional)
        session (httpx.AsyncClient | None): HTTP client session to use
        debug_api (bool): Whether to enable API debugging
        parent_class (Optional[str]): Name of calling class for debugging
        debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
        return_raw (bool): Whether to return raw response without processing

    Returns:
        rgd.ResponseGetData: Response containing session token or error information

    Raises:
        InvalidInstanceError: If the Domo instance is invalid
        InvalidCredentialsError: If credentials are invalid or missing session token
        AccountLockedError: If the user account is locked
        NoAccessTokenReturned: If no access token is returned from the API
    """

    from ..client import get_data as gd

    domo_instance = domo_instance or (auth.domo_instance if auth else "")

    url = f"https://{domo_instance}.domo.com/api/content/v2/authentication"

    body = {
        "method": "password",
        "emailAddress": domo_username,
        "password": domo_password,
    }

    res = await gd.get_data(
        auth=auth,  # type: ignore  # Auth can be None for authentication endpoints
        method="POST",
        url=url,
        body=body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
        return_raw=return_raw,
    )

    if return_raw:
        # Type assertion for raw return
        return res  # type: ignore

    # Validate response type
    if not isinstance(res, rgd.ResponseGetData):
        raise TypeError(f"Expected ResponseGetData, got {type(res)}")

    # Handle specific error cases
    if res.status == 403 and res.response == "Forbidden":
        raise InvalidInstanceError(res=res, domo_instance=domo_instance)

    if res.is_success and isinstance(res.response, dict):
        reason = res.response.get("reason")

        if reason == "INVALID_CREDENTIALS":
            res.is_success = False
            raise InvalidCredentialsError(res=res)

        if reason == "ACCOUNT_LOCKED":
            res.is_success = False
            raise AccountLockedError(res=res)

        # Check for empty response
        if res.response == {} or res.response == "":
            res.is_success = False
            raise NoAccessTokenReturnedError(res=res)

    # Validate session token presence
    if isinstance(res.response, dict) and not res.response.get("sessionToken"):
        res.is_success = False
        raise InvalidCredentialsError(res=res)

    return res


@log_call(
    level_name="route",
    config=LogDecoratorConfig(result_processor=ResponseGetDataProcessor()),
)
async def get_developer_auth(
    domo_client_id: str,
    domo_client_secret: str,
    auth: Optional[Any] = None,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 1,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Authenticate using OAuth2 client credentials for developer APIs.

    This function is specifically for authenticating against APIs documented
    under developer.domo.com using OAuth2 client credentials flow.

    Args:
        domo_client_id (str): OAuth2 client ID from developer app registration
        domo_client_secret (str): OAuth2 client secret
        auth (Optional[Any]): Existing auth object (optional)
        session (httpx.AsyncClient | None): HTTP client session to use
        debug_api (bool): Whether to enable API debugging
        parent_class (Optional[str]): Name of calling class for debugging
        debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
        return_raw (bool): Whether to return raw response without processing

    Returns:
        rgd.ResponseGetData: Response containing access token or error information

    Raises:
        InvalidCredentialsError: If the client credentials are invalid
    """

    from ..client import get_data as gd

    url = "https://api.domo.com/oauth/token?grant_type=client_credentials"

    # Create session with basic auth if not provided
    if session is None:
        session = httpx.AsyncClient(
            auth=httpx.BasicAuth(domo_client_id, domo_client_secret)
        )

    res = await gd.get_data(
        method="GET",
        url=url,
        session=session,
        debug_api=debug_api,
        auth=auth,  # type: ignore  # Auth can be None for authentication endpoints
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        return_raw=return_raw,
    )

    if return_raw:
        # Type assertion for raw return
        return res  # type: ignore

    # Validate response type
    if not isinstance(res, rgd.ResponseGetData):
        raise TypeError(f"Expected ResponseGetData, got {type(res)}")

    # Handle authentication errors
    if res.status == 401 and res.response == "Unauthorized":
        res.is_success = False
        raise InvalidCredentialsError(res=res)

    return res


@log_call(
    level_name="route",
    config=LogDecoratorConfig(result_processor=ResponseGetDataProcessor()),
)
async def who_am_i(
    auth: Any,
    session: httpx.AsyncClient | None = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 0,
    debug_api: bool = False,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Validate authentication against the 'me' API endpoint.

    This function validates the authentication token by calling Domo's user 'me' API.
    This is the same authentication test the Domo Java CLI uses.

    Args:
        auth (Any): Authentication object containing domo_instance and auth tokens
        session (httpx.AsyncClient | None): HTTP client session to use
        parent_class (Optional[str]): Name of calling class for debugging
        debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
        debug_api (bool): Whether to enable API debugging
        return_raw (bool): Whether to return raw response without processing

    Returns:
        rgd.ResponseGetData: Response containing user information or error details

    Raises:
        InvalidInstanceError: If the Domo instance is invalid (403 Forbidden)
        InvalidCredentialsError: If the authentication token is invalid
    """

    from ..client import get_data as gd

    url = f"https://{auth.domo_instance}.domo.com/api/content/v2/users/me"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
        return_raw=return_raw,
    )

    if not res.is_success:
        # The @log_call decorator will handle error logging automatically
        pass

    if return_raw:
        # Type assertion for raw return
        return res  # type: ignore

    # Validate response type
    if not isinstance(res, rgd.ResponseGetData):
        raise TypeError(f"Expected ResponseGetData, got {type(res)}")

    # Handle specific error cases
    if res.status == 403 and res.response == "Forbidden":
        raise InvalidInstanceError(res=res)

    if res.status == 401 and res.response == "Unauthorized":
        res.is_success = False  # Fix typo: was is_sucess

    if not res.is_success:
        raise InvalidCredentialsError(res=res)

    return res


@log_call(
    level_name="route",
    config=LogDecoratorConfig(result_processor=ResponseGetDataProcessor()),
)
async def elevate_user_otp(
    auth: Any,
    one_time_password: str,
    user_id: Optional[str] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    session: httpx.AsyncClient | None = None,
    parent_class: Optional[str] = None,
) -> rgd.ResponseGetData:
    """Elevate authentication using a one-time password (OTP).

    This function is used when multi-factor authentication is enabled and
    an additional OTP verification step is required.

    Args:
        auth (Any): Authentication object containing domo_instance and tokens
        one_time_password (str): The OTP code for authentication elevation
        user_id (Optional[str]): User ID (will be retrieved from auth if not provided)
        debug_api (bool): Whether to enable API debugging
        debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
        session (httpx.AsyncClient | None): HTTP client session to use
        parent_class (Optional[str]): Name of calling class for debugging

    Returns:
        rgd.ResponseGetData: Response from the OTP elevation request

    Raises:
        InvalidCredentialsError: If the OTP is invalid or elevation fails
    """
    from ..client import get_data as gd

    # Get user_id from auth if not provided
    if not auth.user_id and not user_id:
        await auth.who_am_i()

    user_id = user_id or auth.user_id

    url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/authentication/elevations/{user_id}"

    body = {"timeBasedOneTimePassword": one_time_password}

    res = await gd.get_data(
        auth=auth,
        method="PUT",
        url=url,
        body=body,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
        session=session,
    )

    # Validate response type
    if not isinstance(res, rgd.ResponseGetData):
        raise TypeError(f"Expected ResponseGetData, got {type(res)}")

    if not res.is_success:
        raise InvalidCredentialsError(res=res)

    return res
