"""
CodeEngine CRUD Route Functions (Legacy)

This module provides backward compatibility imports from the new codeengine package.
All functionality has been moved to the codeengine/ subdirectory.

For new code, please import directly from:
    from domolibrary2.routes.codeengine import <function_name>
"""

__all__ = [
    "CodeEnginePackageBuilder",
    "deploy_code_engine_package",
    "CodeEngine_InvalidPackage",
    "create_code_engine_package",
    "increment_version",
    "upsert_code_engine_package_version",
    "upsert_package",
]

# Import all from the new package structure
from .codeengine import (
    CodeEnginePackageBuilder,
    CodeEngine_InvalidPackage,
    create_code_engine_package,
    deploy_code_engine_package,
    increment_version,
    upsert_code_engine_package_version,
    upsert_package,
)

# Backward compatibility - import the error that was previously imported
from .codeengine import CodeEngine_GET_Error as CodeEngine_API_Error
