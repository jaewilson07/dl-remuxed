__version__ = "0.0.1-alpha"

# Import submodules to make them available
# Note: classes, client, and routes have circular dependencies
# If you encounter import errors, import individual modules directly like:
# from domolibrary2.client.auth import DomoAuth
# from domolibrary2.routes.user import get_user
# from domolibrary2.classes.DomoUser import DomoUser

from . import client, routes, utils, classes, integrations


# Define what gets imported with "from domolibrary2 import *"
__all__ = [
    "__version__",
    "classes",
    "integrations",
    "client",
    "routes",
    "utils",
]
