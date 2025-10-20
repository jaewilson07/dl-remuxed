"""Modern Domo Exception classes with improved structure and usability"""

__all__ = ["DomoError", "RouteError", "ClassError", "AuthError"]

from dataclasses import dataclass, field
from typing import Any, Optional, List, Union


@dataclass
class DomoError(Exception):
    """Base exception for all Domo-related errors.

    This exception stores all relevant context as attributes and provides
    a clean string representation for logging and debugging.

    Attributes:
        message: Human-readable error message
        entity_id: ID of the entity that caused the error (dataset, card, etc.)
        function_name: Name of the function where the error occurred
        parent_class: Name of the class where the error occurred
        status: HTTP status code if applicable
        domo_instance: Domo instance URL where the error occurred
        is_warning: Whether this is a warning (⚠️) vs error (🛑)
        response_data: Full response object for debugging
        additional_context: Any additional context data

    Examples:
        >>> error = DomoError(
        ...     message="Dataset not found",
        ...     entity_id="abc123",
        ...     status=404,
        ...     domo_instance="mycompany"
        ... )
        >>> print(error)
        🛑 DomoError: Dataset not found [entity: abc123 | status: 404 | instance: mycompany]
    """

    message: str = "An error occurred"
    entity_id: Optional[str] = None
    function_name: Optional[str] = None
    parent_class: Optional[str] = None
    status: Optional[int] = None
    domo_instance: Optional[str] = None
    is_warning: bool = False
    response_data: Any = field(default=None, repr=False)
    additional_context: dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        """Extract additional context from response_data if available."""
        if self.response_data:
            # Extract from response object if not explicitly set
            if not self.status and hasattr(self.response_data, "status"):
                self.status = self.response_data.status

            if not self.domo_instance and hasattr(self.response_data, "auth"):
                auth = getattr(self.response_data, "auth", None)
                if auth and hasattr(auth, "domo_instance"):
                    self.domo_instance = auth.domo_instance

            # Extract from traceback_details if available
            traceback_details = getattr(self.response_data, "traceback_details", None)
            if traceback_details:
                if not self.function_name and hasattr(
                    traceback_details, "function_name"
                ):
                    self.function_name = traceback_details.function_name
                if not self.parent_class and hasattr(traceback_details, "parent_class"):
                    self.parent_class = traceback_details.parent_class

        # Ensure we have a meaningful message
        if not self.message or self.message == "An error occurred":
            self.message = self._generate_default_message()

        # Call parent's __init__ with formatted message
        super().__init__(str(self))

    def _generate_default_message(self) -> str:
        """Generate a default message based on available context."""
        if self.status:
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
            else:
                return f"Request failed (HTTP {self.status})"

        if self.function_name:
            return f"Operation failed in {self.function_name}"

        return "An error occurred"

    def __str__(self) -> str:
        """Generate a formatted error message."""
        prefix = "⚠️" if self.is_warning else "🛑"

        # Build location context
        location_parts = []
        if self.parent_class:
            location_parts.append(self.parent_class)
        if self.function_name:
            location_parts.append(self.function_name)
        location_str = ".".join(location_parts)

        # Build context parts
        context_parts = []
        if location_str:
            context_parts.append(f"in {location_str}")
        if self.entity_id:
            context_parts.append(f"entity: {self.entity_id}")
        if self.status:
            context_parts.append(f"status: {self.status}")
        if self.domo_instance:
            context_parts.append(f"instance: {self.domo_instance}")

        context_str = " | ".join(context_parts)

        if context_str:
            return f"{prefix} {self.__class__.__name__}: {self.message} [{context_str}]"
        else:
            return f"{prefix} {self.__class__.__name__}: {self.message}"

    @classmethod
    def from_response(
        cls, response_data: Any, message: str = "API request failed", **kwargs
    ) -> "DomoError":
        """Create a DomoError from a response object.

        Args:
            response_data: Response object containing error details
            message: Custom error message (optional)
            **kwargs: Additional parameters for the exception

        Returns:
            DomoError instance with extracted context

        Examples:
            >>> error = DomoError.from_response(response, "Dataset creation failed")
            >>> error = DomoError.from_response(response, entity_id="abc123")
        """
        return cls(message=message, response_data=response_data, **kwargs)

    @classmethod
    def for_entity(
        cls, entity_id: str, message: str, entity_type: str = "resource", **kwargs
    ) -> "DomoError":
        """Create a DomoError for a specific entity.

        Args:
            entity_id: ID of the entity that caused the error
            message: Error message
            entity_type: Type of entity (dataset, card, user, etc.)
            **kwargs: Additional parameters

        Returns:
            DomoError instance with entity context

        Examples:
            >>> error = DomoError.for_entity("abc123", "Dataset not found", "dataset")
        """
        if "{entity_id}" in message:
            message = message.format(entity_id=entity_id)
        elif "{entity_type}" in message:
            message = message.format(entity_type=entity_type, entity_id=entity_id)

        return cls(message=message, entity_id=entity_id, **kwargs)


@dataclass
class RouteError(DomoError):
    """Exception for API route/endpoint errors.

    This exception is typically raised when API calls fail or return
    unexpected responses. It automatically extracts relevant information
    from the response object.

    Examples:
        >>> # Basic route error
        >>> error = RouteError(message="API call failed", status=404)

        >>> # From response object
        >>> error = RouteError.from_response(response, "Dataset retrieval failed")

        >>> # With entity context
        >>> error = RouteError.for_entity("abc123", "Dataset {entity_id} not found")
    """

    def __post_init__(self):
        """Extract route-specific information from response."""
        if self.response_data:
            # Build enhanced message from response
            message_parts = (
                [self.message] if self.message != "An error occurred" else []
            )

            if hasattr(self.response_data, "response"):
                response_content = getattr(self.response_data, "response", "")
                if response_content and str(response_content) not in str(self.message):
                    message_parts.append(f"API Response: {response_content}")

            if hasattr(self.response_data, "url"):
                url = getattr(self.response_data, "url", "")
                if url:
                    message_parts.append(f"URL: {url}")

            if hasattr(self.response_data, "body"):
                body = getattr(self.response_data, "body", "")
                if body:
                    self.additional_context["request_body"] = str(body)

            if message_parts:
                self.message = " | ".join(message_parts)

        super().__post_init__()


@dataclass
class AuthError(RouteError):
    """Exception for authentication-related errors.

    This exception is used for all authentication failures including
    invalid credentials, expired tokens, insufficient permissions, etc.
    It provides enhanced context for auth-specific debugging.

    Attributes:
        auth_type: Type of authentication that failed (FullAuth, DeveloperAuth, etc.)
        required_auth_types: List of auth types required for the operation
        auth_instance: The auth object that failed (optional)

    Examples:
        >>> # Basic auth error
        >>> error = AuthError(message="Invalid credentials")

        >>> # With auth type context
        >>> error = AuthError(
        ...     message="This API requires DeveloperAuth",
        ...     auth_type="FullAuth",
        ...     required_auth_types=["DeveloperAuth"]
        ... )

        >>> # From auth validation
        >>> error = AuthError.for_invalid_credentials("mycompany", "Invalid password")
    """

    auth_type: Optional[str] = None
    required_auth_types: Optional[List[str]] = None
    auth_instance: Any = field(default=None, repr=False)

    def __post_init__(self):
        """Extract auth-specific information."""
        # Extract auth type from auth_instance if available
        if self.auth_instance and not self.auth_type:
            if hasattr(self.auth_instance, "__class__"):
                self.auth_type = self.auth_instance.__class__.__name__

        # Build auth-specific message context
        if self.required_auth_types and self.auth_type:
            auth_context = (
                f"requires {'/'.join(self.required_auth_types)}, got {self.auth_type}"
            )
            if "requires" not in self.message.lower():
                self.message = f"{self.message} (operation {auth_context})"

        # Store auth info in additional context
        if self.auth_type:
            self.additional_context["auth_type"] = self.auth_type
        if self.required_auth_types:
            self.additional_context["required_auth_types"] = self.required_auth_types

        super().__post_init__()

    @classmethod
    def for_invalid_credentials(
        cls,
        domo_instance: Optional[str] = None,
        message: str = "Invalid credentials provided",
        **kwargs,
    ) -> "AuthError":
        """Create an AuthError for invalid credentials.

        Args:
            domo_instance: Domo instance where auth failed
            message: Custom error message
            **kwargs: Additional parameters

        Returns:
            AuthError instance for credential failures
        """
        return cls(message=message, domo_instance=domo_instance, status=401, **kwargs)

    @classmethod
    def for_invalid_auth_type(
        cls,
        required_auth_types: Union[str, List[str]],
        current_auth_type: Optional[str] = None,
        **kwargs,
    ) -> "AuthError":
        """Create an AuthError for wrong authentication type.

        Args:
            required_auth_types: Required auth type(s) for the operation
            current_auth_type: Auth type that was provided
            **kwargs: Additional parameters

        Returns:
            AuthError instance for auth type mismatches
        """
        if isinstance(required_auth_types, str):
            required_auth_types = [required_auth_types]

        auth_list = ", ".join(required_auth_types)
        message = f"This API requires: {auth_list}"
        if current_auth_type:
            message += f" (provided: {current_auth_type})"

        return cls(
            message=message,
            auth_type=current_auth_type,
            required_auth_types=required_auth_types,
            status=401,
            **kwargs,
        )


@dataclass
class ClassError(DomoError):
    """Exception for class-specific errors.

    This exception is used when errors occur within specific Domo entity
    classes (DomoDataset, DomoCard, etc.). It provides enhanced context
    about the class instance and entity details.

    Attributes:
        entity_name: Human-readable name of the entity
        class_name: Name of the class where the error occurred

    Examples:
        >>> # Basic class error
        >>> error = ClassError(
        ...     message="Failed to update dataset",
        ...     entity_id="abc123",
        ...     class_name="DomoDataset"
        ... )

        >>> # From class instance
        >>> dataset = DomoDataset(id="abc123", name="Sales Data")
        >>> error = ClassError.from_class_instance(
        ...     dataset,
        ...     "Update failed",
        ...     cls_name_attr="name"
        ... )
    """

    entity_name: Optional[str] = None
    class_name: Optional[str] = None

    def __post_init__(self):
        """Extract class-specific information."""
        # If we have additional context with class info, extract it
        if "cls_instance" in self.additional_context:
            cls_instance = self.additional_context["cls_instance"]

            # Extract class name
            if not self.class_name and hasattr(cls_instance, "__class__"):
                self.class_name = cls_instance.__class__.__name__

            # Extract entity ID
            if not self.entity_id and hasattr(cls_instance, "id"):
                self.entity_id = cls_instance.id

            # Extract entity name using specified attribute
            cls_name_attr = self.additional_context.get("cls_name_attr")
            if (
                not self.entity_name
                and cls_name_attr
                and hasattr(cls_instance, cls_name_attr)
            ):
                self.entity_name = getattr(cls_instance, cls_name_attr)

        # Set parent_class from class_name if not set
        if not self.parent_class and self.class_name:
            self.parent_class = self.class_name

        super().__post_init__()

    def __str__(self) -> str:
        """Enhanced string representation for class errors."""
        base_str = super().__str__()

        if self.entity_name and self.entity_id:
            # Add entity name to the representation
            return base_str.replace(
                f"entity: {self.entity_id}",
                f"entity: {self.entity_id} ({self.entity_name})",
            )

        return base_str

    @classmethod
    def from_class_instance(
        cls,
        cls_instance: Any,
        message: str,
        cls_name_attr: Optional[str] = None,
        **kwargs,
    ) -> "ClassError":
        """Create a ClassError from a class instance.

        Args:
            cls_instance: The class instance that caused the error
            message: Error message
            cls_name_attr: Attribute name to use for entity name (e.g., 'name', 'title')
            **kwargs: Additional parameters

        Returns:
            ClassError instance with extracted class context

        Examples:
            >>> dataset = DomoDataset(id="abc123", name="Sales Data")
            >>> error = ClassError.from_class_instance(
            ...     dataset,
            ...     "Dataset validation failed",
            ...     cls_name_attr="name"
            ... )
        """
        additional_context = kwargs.pop("additional_context", {})
        additional_context.update(
            {"cls_instance": cls_instance, "cls_name_attr": cls_name_attr}
        )

        return cls(message=message, additional_context=additional_context, **kwargs)

    @classmethod
    def for_missing_attribute(
        cls,
        cls_instance: Any,
        attribute_name: str,
        operation: str = "operation",
        **kwargs,
    ) -> "ClassError":
        """Create a ClassError for missing required attributes.

        Args:
            cls_instance: The class instance missing the attribute
            attribute_name: Name of the missing attribute
            operation: Description of the operation that failed
            **kwargs: Additional parameters

        Returns:
            ClassError instance for missing attribute
        """
        class_name = (
            cls_instance.__class__.__name__
            if hasattr(cls_instance, "__class__")
            else "object"
        )
        message = f"{operation} failed: {class_name} missing required attribute '{attribute_name}'"

        return cls.from_class_instance(cls_instance, message, **kwargs)

    @classmethod
    def for_invalid_state(
        cls,
        cls_instance: Any,
        expected_state: str,
        current_state: str,
        operation: str = "operation",
        **kwargs,
    ) -> "ClassError":
        """Create a ClassError for invalid object state.

        Args:
            cls_instance: The class instance in invalid state
            expected_state: What state was expected
            current_state: What state the object is in
            operation: Description of the operation that failed
            **kwargs: Additional parameters

        Returns:
            ClassError instance for invalid state
        """
        class_name = (
            cls_instance.__class__.__name__
            if hasattr(cls_instance, "__class__")
            else "object"
        )
        message = f"{operation} failed: {class_name} in state '{current_state}', expected '{expected_state}'"

        return cls.from_class_instance(cls_instance, message, **kwargs)
