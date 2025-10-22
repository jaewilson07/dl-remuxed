"""
Instance Config Package

This package provides instance configuration management functionality including
API client management, MFA settings, SSO configuration, and other instance-level settings.

Modules:
    exceptions: Exception classes for instance config operations
    api_client: API client (developer token) management functions
"""

# Import exception classes
from .exceptions import (
    ApiClient_CRUD_Error,
    ApiClient_GET_Error,
    ApiClient_RevokeError,
)

# Import API client functions and enums
from .api_client import (
    ApiClient_ScopeEnum,
    create_api_client,
    get_api_clients,
    get_client_by_id,
    revoke_api_client,
)

__all__ = [
    # Exception classes
    "ApiClient_GET_Error",
    "ApiClient_CRUD_Error",
    "ApiClient_RevokeError",
    # Enums
    "ApiClient_ScopeEnum",
    # API Client functions
    "get_api_clients",
    "get_client_by_id",
    "create_api_client",
    "revoke_api_client",
]
