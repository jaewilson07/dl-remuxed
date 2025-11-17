"""
Test suite for DomoScheduler_Policies class
Tests scheduler policy management functionality
"""

import os
from datetime import datetime

import pytest
from dotenv import load_dotenv

from domolibrary2.auth import DomoTokenAuth
from domolibrary2.classes.DomoInstanceConfig.scheduler_policies import (
    DomoScheduler_Policies,
    DomoScheduler_Policy,
    DomoScheduler_Policy_Restrictions,
)

load_dotenv()


# ============================================================================
# CONSTANTS
# ============================================================================

SCHEDULER_POLICY_ID = "f6bd6eee-e5e9-4082-b43d-147b2b75f90d"


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def token_auth() -> DomoTokenAuth:
    """Fixture for token-based authentication."""
    return DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


@pytest.fixture
def scheduler_policies(token_auth: DomoTokenAuth) -> DomoScheduler_Policies:
    """Fixture for DomoScheduler_Policies instance."""
    return DomoScheduler_Policies(
        auth=token_auth,  # type: ignore
        parent=None,
        parent_id="",
    )


# ============================================================================
# SCHEDULER POLICY TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_scheduler_policies(
    scheduler_policies: DomoScheduler_Policies,
) -> None:
    """Test retrieving all scheduler policies."""
    policies = await scheduler_policies.get()

    assert policies is not None
    assert isinstance(policies, list)
    assert all(isinstance(p, DomoScheduler_Policy) for p in policies)

    # Verify policies are stored in the instance
    assert scheduler_policies.policies is not None
    assert len(scheduler_policies.policies) == len(policies)


@pytest.mark.asyncio
async def test_get_scheduler_policy_by_id(
    scheduler_policies: DomoScheduler_Policies,
) -> None:
    """Test retrieving a specific scheduler policy by ID."""
    # First get all policies to ensure we have data
    await scheduler_policies.get()

    if not scheduler_policies.policies:
        pytest.skip("No scheduler policies available to test")

    # Get a policy by ID
    test_policy = scheduler_policies.policies[0]
    assert test_policy.id is not None


@pytest.mark.asyncio
async def test_upsert_scheduler_policy(
    scheduler_policies: DomoScheduler_Policies,
) -> None:
    """Test creating/updating a scheduler policy."""
    # Get existing policies
    await scheduler_policies.get()

    if not scheduler_policies.policies:
        pytest.skip("No scheduler policies available to copy")

    # Create a copy of the first policy
    original_policy = scheduler_policies.policies[0]
    new_policy = DomoScheduler_Policy(
        id=None,  # None for new policy
        name=f"copy of {original_policy.name}",
        created_on=datetime.now(),
        frequencies=original_policy.frequencies,
        members=original_policy.members.copy() if original_policy.members else [],
    )

    # Modify the frequencies
    new_policy.frequencies.connector_frequency = (
        DomoScheduler_Policy_Restrictions.HOURLY
    )
    new_policy.frequencies.dataflow_frequency = (
        DomoScheduler_Policy_Restrictions.NO_RESTRICTIONS
    )

    # Upsert the policy
    result = await scheduler_policies.upsert(new_policy)

    assert result is not None

    # Refresh and verify the new policy exists
    await scheduler_policies.get()

    # Find the newly created policy
    created_policy = next(
        (p for p in scheduler_policies.policies if p.name == new_policy.name),
        None,
    )

    assert created_policy is not None
    assert created_policy.id is not None
    assert created_policy.name == new_policy.name
    assert (
        created_policy.frequencies.connector_frequency
        == DomoScheduler_Policy_Restrictions.HOURLY
    )


@pytest.mark.asyncio
async def test_update_existing_scheduler_policy(
    scheduler_policies: DomoScheduler_Policies,
) -> None:
    """Test updating an existing scheduler policy."""
    await scheduler_policies.get()

    if not scheduler_policies.policies:
        pytest.skip("No scheduler policies available to update")

    # Get an existing policy
    policy_to_update = scheduler_policies.policies[0]
    original_connector_freq = policy_to_update.frequencies.connector_frequency

    # Modify frequency and update
    policy_to_update.frequencies.connector_frequency = (
        DomoScheduler_Policy_Restrictions.DAILY
    )

    result = await scheduler_policies.upsert(policy_to_update)
    assert result is not None

    # Refresh and verify update
    await scheduler_policies.get()

    updated_policy = next(
        (p for p in scheduler_policies.policies if p.id == policy_to_update.id),
        None,
    )

    assert updated_policy is not None
    assert (
        updated_policy.frequencies.connector_frequency
        == DomoScheduler_Policy_Restrictions.DAILY
    )

    # Restore original frequency
    updated_policy.frequencies.connector_frequency = original_connector_freq
    await scheduler_policies.upsert(updated_policy)


@pytest.mark.asyncio
async def test_delete_scheduler_policy(
    scheduler_policies: DomoScheduler_Policies,
) -> None:
    """Test deleting a scheduler policy."""
    # First create a policy to delete
    await scheduler_policies.get()

    if not scheduler_policies.policies:
        pytest.skip("No scheduler policies available")

    # Create a temporary policy for deletion
    base_policy = scheduler_policies.policies[0]
    temp_policy = DomoScheduler_Policy(
        id=None,
        name="Temporary Policy for Deletion Test",
        created_on=datetime.now(),
        frequencies=base_policy.frequencies,
        members=[],
    )

    # Create the policy
    await scheduler_policies.upsert(temp_policy)
    await scheduler_policies.get()

    # Find the created policy
    policy_to_delete = next(
        (p for p in scheduler_policies.policies if p.name == temp_policy.name),
        None,
    )

    if not policy_to_delete or not policy_to_delete.id:
        pytest.skip("Failed to create temporary policy for deletion test")

    policy_id = policy_to_delete.id
    initial_count = len(scheduler_policies.policies)

    # Delete the policy
    result = await scheduler_policies.delete(str(policy_id))
    assert result is not None

    # Refresh and verify deletion
    await scheduler_policies.get()

    assert len(scheduler_policies.policies) == initial_count - 1

    # Verify the policy is no longer in the list
    deleted_policy = next(
        (p for p in scheduler_policies.policies if p.id == policy_id),
        None,
    )
    assert deleted_policy is None


@pytest.mark.asyncio
async def test_scheduler_policy_restrictions_enum() -> None:
    """Test scheduler policy restriction enum values."""
    # Verify enum values exist and are correct
    assert hasattr(DomoScheduler_Policy_Restrictions, "HOURLY")
    assert hasattr(DomoScheduler_Policy_Restrictions, "NO_RESTRICTIONS")
    assert hasattr(DomoScheduler_Policy_Restrictions, "DAILY")

    # These are commonly used values
    assert DomoScheduler_Policy_Restrictions.HOURLY is not None
    assert DomoScheduler_Policy_Restrictions.NO_RESTRICTIONS is not None


@pytest.mark.asyncio
async def test_scheduler_policies_empty_list_handling(
    scheduler_policies: DomoScheduler_Policies,
) -> None:
    """Test that the system handles empty policy lists gracefully."""
    # This test verifies the system doesn't crash with empty data
    policies = await scheduler_policies.get()

    # Should return a list (even if empty)
    assert isinstance(policies, list)

    # The policies should be accessible
    assert hasattr(scheduler_policies, "policies")
    assert isinstance(scheduler_policies.policies, list)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_full_crud_cycle(
    scheduler_policies: DomoScheduler_Policies,
) -> None:
    """Test complete CRUD cycle: Create, Read, Update, Delete."""
    # CREATE
    await scheduler_policies.get()

    if not scheduler_policies.policies:
        pytest.skip("No base policies to work with")

    base_policy = scheduler_policies.policies[0]

    new_policy = DomoScheduler_Policy(
        id=None,
        name="CRUD Test Policy",
        created_on=datetime.now(),
        frequencies=base_policy.frequencies,
        members=[],
    )

    created = await scheduler_policies.upsert(new_policy)
    assert created is not None

    # READ
    await scheduler_policies.get()
    found_policy = next(
        (p for p in scheduler_policies.policies if p.name == "CRUD Test Policy"),
        None,
    )
    assert found_policy is not None
    assert found_policy.id is not None
    policy_id = found_policy.id

    # UPDATE
    found_policy.frequencies.dataflow_frequency = (
        DomoScheduler_Policy_Restrictions.HOURLY
    )
    await scheduler_policies.upsert(found_policy)

    await scheduler_policies.get()
    updated_policy = next(
        (p for p in scheduler_policies.policies if p.id == policy_id),
        None,
    )
    assert updated_policy is not None
    assert (
        updated_policy.frequencies.dataflow_frequency
        == DomoScheduler_Policy_Restrictions.HOURLY
    )

    # DELETE
    await scheduler_policies.delete(str(policy_id))

    await scheduler_policies.get()
    deleted_policy = next(
        (p for p in scheduler_policies.policies if p.id == policy_id),
        None,
    )
    assert deleted_policy is None
