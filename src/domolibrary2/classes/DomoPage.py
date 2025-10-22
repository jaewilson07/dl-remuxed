"""Legacy DomoPage module - redirects to page module.

This module maintains backward compatibility by importing from the new
modular page structure. All page functionality has been moved to the
classes.page submodule for better organization.

Deprecated: This module will be removed in a future version.
Please update imports to use: from domolibrary2.classes.page import DomoPage
"""

# For backward compatibility, import everything from the new page module
from .page import *

__all__ = ["DomoPage_GetRecursive", "DomoPage", "DomoPages", "Page_NoAccess"]
