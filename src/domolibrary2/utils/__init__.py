"""
Utilities Library

A comprehensive collection of utility functions for data processing, file operations,
image handling, and common programming tasks. This library is designed to be
standalone and reusable across different projects.

Modules:
    chunk_execution: Async execution utilities with retry logic and concurrency control
    compare: Data comparison utilities for dictionaries and lists
    convert: Data conversion utilities for various formats and types
    DictDot: Dot notation access for dictionaries
    files: File and folder operation utilities
    Image: Image processing and manipulation utilities
    read_creds_from_dotenv: Environment credential reading utilities
    upload_data: Data upload utilities (may require external dependencies)
    xkcd_password: Password generation utilities
    exceptions: Custom exception classes for error handling

Usage:
    >>> from utils import chunk_execution, convert, DictDot
    >>> from utils.exceptions import UtilityError

    >>> # Use async utilities
    >>> await chunk_execution.run_with_retry(my_function)

    >>> # Convert data formats
    >>> datetime_obj = convert.convert_string_to_datetime("2023-01-01")

    >>> # Use dot notation for dictionaries
    >>> data = DictDot.DictDot({"user": {"name": "John"}})
    >>> print(data.user.name)  # "John"

Version: 1.0.0
Author: Domo Utils Contributors
License: MIT
"""

# Import exceptions for easy access
# Import main utility modules
from . import (
    DictDot,
    Image,
    chunk_execution,
    compare,
    convert,
    files,
    read_creds_from_dotenv,
    xkcd_password,
)

# Import legacy exception names from convert module for backwards compatibility
from .convert import (
    ConcatDataframe_InvalidElement,  # Legacy alias for ConcatDataframeError
    InvalidEmail,  # Legacy alias for InvalidEmailError
)
from .exceptions import (
    ConcatDataframeError,
    CredentialsError,
    FileOperationError,
    ImageProcessingError,
    InvalidEmailError,
    UtilityError,
)

# Conditional import for upload_data (may have external dependencies)
try:
    from . import upload_data

    _UPLOAD_DATA_AVAILABLE = True
except ImportError:
    _UPLOAD_DATA_AVAILABLE = False
    upload_data = None

# Always available standalone upload utilities
from . import upload_data_standalone

__all__ = [
    # Exception classes
    "UtilityError",
    "InvalidEmailError",
    "ConcatDataframeError",
    "FileOperationError",
    "ImageProcessingError",
    "CredentialsError",
    # Legacy exception names
    "InvalidEmail",
    "ConcatDataframe_InvalidElement",
    # Utility modules
    "chunk_execution",
    "compare",
    "convert",
    "DictDot",
    "files",
    "Image",
    "read_creds_from_dotenv",
    "xkcd_password",
    # Upload modules (conditional and standalone)
    "upload_data",  # May be None if dependencies not available
    "upload_data_standalone",  # Always available
]

__version__ = "1.0.0"
__author__ = "Domo Utils Contributors"
__license__ = "MIT"


# Utility functions for module introspection
def get_available_modules():
    """
    Get a list of available utility modules.

    Returns:
        dict: Dictionary with module names as keys and availability as values

    Example:
        >>> modules = get_available_modules()
        >>> print(modules['upload_data'])  # True or False
        >>> print(modules['upload_data_standalone'])  # Always True
    """
    return {
        "chunk_execution": True,
        "compare": True,
        "convert": True,
        "DictDot": True,
        "files": True,
        "Image": True,
        "read_creds_from_dotenv": True,
        "xkcd_password": True,
        "upload_data": _UPLOAD_DATA_AVAILABLE,
        "upload_data_standalone": True,
        "exceptions": True,
    }


def get_module_info():
    """
    Get information about the utils library.

    Returns:
        dict: Library information including version, available modules, etc.
    """
    return {
        "name": "utils",
        "version": __version__,
        "author": __author__,
        "license": __license__,
        "available_modules": get_available_modules(),
        "total_modules": len([m for m in get_available_modules().values() if m]),
    }
