"""Routes package

This package organizes route modules by domain. Subpackages like
`instance_config` are exposed for convenience so modules can be imported via:

        from domolibrary2.routes.instance_config import api_client

"""

# Re-export key subpackages for static analyzers and convenience
from . import instance_config  # noqa: F401

__all__ = [
    "instance_config",
]
