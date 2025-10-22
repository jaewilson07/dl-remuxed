"""
Page Route Functions

This module provides functions for managing Domo pages including retrieval,
layout management, access control, and sharing operations.

The module is organized into functional areas:
- core: Basic page retrieval and definition functions
- access: Access control and permissions functions
- crud: Layout management, locks, and ownership functions
- exceptions: All page-related exception classes

Functions:
    get_pages_adminsummary: Retrieve all pages visible to the user
    get_page_by_id: Retrieve a specific page by ID
    get_page_definition: Retrieve detailed page definition
    get_page_access_test: Test page access permissions
    get_page_access_list: Retrieve page access list with users and groups
    update_page_layout: Update page layout configuration
    put_writelock: Set write lock on a page layout
    delete_writelock: Remove write lock from a page layout
    add_page_owner: Add owners to pages

Exception Classes:
    Page_GET_Error: Raised when page retrieval fails
    SearchPage_NotFound: Raised when page search returns no results
    Page_CRUD_Error: Raised when page create/update/delete operations fail
    PageSharing_Error: Raised when page sharing operations fail
"""

# Import all functions and exceptions using wildcard imports
# This is safe because each submodule defines __all__ explicitly
from .exceptions import *
from .core import *
from .access import *
from .crud import *
