"""
Test script to verify the modular page structure works correctly.

This script demonstrates that all functions and exceptions can be imported
from the main page module just like before, maintaining backward compatibility.
"""

# Test imports work exactly like before
try:
    from domolibrary2.routes.page import (
        # Exception classes
        Page_GET_Error,
        SearchPage_NotFound,
        Page_CRUD_Error,
        PageSharing_Error,
        # Core functions
        get_pages_adminsummary,
        get_page_by_id,
        get_page_definition,
        # Access functions
        get_page_access_test,
        get_page_access_list,
        # Property functions
        update_page_layout,
        put_writelock,
        delete_writelock,
        add_page_owner,
    )

    print("✅ All imports successful!")
    print(
        f"✅ Imported {len([Page_GET_Error, SearchPage_NotFound, Page_CRUD_Error, PageSharing_Error])} exception classes"
    )
    print(
        f"✅ Imported {len([get_pages_adminsummary, get_page_by_id, get_page_definition])} core functions"
    )
    print(
        f"✅ Imported {len([get_page_access_test, get_page_access_list])} access functions"
    )
    print(
        f"✅ Imported {len([update_page_layout, put_writelock, delete_writelock, add_page_owner])} property functions"
    )

    # Test individual module imports also work
    from domolibrary2.routes.page.core import get_page_by_id as core_get_page_by_id
    from domolibrary2.routes.page.access import (
        get_page_access_list as access_get_page_access_list,
    )
    from domolibrary2.routes.page.crud import (
        update_page_layout as props_update_page_layout,
    )
    from domolibrary2.routes.page.exceptions import (
        Page_GET_Error as exc_Page_GET_Error,
    )

    print("✅ Individual module imports also work!")

    # Verify functions are the same objects (proper re-export)
    assert get_page_by_id is core_get_page_by_id, "Core function re-export failed"
    assert (
        get_page_access_list is access_get_page_access_list
    ), "Access function re-export failed"
    assert (
        update_page_layout is props_update_page_layout
    ), "Property function re-export failed"
    assert Page_GET_Error is exc_Page_GET_Error, "Exception class re-export failed"

    print("✅ All function re-exports are correct!")
    print("✅ Modular page structure is working perfectly!")

except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Test failed: {e}")
