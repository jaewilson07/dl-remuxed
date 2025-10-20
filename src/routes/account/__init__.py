"""
Account Package

This package provides account management functionality split across multiple modules for better organization.

Modules:
    exceptions: Exception classes for account operations
    core: Core account retrieval functions
    oauth: OAuth-specific account functions
    config: Account configuration management
    crud: Create, read, update, delete operations
    sharing: Account sharing and access management
"""

# Import all exception classes
from .exceptions import (
    Account_GET_Error,
    SearchAccount_NotFound,
    Account_CRUD_Error,
    AccountSharing_Error,
    Account_Config_Error,
    Account_NoMatch,
    Account_CreateParams_Error,
)

# Import core functions
from .core import (
    get_available_data_providers,
    get_accounts,
    get_account_by_id,
)

# Import OAuth functions
from .oauth import (
    get_oauth_accounts,
    get_oauth_account_by_id,
)

# Import configuration functions
from .config import (
    get_account_config,
    get_oauth_account_config,
    update_account_config,
    update_oauth_account_config,
)

# Import CRUD functions
from .crud import (
    generate_create_account_body,
    create_account,
    delete_account,
    generate_create_oauth_account_body,
    create_oauth_account,
    delete_oauth_account,
    update_account_name,
    update_oauth_account_name,
)

# Import sharing functions and classes
from .sharing import (
    ShareAccount_V1_AccessLevel,
    ShareAccount_AccessLevel,
    get_account_accesslist,
    get_oauth_account_accesslist,
    share_account,
    share_oauth_account,
    share_account_v1,
)

__all__ = [
    # Exception classes
    "Account_GET_Error",
    "SearchAccount_NotFound",
    "Account_CRUD_Error",
    "AccountSharing_Error",
    "Account_Config_Error",
    "Account_NoMatch",
    "Account_CreateParams_Error",
    # Core functions
    "get_available_data_providers",
    "get_accounts",
    "get_account_by_id",
    # OAuth functions
    "get_oauth_accounts",
    "get_oauth_account_by_id",
    # Configuration functions
    "get_account_config",
    "get_oauth_account_config",
    "update_account_config",
    "update_oauth_account_config",
    # CRUD functions
    "generate_create_account_body",
    "create_account",
    "delete_account",
    "generate_create_oauth_account_body",
    "create_oauth_account",
    "delete_oauth_account",
    "update_account_name",
    "update_oauth_account_name",
    # Sharing functions and classes
    "ShareAccount_V1_AccessLevel",
    "ShareAccount_AccessLevel",
    "get_account_accesslist",
    "get_oauth_account_accesslist",
    "share_account",
    "share_oauth_account",
    "share_account_v1",
]
