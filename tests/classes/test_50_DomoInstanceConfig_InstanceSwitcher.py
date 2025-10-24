"""
Test file for DomoInstanceConfig_InstanceSwitcher.
Tests instance switcher mapping configuration and management.
"""

import os

from dotenv import load_dotenv

import domolibrary2.classes.DomoInstanceConfig.isntance_switcher as instance_switcher
import domolibrary2.client.auth as dmda

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


async def test_cell_0(token_auth=token_auth) -> bool:
    """Helper function to verify authentication."""
    return await token_auth.who_am_i()


async def test_cell_1(token_auth=token_auth):
    """Test getting instance switcher mappings."""
    switcher = instance_switcher.InstanceSwitcher(auth=token_auth)

    # Get existing mappings
    mappings = await switcher.get_mapping(debug_api=False, return_raw=False)

    print(f"Retrieved {len(mappings)} instance switcher mappings")
    for mapping in mappings:
        print(f"  - {mapping.user_attribute} -> {mapping.target_instance}")

    return mappings


async def test_cell_2(token_auth=token_auth):
    """Test from_dict method on Mapping class."""
    # Create a sample mapping from dictionary
    sample_dict = {
        "userAttribute": "test_attribute",
        "instance": "test-instance.domo.com",
    }

    mapping = instance_switcher.InstanceSwitcher_Mapping.from_dict(sample_dict)

    print(f"Created mapping: {mapping.user_attribute} -> {mapping.target_instance}")

    # Verify .domo.com was stripped
    assert mapping.target_instance == "test-instance"

    # Test to_dict conversion
    result_dict = mapping.to_dict()
    print(f"Converted back to dict: {result_dict}")

    assert result_dict["userAttribute"] == "test_attribute"
    assert result_dict["instance"] == "test-instance.domo.com"

    return mapping


async def test_cell_3(token_auth=token_auth):
    """Test mapping equality and comparison."""
    mapping1 = instance_switcher.InstanceSwitcher_Mapping(
        user_attribute="attr1", target_instance="instance1.domo.com"
    )

    mapping2 = instance_switcher.InstanceSwitcher_Mapping(
        user_attribute="attr1", target_instance="instance1"
    )

    mapping3 = instance_switcher.InstanceSwitcher_Mapping(
        user_attribute="attr2", target_instance="instance2"
    )

    # Test equality
    assert mapping1 == mapping2  # Should be equal after .domo.com removal
    assert mapping1 != mapping3

    print("Mapping equality tests passed")

    return True


async def test_cell_4(token_auth=token_auth):
    """Test getting raw response."""
    switcher = instance_switcher.InstanceSwitcher(auth=token_auth)

    # Get raw response
    res = await switcher.get_mapping(debug_api=False, return_raw=True)

    print(f"Raw response status: {res.status}")
    print(f"Raw response is_success: {res.is_success}")

    return res


async def main(token_auth=token_auth):
    """Run all test functions."""
    fn_ls = [
        test_cell_0,
        test_cell_1,
        test_cell_2,
        test_cell_3,
        test_cell_4,
    ]

    for fn in fn_ls:
        print(f"\n{'='*60}")
        print(f"Running {fn.__name__}: {fn.__doc__.strip() if fn.__doc__ else ''}")
        print("=" * 60)
        try:
            await fn(token_auth=token_auth)
            print(f"✓ {fn.__name__} passed")
        except Exception as e:
            print(f"✗ {fn.__name__} failed: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        main(token_auth=token_auth),
    )
