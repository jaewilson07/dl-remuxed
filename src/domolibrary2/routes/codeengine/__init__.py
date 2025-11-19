"""
CodeEngine Package

This package provides codeengine management functionality split across multiple modules
for better organization.

Modules:
    exceptions: Exception classes for codeengine operations
    core: Core codeengine retrieval functions
    crud: Create, read, update, delete operations
"""

# Import all exception classes
# Import core functions
from .core import (
    CodeEngine_Package_Parts,
    execute_codeengine_function,
    get_codeengine_package_by_id,
    get_codeengine_package_by_id_and_version,
    get_current_package_version,
    get_package_versions,
    get_packages,
    test_package_is_identical,
    test_package_is_released,
)

from . import crud, core, packages

# Import CRUD functions
from .crud import (
    CodeEnginePackageBuilder,
    create_codeengine_package,
    deploy_codeengine_package,
    increment_version,
    share_accounts_with_package,
    upsert_codeengine_package_version,
    upsert_package,
)
from .exceptions import (
    CodeEngine_CRUD_Error,
    CodeEngine_FunctionCallError,
    CodeEngine_GET_Error,
    CodeEngine_InvalidPackageError,
    SearchCodeEngineNotFoundError,
)

from .packages import generate_share_account_package

# Backward compatibility alias
CodeEngine_API_Error = CodeEngine_GET_Error

__all__ = [
    "crud",
    "core",
    "packages"
    # Exception classes
    "CodeEngine_GET_Error",
    "SearchCodeEngineNotFoundError",
    "CodeEngine_CRUD_Error",
    "CodeEngine_InvalidPackageError",
    "CodeEngine_FunctionCallError",
    "CodeEngine_API_Error",  # Backward compatibility alias
    # Core functions
    "get_packages",
    "CodeEngine_Package_Parts",
    "get_codeengine_package_by_id",
    "get_package_versions",
    "get_current_package_version",
    "get_codeengine_package_by_id_and_version",
    "test_package_is_released",
    "test_package_is_identical",
    "execute_codeengine_function",
    # CRUD functions
    "CodeEnginePackageBuilder",
    "deploy_codeengine_package",
    "create_codeengine_package",
    "increment_version",
    "upsert_codeengine_package_version",
    "upsert_package",
    "share_accounts_with_package",
    "generate_share_account_package",
]
