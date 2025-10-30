"""Domo authentication classes for various authentication methods."""

__all__ = [
    "DomoAuth",
    "test_is_full_auth",
    "DomoTokenAuth",
    "DomoDeveloperAuth",
    "DomoJupyterAuth",
    "DomoJupyterFullAuth",
    "DomoJupyterTokenAuth",
    "test_is_jupyter_auth",
]

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Union

import httpx
from dc_logger.decorators import log_call

from .exceptions import AuthError
from .response import ResponseGetData


class _DomoAuth_Required(ABC):
    """Abstract base class for required Domo authentication parameters.

    This class provides the minimal required functionality for Domo authentication,
    including instance validation and manual login URL generation.

    Attributes:
        domo_instance (str): The Domo instance identifier (e.g., 'mycompany' or 'mycompany.domo.com')
    """

    def __init__(self, domo_instance: str):
        """Initialize with required Domo instance.

        Args:
            domo_instance (str): The Domo instance identifier

        Raises:
            InvalidInstanceError: If domo_instance is empty or None
        """
        if not domo_instance:
            raise AuthError(message="Domo instance is required. Example: 'mycompany'")

        self.domo_instance = domo_instance

    @property
    def url_manual_login(self) -> str:
        """Generate the manual login URL for the Domo instance.

        Returns:
            str: The complete URL for manual login to the Domo instance
        """
        return f"https://{self.domo_instance}.domo.com/auth/index?domoManualLogin=true"


class _DomoAuth_Optional(ABC):
    """Abstract base class for optional Domo authentication functionality.

    This class provides common authentication methods and token management
    functionality that can be shared across different authentication types.

    Attributes:
        domo_instance (str): The Domo instance identifier
        token_name (Optional[str]): Name identifier for the token
        token (Optional[str]): The authentication token
        user_id (Optional[str]): The authenticated user's ID
        is_valid_token (bool): Whether the current token is valid
    """

    def __init__(
        self,
        domo_instance: str,
        token_name: Optional[str] = None,
        token: Optional[str] = None,
        user_id: Optional[str] = None,
        is_valid_token: bool = False,
    ):
        """Initialize optional authentication parameters.

        Args:
            domo_instance (str): The Domo instance identifier
            token_name (Optional[str]): Name identifier for the token
            token (Optional[str]): The authentication token
            user_id (Optional[str]): The authenticated user's ID
            is_valid_token (bool): Whether the current token is valid

        Raises:
            InvalidInstanceError: If domo_instance is empty or None
        """
        self.domo_instance = domo_instance
        self.token_name = token_name
        self.token = token
        self.user_id = user_id
        self.is_valid_token = is_valid_token

        self._set_token_name()

        if not self.domo_instance:
            raise AuthError(
                message="Domo instance is required. Example: 'mycompany.domo.com' or 'mycompany'"
            )

    def _set_token_name(self):
        """Set default token name to domo_instance if not provided."""
        if not self.token_name:
            self.token_name = self.domo_instance

    @property
    @abstractmethod
    def auth_header(self) -> dict:
        """Generate authentication headers for API requests.

        Returns:
            dict: HTTP headers containing authentication information

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement auth_header property.")

    @log_call(action_name="class")
    async def who_am_i(
        self,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ) -> ResponseGetData:
        """Perform an API call to identify the user associated with the token.

        This method validates the authentication token by calling the Domo 'me' API
        endpoint and updates the user_id and token validity status.

        Args:
            session (Optional[httpx.AsyncClient]): HTTP client session to use for the request
            debug_api (bool): Whether to enable API debugging
            debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging

        Returns:
            ResponseGetData: Response containing user information and success status

        Raises:
            TypeError: If the response is not of expected ResponseGetData type
        """
        # Create session if not provided

        from ..routes import auth as auth_routes

        # logger = get_global_logger()
        if logger:
            await logger.info("Executing who_am_i for token validation.")

        res = await auth_routes.who_am_i(
            auth=self,
            parent_class=self.__class__.__name__,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        # Type assertion for proper typing
        if res.is_success:
            self.is_valid_token = True

        if res.response and isinstance(res.response, dict):
            self.user_id = res.response.get("id")

        return res

    async def elevate_otp(
        self,
        one_time_password: str,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        """Elevate the authentication to include OTP (One-Time Password) if required.

        This method is used when multi-factor authentication is enabled and an
        additional OTP verification step is required.

        Args:
            one_time_password (str): The OTP code for authentication elevation
            debug_api (bool): Whether to enable API debugging
            session (Optional[httpx.AsyncClient]): HTTP client session to use
            debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging

        Returns:
            ResponseGetData: Response from the OTP elevation request
        """
        # Create session if not provided
        if session is None:
            async with httpx.AsyncClient() as client_session:
                from ..routes import auth as auth_routes

                return await auth_routes.elevate_user_otp(
                    auth=self,
                    debug_api=debug_api,
                    session=client_session,
                    one_time_password=one_time_password,
                    debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                )
        else:
            from ..routes import auth as auth_routes

            return await auth_routes.elevate_user_otp(
                auth=self,
                debug_api=debug_api,
                session=session,
                one_time_password=one_time_password,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            )

    @abstractmethod
    async def get_auth_token(
        self,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        **kwargs,
    ) -> Union[str, ResponseGetData]:
        """Retrieve or generate an authentication token.

        This abstract method must be implemented by subclasses to handle
        the specific authentication flow for each authentication type.

        Args:
            session (Optional[httpx.AsyncClient]): HTTP client session to use
            debug_api (bool): Whether to enable API debugging
            debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
            **kwargs: Additional keyword arguments specific to the authentication type

        Returns:
            Union[str, ResponseGetData]: The authentication token or raw response data

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement get_auth_token method.")

    async def print_is_token(
        self,
        debug_api: bool = False,
        token_name: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
    ) -> bool:
        """Print token status and return True if token is valid, otherwise False.

        This method performs a complete authentication check including token
        retrieval and validation, then prints a user-friendly status message.

        Args:
            debug_api (bool): Whether to enable API debugging
            token_name (Optional[str]): Override token name for display purposes
            session (Optional[httpx.AsyncClient]): HTTP client session to use

        Returns:
            bool: True if token is valid, False otherwise
        """
        self.token_name = token_name or self.token_name

        if not self.token:
            await self.get_auth_token(debug_api=debug_api, session=session)

        if not self.is_valid_token:
            await self.who_am_i(session=session, debug_api=debug_api)

        if not self.is_valid_token:
            print(
                f"🚧 failed to retrieve {self.token_name} token from {self.domo_instance}"
            )
            return False

        print(f"🎉 {self.token_name} token retrieved from {self.domo_instance} ⚙️")
        return True


@dataclass
class DomoAuth(_DomoAuth_Optional, _DomoAuth_Required):
    """Concrete combined DomoAuth base class.

    This is a concrete implementation that combines the required and optional
    authentication functionality. It serves as a base class for specific
    authentication types.
    """


class _DomoFullAuth_Required(_DomoAuth_Required, _DomoAuth_Optional):
    """Mixin for required parameters for DomoFullAuth.

    This class provides full authentication functionality using username and password
    credentials to obtain session tokens from Domo's product APIs.

    Attributes:
        domo_username (str): Domo username for authentication
        domo_password (str): Domo password for authentication
    """

    def __init__(
        self,
        domo_username: str,
        domo_password: str,
        domo_instance: str,
        token_name: Optional[str] = None,
        token: Optional[str] = None,
        user_id: Optional[str] = None,
        is_valid_token: bool = False,
    ):
        """Initialize full authentication with username and password.

        Args:
            domo_username (str): Domo username for authentication
            domo_password (str): Domo password for authentication
            domo_instance (str): The Domo instance identifier
            token_name (Optional[str]): Name identifier for the token
            token (Optional[str]): Pre-existing authentication token
            user_id (Optional[str]): The authenticated user's ID
            is_valid_token (bool): Whether the current token is valid

        Raises:
            InvalidCredentialsError: If username or password is empty
            InvalidInstanceError: If domo_instance is empty
        """
        if not domo_username:
            raise AuthError(message="Domo username is required.")
        if not domo_password:
            raise AuthError(message="Domo password is required.")

        if not domo_instance:
            raise AuthError(message="Domo instance is required.")

        self.domo_username = domo_username
        self.domo_password = domo_password

        # Initialize base classes
        _DomoAuth_Required.__init__(self, domo_instance)
        _DomoAuth_Optional.__init__(
            self, domo_instance, token_name, token, user_id, is_valid_token
        )

    @property
    def auth_header(self) -> dict:
        """Generate the full authentication header specific to product APIs.

        Returns:
            dict: HTTP headers with 'x-domo-authentication' token, or empty dict if no token
        """
        return {"x-domo-authentication": self.token} if self.token else {}

    async def get_auth_token(
        self,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        return_raw: bool = False,
        **kwargs,
    ) -> Union[str, ResponseGetData]:
        """Retrieve the authentication token from product APIs using the provided credentials.

        This method authenticates with Domo using username and password to obtain
        a session token that can be used for subsequent API calls.

        Args:
            session (Optional[httpx.AsyncClient]): HTTP client session to use
            debug_api (bool): Whether to enable API debugging
            debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
            return_raw (bool): Whether to return raw ResponseGetData instead of token string
            **kwargs: Additional keyword arguments

        Returns:
            Union[str, ResponseGetData]: Authentication token string or raw response data

        Raises:
            InvalidCredentialsError: If authentication fails or no token is returned
        """
        from ..routes import auth as auth_routes

        res = await auth_routes.get_full_auth(
            auth=None,
            domo_instance=self.domo_instance,
            domo_username=self.domo_username,
            domo_password=self.domo_password,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        if res.is_success and res.response:
            self.is_valid_token = True

            token = str(res.response.get("sessionToken", ""))
            self.token = token
            self.token_name = self.token_name or "full_auth"

        if not self.token:
            raise AuthError(message="Failed to retrieve authentication token")

        return self.token


@dataclass
class DomoFullAuth(
    _DomoFullAuth_Required,
):
    """Full authentication using Domo username and password.

    This class provides authentication using Domo credentials (username and password)
    to obtain session tokens. It's typically used for direct user authentication
    where username/password login is permitted.

    Attributes:
        domo_instance (str): The Domo instance identifier
        domo_username (str): Domo username for authentication
        domo_password (str): Domo password for authentication (not shown in repr)
        token_name (Optional[str]): Name identifier for the token
        token (Optional[str]): The authentication token (not shown in repr)
        user_id (Optional[str]): The authenticated user's ID
        is_valid_token (bool): Whether the current token is valid

    Example:
        >>> auth = DomoFullAuth(
        ...     domo_instance="mycompany",
        ...     domo_username="user@company.com",
        ...     domo_password="secure_password"
        ... )
        >>> token = await auth.get_auth_token()
    """

    domo_instance: str
    domo_username: str
    domo_password: str = field(repr=False)
    token_name: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    user_id: Optional[str] = None
    is_valid_token: bool = False

    def __post_init__(self):
        """Initialize the authentication mixins after dataclass creation."""
        # Initialize mixins explicitly with proper arguments
        _DomoFullAuth_Required.__init__(
            self,
            domo_username=self.domo_username,
            domo_password=self.domo_password,
            domo_instance=self.domo_instance,
            token_name=self.token_name,
            token=self.token,
            user_id=self.user_id,
            is_valid_token=self.is_valid_token,
        )


def test_is_full_auth(
    auth,
    function_name=None,
    num_stacks_to_drop=1,  # pass q for route pass 2 for class
):
    """Test that the provided object is a DomoFullAuth instance.

    This validation function ensures that the authentication object is of the
    correct type for functions that specifically require full authentication.

    Args:
        auth: The authentication object to validate
        function_name (Optional[str]): Override function name for error reporting
        num_stacks_to_drop (int): Number of stack frames to drop for debugging

    Raises:
        InvalidAuthTypeError: If auth is not a DomoFullAuth instance
    """
    # TODO: Re-implement traceback functionality
    function_name = function_name or "test_is_full_auth"

    if auth.__class__.__name__ != "DomoFullAuth":
        raise AuthError(
            message=f"{function_name} requires DomoFullAuth authentication."
        )


class _DomoTokenAuth_Required(_DomoAuth_Required, _DomoAuth_Optional):
    """Mixin for required parameters for DomoTokenAuth.

    This class provides token-based authentication functionality using pre-generated
    access tokens from Domo's admin panel. This is useful in environments where
    direct username/password authentication is not permitted.

    Attributes:
        domo_access_token (str): Pre-generated access token from Domo admin panel
    """

    def __init__(
        self,
        domo_access_token: str,
        domo_instance: str,
        token_name: Optional[str] = None,
        token: Optional[str] = None,
        user_id: Optional[str] = None,
        is_valid_token: bool = False,
    ):
        """Initialize token authentication with pre-generated access token.

        Args:
            domo_access_token (str): Pre-generated access token from Domo admin panel
            domo_instance (str): The Domo instance identifier
            token_name (Optional[str]): Name identifier for the token
            token (Optional[str]): The authentication token (will be set to access token)
            user_id (Optional[str]): The authenticated user's ID
            is_valid_token (bool): Whether the current token is valid

        Raises:
            InvalidCredentialsError: If domo_access_token is empty
        """
        if not domo_access_token:
            raise AuthError(message="Domo access token is required.")
        self.domo_access_token = domo_access_token

        # Initialize base classes
        _DomoAuth_Required.__init__(self, domo_instance)
        _DomoAuth_Optional.__init__(
            self, domo_instance, token_name, token, user_id, is_valid_token
        )

    @property
    def auth_header(self) -> dict:
        """Generate the authentication header for access token based authentication.

        Returns:
            dict: HTTP headers with 'x-domo-developer-token' containing the access token
        """
        return {"x-domo-developer-token": self.token or self.domo_access_token}

    async def get_auth_token(
        self,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        token_name: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Retrieve the access token, updating internal attributes as necessary.

        For token authentication, this method validates the token by calling who_am_i
        if no user_id is set, then returns the access token.

        Args:
            session (Optional[httpx.AsyncClient]): HTTP client session to use
            debug_api (bool): Whether to enable API debugging
            debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
            token_name (Optional[str]): Override token name for display purposes
            **kwargs: Additional keyword arguments

        Returns:
            str: The access token
        """

        if not self.user_id:
            await self.who_am_i(
                session=session,
                debug_api=debug_api,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            )

        self.token = self.domo_access_token
        self.is_valid_token = True

        if token_name:
            self.token_name = token_name

        return self.token


@dataclass
class DomoTokenAuth(_DomoTokenAuth_Required):
    """Token-based authentication using pre-generated access tokens.

    This authentication method uses access tokens generated from Domo's admin panel
    (Admin > Access Tokens). This is particularly useful in environments where
    direct username/password authentication is not permitted or for automated systems.

    Attributes:
        domo_access_token (str): Pre-generated access token (not shown in repr)
        domo_instance (str): The Domo instance identifier
        token_name (Optional[str]): Name identifier for the token
        token (Optional[str]): The authentication token (not shown in repr)
        user_id (Optional[str]): The authenticated user's ID
        is_valid_token (bool): Whether the current token is valid

    Example:
        >>> auth = DomoTokenAuth(
        ...     domo_access_token="your-access-token-here",
        ...     domo_instance="mycompany"
        ... )
        >>> token = await auth.get_auth_token()
    """

    domo_access_token: str = field(repr=False)
    domo_instance: str

    token_name: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    user_id: Optional[str] = None
    is_valid_token: bool = False

    def __post_init__(self):
        """Initialize the authentication after dataclass creation."""
        self.token = self.domo_access_token

        if not self.token:
            raise AuthError(message="Domo access token is required.")

        _DomoTokenAuth_Required.__init__(
            self,
            domo_access_token=self.domo_access_token,
            domo_instance=self.domo_instance,
            token_name=self.token_name,
            token=self.token,
            user_id=self.user_id,
            is_valid_token=self.is_valid_token,
        )


@dataclass
class DomoDeveloperAuth(_DomoAuth_Optional, _DomoAuth_Required):
    """Developer authentication using client credentials.

    This authentication method uses OAuth2 client credentials (client ID and secret)
    to obtain bearer tokens. This is typically used for applications built on
    Domo's developer platform and requires developer app registration.

    Attributes:
        domo_client_id (str): OAuth2 client ID from developer app registration
        domo_client_secret (str): OAuth2 client secret (not shown in repr)
        domo_instance (str): The Domo instance identifier
        token_name (Optional[str]): Name identifier for the token
        token (Optional[str]): The bearer token (not shown in repr)
        user_id (Optional[str]): The authenticated user's ID
        is_valid_token (bool): Whether the current token is valid

    Example:
        >>> auth = DomoDeveloperAuth(
        ...     domo_client_id="your-client-id",
        ...     domo_client_secret="your-client-secret",
        ...     domo_instance="mycompany"
        ... )
        >>> token = await auth.get_auth_token()
    """

    domo_client_id: str
    domo_client_secret: str = field(repr=False)
    domo_instance: str

    token_name: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    user_id: Optional[str] = None
    is_valid_token: bool = False

    def __post_init__(self):
        """Initialize the authentication after dataclass creation."""
        # Initialize base classes
        _DomoAuth_Optional.__init__(
            self,
            domo_instance=self.domo_instance,
            token_name=self.token_name,
            token=self.token,
            user_id=self.user_id,
            is_valid_token=self.is_valid_token,
        )
        _DomoAuth_Required.__init__(self, domo_instance=self.domo_instance)

    @property
    def auth_header(self) -> dict:
        """Generate the authentication header for developer token authentication.

        Returns:
            dict: HTTP headers with 'Authorization' bearer token, or empty dict if no token
        """
        if self.token:
            return {"Authorization": f"bearer {self.token}"}
        return {}

    async def get_auth_token(
        self,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        **kwargs,
    ) -> str:
        """Retrieve the developer token using client credentials and update internal attributes.

        This method uses OAuth2 client credentials flow to obtain a bearer token
        from Domo's developer authentication endpoint.

        Args:
            session (Optional[httpx.AsyncClient]): HTTP client session to use
            debug_api (bool): Whether to enable API debugging
            debug_num_stacks_to_drop (int): Number of stack frames to drop for debugging
            **kwargs: Additional keyword arguments

        Returns:
            str: The bearer token for API authentication

        Raises:
            InvalidCredentialsError: If authentication fails or no token is returned
        """

        from ..routes import auth as auth_routes

        res = await auth_routes.get_developer_auth(
            auth=None,
            domo_client_id=self.domo_client_id,
            domo_client_secret=self.domo_client_secret,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        if isinstance(res, ResponseGetData) and res.is_success and res.response:
            self.is_valid_token = True
            self.token = str(res.response.get("access_token", ""))
            self.user_id = res.response.get("userId")
            self.domo_instance = res.response.get("domain", self.domo_instance)
            self.token_name = self.token_name or "developer_auth"
            return self.token

        raise AuthError(message="Failed to retrieve developer token")


class _DomoJupyter_Required:
    """Required parameters and setup for Domo Jupyter authentication.

    This class provides the foundational authentication components needed for
    Domo Jupyter environments, including token validation and environment setup.

    Attributes:
        jupyter_token (str): Authorization token from Domo Jupyter network traffic
        service_location (str): Service location from Domo Jupyter environment
        service_prefix (str): Service prefix from Domo Jupyter environment
    """

    def __init__(
        self,
        jupyter_token: Optional[str] = None,
        service_location: Optional[str] = None,
        service_prefix: Optional[str] = None,
    ):
        """Initialize Jupyter authentication parameters.

        If parameters are not provided, the user will be prompted to enter them
        interactively. These values are typically obtained by monitoring Domo
        Jupyter network traffic.

        Args:
            jupyter_token (Optional[str]): Authorization token from network traffic
            service_location (Optional[str]): Service location from environment
            service_prefix (Optional[str]): Service prefix from environment

        Raises:
            ValueError: If any required parameters are missing after initialization
        """

        # Initialize fields, prompting if not provided
        self.jupyter_token = jupyter_token or input(
            "jupyter token: # retrieve this by monitoring Domo Jupyter network traffic. It is the Authorization header\n> "
        )
        self.service_location = service_location or input(
            "service_location: # retrieve from Domo Jupyter environment\n> "
        )
        self.service_prefix = service_prefix or input(
            "service_prefix: # retrieve from Domo Jupyter environment\n> "
        )

        self._test_prereq()

    # --- Methods ---
    def get_jupyter_token_flow(self):
        """Stub method for initiating a Jupyter token retrieval flow.

        This method is a placeholder for future implementation of automated
        Jupyter token retrieval.
        """
        print("hello world, I am a jupyter_token")

    def _test_prereq(self):
        """Validate that required attributes are present.

        Raises:
            ValueError: If any required Jupyter parameters are missing
        """
        missing = []
        if not self.jupyter_token:
            missing.append("jupyter_token")
        if not self.service_location:
            missing.append("service_location")
        if not self.service_prefix:
            missing.append("service_prefix")

        if missing:
            raise ValueError(f"DomoJupyterAuth objects must have: {', '.join(missing)}")


@dataclass
class DomoJupyterAuth(_DomoAuth_Optional, _DomoJupyter_Required, _DomoAuth_Required):
    """Base class for Domo Jupyter authentication.

    This class combines the core authentication functionality with Jupyter-specific
    requirements. It serves as a foundation for specific Jupyter authentication types.
    """


@dataclass
class DomoJupyterFullAuth(
    _DomoJupyter_Required,
    _DomoFullAuth_Required,
):
    """Jupyter authentication using full credentials (username/password).

    This class combines full Domo authentication with Jupyter environment support.
    It's used when working within Domo Jupyter environments and requires both
    standard Domo credentials and Jupyter-specific authentication tokens.

    Attributes:
        jupyter_token (str): Authorization token from Domo Jupyter (not shown in repr)
        service_location (str): Service location from Jupyter environment
        service_prefix (str): Service prefix from Jupyter environment
        domo_instance (str): The Domo instance identifier
        domo_username (str): Domo username for authentication
        domo_password (str): Domo password for authentication (not shown in repr)
        token_name (Optional[str]): Name identifier for the token
        token (Optional[str]): The authentication token (not shown in repr)
        user_id (Optional[str]): The authenticated user's ID
        is_valid_token (bool): Whether the current token is valid

    Example:
        >>> auth = DomoJupyterFullAuth(
        ...     jupyter_token="jupyter-auth-token",
        ...     service_location="service-location",
        ...     service_prefix="service-prefix",
        ...     domo_instance="mycompany",
        ...     domo_username="user@company.com",
        ...     domo_password="secure_password"
        ... )
    """

    jupyter_token: str = field(repr=False)
    service_location: str
    service_prefix: str

    domo_instance: str
    domo_username: str
    domo_password: str = field(repr=False)

    token_name: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    user_id: Optional[str] = None
    is_valid_token: bool = False

    def __post_init__(self):
        """Initialize the Jupyter and full authentication mixins."""
        # Initialize mixins explicitly
        _DomoJupyter_Required.__init__(
            self,
            jupyter_token=self.jupyter_token,
            service_location=self.service_location,
            service_prefix=self.service_prefix,
        )
        _DomoFullAuth_Required.__init__(
            self,
            domo_username=self.domo_username,
            domo_password=self.domo_password,
            domo_instance=self.domo_instance,
            token_name=self.token_name,
            token=self.token,
            user_id=self.user_id,
            is_valid_token=self.is_valid_token,
        )

    @property
    def auth_header(self) -> dict:
        """Generate authentication headers combining Domo and Jupyter tokens.

        Returns:
            dict: Combined authentication headers for both Domo and Jupyter APIs
        """
        return {
            **super().auth_header,
            "authorization": f"Token {self.jupyter_token}",
        }

    @classmethod
    def convert_auth(
        cls, auth: DomoFullAuth, jupyter_token, service_location, service_prefix
    ):
        """Convert DomoFullAuth to DomoJupyterFullAuth.

        This factory method creates a Jupyter-enabled authentication object from
        an existing full authentication object by adding the necessary Jupyter
        environment parameters.

        Args:
            auth (DomoFullAuth): Existing full authentication object
            jupyter_token (str): Authorization token from Domo Jupyter
            service_location (str): Service location from Jupyter environment
            service_prefix (str): Service prefix from Jupyter environment

        Returns:
            DomoJupyterFullAuth: New Jupyter-enabled authentication object
        """
        return cls(
            domo_instance=auth.domo_instance,
            domo_username=auth.domo_username,
            domo_password=auth.domo_password,
            jupyter_token=jupyter_token,
            service_location=service_location,
            service_prefix=service_prefix,
            token_name=auth.token_name,
            token=auth.token,
            user_id=auth.user_id,
            is_valid_token=auth.is_valid_token,
        )


@dataclass
class DomoJupyterTokenAuth(
    _DomoJupyter_Required,
    _DomoTokenAuth_Required,
):
    """Jupyter authentication using access tokens.

    This class combines token-based Domo authentication with Jupyter environment support.
    It's used when working within Domo Jupyter environments with pre-generated access
    tokens instead of username/password credentials.

    Attributes:
        jupyter_token (str): Authorization token from Domo Jupyter (not shown in repr)
        service_location (str): Service location from Jupyter environment
        service_prefix (str): Service prefix from Jupyter environment
        domo_instance (str): The Domo instance identifier
        domo_access_token (str): Pre-generated access token (not shown in repr)
        token_name (Optional[str]): Name identifier for the token
        token (Optional[str]): The authentication token (not shown in repr)
        user_id (Optional[str]): The authenticated user's ID
        is_valid_token (bool): Whether the current token is valid

    Example:
        >>> auth = DomoJupyterTokenAuth(
        ...     jupyter_token="jupyter-auth-token",
        ...     service_location="service-location",
        ...     service_prefix="service-prefix",
        ...     domo_instance="mycompany",
        ...     domo_access_token="your-access-token"
        ... )
    """

    jupyter_token: str = field(repr=False)
    service_location: str
    service_prefix: str

    domo_instance: str

    domo_access_token: str = field(repr=False)

    token_name: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    user_id: Optional[str] = None
    is_valid_token: bool = False

    def __post_init__(self):
        """Initialize the Jupyter and token authentication mixins."""
        _DomoJupyter_Required.__init__(
            self,
            jupyter_token=self.jupyter_token,
            service_location=self.service_location,
            service_prefix=self.service_prefix,
        )
        _DomoTokenAuth_Required.__init__(
            self,
            domo_access_token=self.domo_access_token,
            domo_instance=self.domo_instance,
            token_name=self.token_name,
            token=self.token,
            user_id=self.user_id,
            is_valid_token=self.is_valid_token,
        )

    @property
    def auth_header(self) -> dict:
        """Generate authentication headers combining Domo and Jupyter tokens.

        Returns:
            dict: Combined authentication headers for both Domo and Jupyter APIs
        """
        return {
            **super().auth_header,
            "authorization": f"Token {self.jupyter_token}",
        }

    @classmethod
    def convert_auth(
        cls, auth: DomoTokenAuth, jupyter_token, service_location, service_prefix
    ):
        """Convert DomoTokenAuth to DomoJupyterTokenAuth.

        This factory method creates a Jupyter-enabled authentication object from
        an existing token authentication object by adding the necessary Jupyter
        environment parameters.

        Args:
            auth (DomoTokenAuth): Existing token authentication object
            jupyter_token (str): Authorization token from Domo Jupyter
            service_location (str): Service location from Jupyter environment
            service_prefix (str): Service prefix from Jupyter environment

        Returns:
            DomoJupyterTokenAuth: New Jupyter-enabled authentication object
        """
        return cls(
            domo_instance=auth.domo_instance,
            domo_access_token=auth.domo_access_token,
            jupyter_token=jupyter_token,
            service_location=service_location,
            service_prefix=service_prefix,
            token_name=auth.token_name,
            token=auth.token,
            user_id=auth.user_id,
            is_valid_token=auth.is_valid_token,
        )


def test_is_jupyter_auth(
    auth: DomoJupyterAuth,
    required_auth_type_ls: Optional[list] = None,
):
    """Test that the provided object is a valid Jupyter authentication instance.

    This validation function ensures that the authentication object is one of the
    accepted Jupyter authentication types for functions that specifically require
    Jupyter authentication capabilities.

    Args:
        auth (DomoJupyterAuth): The authentication object to validate
        required_auth_type_ls (Optional[list]): List of acceptable auth types.
            Defaults to [DomoJupyterFullAuth, DomoJupyterTokenAuth]

    Raises:
        InvalidAuthTypeError: If auth is not one of the required Jupyter auth types
    """
    if required_auth_type_ls is None:
        required_auth_type_ls = [DomoJupyterFullAuth, DomoJupyterTokenAuth]

    # TODO: Re-implement traceback functionality

    if auth.__class__.__name__ not in [
        auth_type.__name__ for auth_type in required_auth_type_ls
    ]:
        raise AuthError(
            message=f"test_is_jupyter_auth requires {[auth_type.__name__ for auth_type in required_auth_type_ls]} authentication, got {auth.__class__.__name__}",
            function_name="test_is_jupyter_auth",
            domo_instance=auth.domo_instance,
        )
