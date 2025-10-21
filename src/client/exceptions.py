"""Modern Domo Exception classes with improved structure and usability"""

__all__ = ["DomoError", "RouteError", "ClassError", "AuthError"]

from dataclasses import dataclass
from typing import Any, Optional, Union


class _DomoError(Exception):
    """Base exception for all Domo-related errors with exception chaining support."""

    def __init__(
        self,
        message: str = "An error occurred",
        entity_id: Optional[str] = None,
        entity_name: Optional[str] = None,
        function_name: Optional[str] = None,
        parent_class: Optional[str] = None,
        status: Optional[int] = None,
        domo_instance: Optional[str] = None,
        is_warning: bool = False,
        exception: Optional[Exception] = None,
    ):
        """Initialize with custom message and optional original exception.

        Args:
            message: Custom error message
            exception: The original exception that caused this error
        """
        self.message = message
        self.entity_id = entity_id
        self.entity_name = entity_name
        self.function_name = function_name
        self.parent_class = parent_class
        self.status = status
        self.domo_instance = domo_instance
        self.is_warning = is_warning
        self.exception = exception

        # Use exception chaining if we have an original exception
        if exception:
            # This preserves the full traceback chain
            super().__init__(
                f"{self._generate_default_message} (caused by: {type(exception).__name__}: {exception})"
            )
            # Explicitly set the cause for proper exception chaining
            self.__cause__ = exception
        else:
            super().__init__(self._generate_default_message)

    @property
    def prefix_txt(self) -> str:
        return "⚠️" if self.is_warning else "🛑"

    @property
    def status_txt(self) -> Union[str, None]:
        if not self.status:
            return None

        if self.status == 404:
            return f"Resource not found (HTTP {self.status})"
        elif self.status == 401:
            return f"Authentication required (HTTP {self.status})"
        elif self.status == 403:
            return f"Access forbidden (HTTP {self.status})"
        elif self.status >= 500:
            return f"Server error (HTTP {self.status})"
        elif self.status >= 400:
            return f"Client error (HTTP {self.status})"

        return f"Request failed (HTTP {self.status})"

    @property
    def function_txt(self) -> Union[str, None]:
        if not self.parent_class and not self.function_name:
            return None

        return "in " + ".".join(
            [ele for ele in [self.parent_class, self.function_name] if ele]
        )

    @property
    def entity_str(self) -> Union[str, None]:
        if not self.entity_id and not self.entity_str:
            return None

        return f"entity: { ' - '.join([ele for ele in [self.entity_id, self.entity_name] if ele])}"

    @property
    def instance_str(self) -> Union[str, None]:
        if not self.domo_instance:
            return None

        return f"in: {self.domo_instance}"

    @property
    def _generate_default_message(self) -> str:
        """Generate a default message based on available context."""

        parts = [
            ele
            for ele in [
                self.prefix_txt,
                self.function_txt,
                self.entity_str,
                self.message,
                self.status_txt,
                self.instance_str,
            ]
            if ele
        ]

        return "|".join(parts) if parts else "An error occurred"


@dataclass
class DomoError(_DomoError):
    """Base exception for all Domo-related errors.

    This exception stores all relevant context as attributes and provides
    a clean string representation for logging and debugging.

    """

    message: str = "An error occurred"
    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    function_name: Optional[str] = None
    parent_class: Optional[str] = None
    status: Optional[int] = None
    domo_instance: Optional[str] = None
    is_warning: bool = False
    exception: Optional[Exception] = None

    def __post_init__(self):
        super().__init__(
            message=self.message,
            entity_id=self.entity_id,
            entity_name=self.entity_name,
            function_name=self.function_name,
            parent_class=self.parent_class,
            status=self.status,
            domo_instance=self.domo_instance,
            is_warning=self.is_warning,
            exception=self.exception,
        )


@dataclass
class RouteError(_DomoError):
    """Exception for API route/endpoint errors."""

    res: Any  # Should be ResponseGetData but avoiding circular import
    message: Optional[str] = None
    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    function_name: Optional[str] = None
    is_warning: bool = False

    def __post_init__(self):
        """Extract route-specific information from response."""

        super().__init__(
            is_warning=self.is_warning,
            message=self.message or "API request failed",
            entity_id=self.entity_id,
            entity_name=self.entity_name,
            parent_class=getattr(self.res, "parent_class", None),
            function_name=self.function_name,
            status=getattr(self.res, "status", None),
            domo_instance=getattr(
                getattr(self.res, "auth", None), "domo_instance", None
            ),
        )


@dataclass
class AuthError(_DomoError):
    """Exception for authentication-related errors."""

    message: str = "An error occurred"
    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    function_name: Optional[str] = None
    parent_class: Optional[str] = None
    status: Optional[int] = None
    domo_instance: Optional[str] = None
    is_warning: bool = False
    exception: Optional[Exception] = None

    def __post_init__(self):
        super().__init__(
            message=self.message,
            entity_id=self.entity_id,
            entity_name=self.entity_name,
            function_name=self.function_name,
            parent_class=self.parent_class,
            status=self.status,
            domo_instance=self.domo_instance,
            is_warning=self.is_warning,
            exception=self.exception,
        )


@dataclass
class ClassError(_DomoError):
    """Exception for class-specific errors."""

    cls: Any = None
    cls_instance: Any = None

    message: str = "An error occurred"

    entity_name: Optional[str] = None
    entity_id_col: Optional[str] = "id"
    function_name: Optional[str] = None
    parent_class: Optional[str] = None
    status: Optional[int] = None
    domo_instance: Optional[str] = None
    is_warning: bool = False
    exception: Optional[Exception] = None

    @property
    def entity_id_str(self) -> Union[str, None]:
        if not self.entity_id_col or not self.cls_instance:
            return None

        return getattr(self.cls_instance, self.entity_id_col, None)

    @property
    def parent_class_str(self) -> Union[str, None]:
        if self.cls_instance:
            return self.cls_instance.__class__.__name__

        if self.cls:
            return self.cls.__name__

    def __post_init__(self):
        """Extract class-specific information."""

        super().__init__(
            is_warning=self.is_warning,
            message=self.message,
            entity_id=self.entity_id_str,
            entity_name=self.entity_name,
            parent_class=self.parent_class_str,
            function_name=self.function_name,
            status=self.status,
            domo_instance=self.domo_instance,
        )
