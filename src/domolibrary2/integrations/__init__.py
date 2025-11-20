# Integrations module - automatically imports all integration modules
# Users can import integrations like: from domolibrary2.integrations import Automation

# Import all integration modules
from . import Automation, RoleHierarchy, auth_utils, shortcut_fn
from .auth_utils import get_auth_from_codeengine

# Define what gets imported with "from domolibrary2.integrations import *"
__all__ = [
    "Automation",
    "RoleHierarchy",
    "shortcut_fn",
    "auth_utils",
    "get_auth_from_codeengine",
]
