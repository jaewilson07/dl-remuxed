__version__ = "0.0.1-alpha"

# Import submodules to make them available
# Note: classes, client, and routes have circular dependencies
# If you encounter import errors, import individual modules directly like:
# from domolibrary2.client.auth import DomoAuth
# from domolibrary2.routes.user import get_user
# from domolibrary2.classes.DomoUser import DomoUser

from . import utils
from . import client
from . import routes


# Use lazy imports for modules with potential circular dependencies
def _lazy_import_classes():
    from . import classes

    return classes


def _lazy_import_integrations():
    from . import integrations

    return integrations


# Define what gets imported with "from domolibrary2 import *"
__all__ = [
    "__version__",
    "classes",
    "client",
    "routes",
    "utils",
    "integrations",
]

# Lazy loading for potentially circular imports
import sys

current_module = sys.modules[__name__]


def __getattr__(name):
    if name == "classes":
        classes = _lazy_import_classes()
        setattr(current_module, "classes", classes)
        return classes
    elif name == "integrations":
        integrations = _lazy_import_integrations()
        setattr(current_module, "integrations", integrations)
        return integrations
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
