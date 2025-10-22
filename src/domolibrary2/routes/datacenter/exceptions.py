"""
Datacenter Route Exception Classes

This module contains all exception classes used by datacenter route functions.

Exception Classes:
    SearchDatacenter_NoResultsFound: Raised when datacenter search returns no results
    Datacenter_GET_Error: Raised when datacenter retrieval operations fail
    ShareResource_Error: Raised when resource sharing operations fail
"""

from typing import Optional

from ...client.exceptions import RouteError


class SearchDatacenter_NoResultsFound(RouteError):
    """Raised when datacenter search operations return no results."""

    def __init__(self, res=None, message: Optional[str] = None, **kwargs):
        super().__init__(
            res=res,
            entity_id=getattr(getattr(res, "auth", None), "domo_instance", None) if res else None,
            message=message or "No results for query parameters",
            **kwargs,
        )


class Datacenter_GET_Error(RouteError):
    """Raised when datacenter retrieval operations fail."""

    def __init__(self, res=None, message: Optional[str] = None, **kwargs):
        super().__init__(
            res=res,
            entity_id=getattr(getattr(res, "auth", None), "domo_instance", None) if res else None,
            message=message or "Datacenter retrieval failed",
            **kwargs,
        )


class ShareResource_Error(RouteError):
    """Raised when resource sharing operations fail."""

    def __init__(
        self,
        message: Optional[str] = None,
        domo_instance: Optional[str] = None,
        parent_class: Optional[str] = None,
        function_name: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message or "Resource sharing operation failed",
            domo_instance=domo_instance,
            parent_class=parent_class,
            function_name=function_name,
            res=res,
            **kwargs,
        )
