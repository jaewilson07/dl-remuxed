"""
User Properties Management Routes

This module provides functionality for managing user properties in Domo instances.
User properties include display name, email, phone, department, role, and other
user-specific attributes that can be updated via the identity API.

Functions:
    update_user: Update user properties
    generate_patch_user_property_body: Generate request body for property updates

Classes:
    UserProperty_Type: Enum of available user property types
    UserProperty: Class representing a user property with type and values

Exception Classes:
    No specific exceptions - uses User_CRUD_Error from user.py module
"""

__all__ = [
    "UserProperty_Type",
    "UserProperty", 
    "generate_patch_user_property_body",
    "update_user",
]

from enum import Enum
from typing import List, Optional

import httpx

from ...client.auth import DomoAuth
from ...client import get_data as gd
from ...client import response as rgd
from ...client.entities import DomoEnumMixin

# Import the User_CRUD_Error from the user module
from .user import User_CRUD_Error


class UserProperty_Type(DomoEnumMixin, Enum):
    """Enumeration of available user property types."""
    display_name = "displayName"
    email_address = "emailAddress"
    phone_number = "phoneNumber"
    title = "title"
    department = "department"
    web_landing_page = "webLandingPage"
    web_mobile_landing_page = "webMobileLandingPage"
    role_id = "roleId"
    employee_id = "employeeId"
    employee_number = "employeeNumber"
    hire_date = "hireDate"
    reports_to = "reportsTo"


class UserProperty:
    """Represents a user property with its type and values."""
    
    def __init__(self, property_type: UserProperty_Type, values):
        """Initialize a user property.
        
        Args:
            property_type: The type of property from UserProperty_Type enum
            values: The value(s) for the property (can be single value or list)
        """
        self.property_type = property_type
        self.values = self._value_to_list(values)

    @staticmethod
    def _value_to_list(values):
        """Convert values to list format if not already.
        
        Args:
            values: Single value or list of values
            
        Returns:
            list: Values as a list
        """
        return values if isinstance(values, list) else [values]

    def to_dict(self):
        """Convert the property to dictionary format for API requests.
        
        Returns:
            dict: Property in API format with key and values
        """
        return {
            "key": self.property_type.value,
            "values": self._value_to_list(self.values),
        }


def generate_patch_user_property_body(user_property_ls: List[UserProperty]):
    """Generate request body for user property updates.
    
    Args:
        user_property_ls: List of UserProperty objects to update
        
    Returns:
        dict: Request body with attributes array for PATCH request
    """
    return {
        "attributes": [user_property.to_dict() for user_property in user_property_ls]
    }


@gd.route_function
async def update_user(
    user_id: str,
    user_property_ls: List[UserProperty],
    auth: DomoAuth,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
    return_raw: bool = False,
):
    """Update user properties via the identity API.
    
    Args:
        user_id: ID of the user to update
        user_property_ls: List of UserProperty objects with updates
        auth: Authentication object
        debug_api: Enable API debugging
        session: HTTP client session
        parent_class: Name of calling class for debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        return_raw: Return raw API response without processing
        
    Returns:
        ResponseGetData object confirming property updates
        
    Raises:
        User_CRUD_Error: If property update fails
    """
    url = f"https://{auth.domo_instance}.domo.com/api/identity/v1/users/{user_id}"

    body = (
        generate_patch_user_property_body(user_property_ls)
        if isinstance(user_property_ls[0], UserProperty)
        else user_property_ls
    )

    res = await gd.get_data(
        url=url,
        method="PATCH",
        auth=auth,
        body=body,
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise User_CRUD_Error(
            operation="update_properties",
            user_id=user_id,
            res=res
        )

    return res