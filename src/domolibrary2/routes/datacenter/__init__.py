"""
Datacenter Package

This package provides datacenter management functionality for searching, lineage, and sharing.

Modules:
    exceptions: Exception classes for datacenter operations
    core: Core datacenter functions, enums, and utilities
"""

# Import all exception classes
from .exceptions import (
    Datacenter_GET_Error,
    SearchDatacenter_NoResultsFound,
    ShareResource_Error,
)

# Backward compatibility alias
SearchDatacenter_GET_Error = Datacenter_GET_Error

# Import all enums
from .core import (
    Datacenter_Enum,
    Datacenter_Filter_Field_Certification_Enum,
    Datacenter_Filter_Field_Enum,
    Dataflow_Type_Filter_Enum,
    ShareResource_Enum,
)

# Import TypedDict
from .core import LineageNode

# Import utility functions
from .core import (
    generate_search_datacenter_account_body,
    generate_search_datacenter_body,
    generate_search_datacenter_filter,
    generate_search_datacenter_filter_search_term,
)

# Import route functions
from .core import (
    get_connectors,
    get_lineage_upstream,
    search_datacenter,
    share_resource,
)

__all__ = [
    # Exception classes
    "SearchDatacenter_NoResultsFound",
    "SearchDatacenter_GET_Error",  # Backward compatibility alias for Datacenter_GET_Error
    "Datacenter_GET_Error",
    "ShareResource_Error",
    # Enums
    "Datacenter_Enum",
    "Dataflow_Type_Filter_Enum",
    "Datacenter_Filter_Field_Enum",
    "Datacenter_Filter_Field_Certification_Enum",
    "ShareResource_Enum",
    # TypedDict
    "LineageNode",
    # Utility functions
    "generate_search_datacenter_filter",
    "generate_search_datacenter_filter_search_term",
    "generate_search_datacenter_body",
    "generate_search_datacenter_account_body",
    # Route functions
    "search_datacenter",
    "get_connectors",
    "get_lineage_upstream",
    "share_resource",
]
