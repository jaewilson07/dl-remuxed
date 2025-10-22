"""
DomoDataset Package

This package provides comprehensive dataset management functionality for Domo instances,
including dataset operations, schema management, PDP policies, streaming capabilities,
and connector management.

Classes:
    DomoDataset_Default: Core dataset operations and management
    FederatedDomoDataset: Federated dataset functionality
    DomoPublishDataset: Published dataset operations
    DomoDataset_Schema: Dataset schema management
    DomoDataset_Schema_Column: Individual column management
    PDP_Policy: PDP policy management
    DomoStream: Dataset streaming operations
    DomoConnector: Dataset connector management

Exceptions:
    DatasetNotFoundError: Raised when dataset cannot be found
    QueryRequestError: Raised when dataset query fails
    DatasetSchema_InvalidSchema: Raised when schema validation fails
    SearchPDP_NotFound: Raised when PDP policy search returns no results

Enums:
    DatasetSchema_Types: Available dataset schema types
    ShareDataset_AccessLevelEnum: Dataset sharing access levels
    StreamConfig_Mapping_snowflake: Snowflake stream mapping types
"""

# Import all classes and functionality from the package modules
from .Connector import DomoConnector, DomoConnectors
from .Dataset import (
    DomoDataset,
    DomoDataset_Default,
    DomoPublishDataset,
    FederatedDomoDataset,
)
from .PDP import Dataset_PDP_Policies, PDP_Parameter, PDP_Policy, SearchPDP_NotFound
from .Schema import (
    DatasetSchema_InvalidSchema,
    DatasetSchema_Types,
    DomoDataset_Schema,
    DomoDataset_Schema_Column,
)
from .Stream import (
    DomoStream,
    StreamConfig,
    StreamConfig_Mapping_snowflake,
    StreamConfig_Mapping_snowflake_federated,
    StreamConfig_Mapping_snowflake_internal_unload,
    StreamConfig_Mapping_snowflake_keypair_internal_managed_unload,
    StreamConfig_Mapping_snowflakekeypairauthentication,
    StreamConfig_Mappings,
)

# Import route-level exceptions that are commonly used
try:
    from ...routes.dataset import (
        DatasetNotFoundError,
        QueryRequestError,
        ShareDataset_AccessLevelEnum,
    )
except ImportError:
    # Fallback if route exceptions aren't available
    pass

__all__ = [
    # Main dataset classes
    "DomoDataset",
    "DomoDataset_Default",
    "DomoPublishDataset",
    "FederatedDomoDataset",
    # Schema management
    "DomoDataset_Schema",
    "DomoDataset_Schema_Column",
    "DatasetSchema_Types",
    "DatasetSchema_InvalidSchema",
    # PDP functionality
    "PDP_Policy",
    "PDP_Parameter",
    "Dataset_PDP_Policies",
    "SearchPDP_NotFound",
    # Streaming
    "DomoStream",
    "StreamConfig",
    "StreamConfig_Mappings",
    "StreamConfig_Mapping_snowflake",
    "StreamConfig_Mapping_snowflake_federated",
    "StreamConfig_Mapping_snowflake_internal_unload",
    "StreamConfig_Mapping_snowflake_keypair_internal_managed_unload",
    "StreamConfig_Mapping_snowflakekeypairauthentication",
    # Connectors
    "DomoConnector",
    "DomoConnectors",
    # Route exceptions (if available)
    "DatasetNotFoundError",
    "QueryRequestError",
    "ShareDataset_AccessLevelEnum",
]
