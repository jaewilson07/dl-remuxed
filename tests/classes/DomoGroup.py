"""Test DomoGroup and DomoGroups classes with RouteContext pattern."""

import os

import pytest
from dotenv import load_dotenv

import domolibrary2.auth as dmda
from domolibrary2.classes.DomoGroup import DomoGroup, DomoGroups

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


@pytest.mark.asyncio
async def test_get_all_groups(token_auth=token_auth):
    """Test getting all groups using DomoGroups manager."""
    domo_groups = DomoGroups(auth=token_auth)
    groups = await domo_groups.get(is_hide_system_groups=True)

    assert groups is not None
    assert isinstance(groups, list)
    assert len(groups) > 0
    print(f"Retrieved {len(groups)} groups")


@pytest.mark.asyncio
async def test_get_group_by_id(token_auth=token_auth):
    """Test getting a specific group by ID."""
    # First get all groups to find a test group
    domo_groups = DomoGroups(auth=token_auth)
    groups = await domo_groups.get(is_hide_system_groups=True)

    # Find a group with "test" in the name, or just use the first one
    test_group = next(
        (g for g in groups if "test" in g.name.lower()), groups[0] if groups else None
    )

    assert test_group is not None, "No groups found"

    # Get the group by ID
    domo_group = await DomoGroup.get_by_id(auth=token_auth, group_id=test_group.id)

    assert domo_group is not None
    assert domo_group.id == test_group.id
    assert domo_group.name == test_group.name
    print(f"Retrieved group: {domo_group.name} ({domo_group.id})")


@pytest.mark.asyncio
async def test_get_group_with_debug_api(token_auth=token_auth):
    """Test getting a group with debug_api flag."""
    domo_groups = DomoGroups(auth=token_auth)
    groups = await domo_groups.get(is_hide_system_groups=True)

    if groups:
        test_group = groups[0]

        # Test with debug_api=True using context_kwargs
        domo_group = await DomoGroup.get_by_id(
            auth=token_auth,
            group_id=test_group.id,
            debug_api=False,  # Set to False to avoid verbose output in tests
        )

        assert domo_group is not None
        assert domo_group.id == test_group.id
        print(f"Retrieved group with context: {domo_group.name}")


@pytest.mark.asyncio
async def test_search_group_by_name(token_auth=token_auth):
    """Test searching for a group by name."""
    domo_groups = DomoGroups(auth=token_auth)

    # Get all groups first
    all_groups = await domo_groups.get(is_hide_system_groups=True)

    if all_groups:
        # Search for the first group by name
        search_name = all_groups[0].name
        found_group = await domo_groups.search_by_name(
            group_name=search_name, only_allow_one=True
        )

        assert found_group is not None
        assert found_group.name == search_name
        print(f"Found group by name: {found_group.name}")


@pytest.mark.asyncio
async def test_get_system_groups_visibility(token_auth=token_auth):
    """Test checking system groups visibility setting."""
    domo_groups = DomoGroups(auth=token_auth)

    is_visible = await domo_groups.get_is_system_groups_visible()

    assert isinstance(is_visible, bool)
    print(f"System groups visible: {is_visible}")


@pytest.mark.asyncio
async def test_get_with_and_without_system_groups(token_auth=token_auth):
    """Test getting groups with and without system groups."""
    domo_groups = DomoGroups(auth=token_auth)

    # Get without system groups
    groups_no_system = await domo_groups.get(is_hide_system_groups=True)

    # Get with system groups
    groups_with_system = await domo_groups.get(is_hide_system_groups=False)

    assert len(groups_with_system) >= len(groups_no_system)
    print(
        f"Groups without system: {len(groups_no_system)}, with system: {len(groups_with_system)}"
    )


@pytest.mark.asyncio
async def test_group_display_url(token_auth=token_auth):
    """Test that groups have valid display URLs."""
    domo_groups = DomoGroups(auth=token_auth)
    groups = await domo_groups.get(is_hide_system_groups=True)

    if groups:
        test_group = groups[0]
        url = test_group.display_url()

        assert url is not None
        assert token_auth.domo_instance in url
        assert str(test_group.id) in url
        print(f"Display URL: {url}")


@pytest.mark.asyncio
async def test_group_membership_object_exists(token_auth=token_auth):
    """Test that DomoGroup has a Membership object."""
    domo_groups = DomoGroups(auth=token_auth)
    groups = await domo_groups.get(is_hide_system_groups=True)

    if groups:
        test_group = groups[0]

        assert hasattr(test_group, "Membership")
        assert test_group.Membership is not None
        print(f"Group {test_group.name} has Membership object")


@pytest.mark.asyncio
async def test_context_kwargs_passing(token_auth=token_auth):
    """Test that context kwargs are properly passed through methods."""
    domo_groups = DomoGroups(auth=token_auth)

    # Test passing session and debug_api through context_kwargs
    groups = await domo_groups.get(is_hide_system_groups=True, debug_api=False)

    assert groups is not None
    assert isinstance(groups, list)
    print(f"Context kwargs passed successfully, retrieved {len(groups)} groups")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
