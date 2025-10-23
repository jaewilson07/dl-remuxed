"""
CodeEngine Route Functions (Legacy)

This module provides backward compatibility imports from the new codeengine package.
All functionality has been moved to the codeengine/ subdirectory.

For new code, please import directly from:
    from domolibrary2.routes.codeengine import <function_name>
"""

__all__ = [
    "CodeEngine_GET_Error",
    "CodeEngine_CRUD_Error",
    "SearchCodeEngine_NotFound",
    "CodeEngine_InvalidPackage",
    "CodeEngine_FunctionCallError",
    "CodeEngine_API_Error",  # Backward compatibility alias
    "get_packages",
    "CodeEngine_Package_Parts",
    "get_codeengine_package_by_id",
    "get_package_versions",
    "get_codeengine_package_by_id_and_version",
    "test_package_is_released",
    "test_package_is_identical",
]

# Import all from the new package structure
from .codeengine import (
    CodeEngine_CRUD_Error,
    CodeEngine_FunctionCallError,
    CodeEngine_GET_Error,
    CodeEngine_InvalidPackage,
    CodeEngine_Package_Parts,
    SearchCodeEngine_NotFound,
    get_codeengine_package_by_id,
    get_codeengine_package_by_id_and_version,
    get_package_versions,
    get_packages,
    test_package_is_identical,
    test_package_is_released,
)

# Backward compatibility aliases
CodeEngine_API_Error = CodeEngine_GET_Error
