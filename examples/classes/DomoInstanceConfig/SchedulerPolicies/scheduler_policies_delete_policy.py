"""
Example: Delete a Scheduler Policy

This script demonstrates how to delete a scheduler policy from a Domo instance.

Usage:
    python scheduler_policies_delete_policy.py [--domo-instance INSTANCE] [--domo-access-token TOKEN] [--policy-id ID]

Environment Variables:
    DOMO_INSTANCE: Your Domo instance URL (e.g., 'mycompany.domo.com')
    DOMO_ACCESS_TOKEN: Your Domo access token
    SCHEDULER_POLICY_ID: The ID of the policy to delete

Example:
    export DOMO_INSTANCE="mycompany.domo.com"
    export DOMO_ACCESS_TOKEN="your-access-token-here"
    export SCHEDULER_POLICY_ID="f6bd6eee-e5e9-4082-b43d-147b2b75f90d"
    python scheduler_policies_delete_policy.py
"""

import argparse
import asyncio
import os

from dotenv import load_dotenv

from domolibrary2.classes.DomoInstanceConfig.scheduler_policies import (
    DomoScheduler_Policies,
)
from domolibrary2.client.auth import DomoTokenAuth


async def main(domo_instance: str, domo_access_token: str, policy_id: str):
    """
    Main function to delete a scheduler policy.

    Args:
        domo_instance: The Domo instance URL
        domo_access_token: The Domo access token for authentication
        policy_id: The ID of the policy to delete
    """
    print("=" * 80)
    print("DELETING SCHEDULER POLICY")
    print("=" * 80)

    # Create authentication object
    print(f"\n1. Authenticating with Domo instance: {domo_instance}")
    token_auth = DomoTokenAuth(
        domo_instance=domo_instance,
        domo_access_token=domo_access_token,
    )

    # Create DomoScheduler_Policies instance
    print("\n2. Creating DomoScheduler_Policies instance...")
    policies_manager = DomoScheduler_Policies(auth=token_auth, parent=None, parent_id="")  # type: ignore

    # Get existing policies to verify the policy exists
    print("\n3. Fetching existing policies to verify policy exists...")
    await policies_manager.get()

    # Find the policy to delete
    policy_to_delete = next(
        (p for p in policies_manager.policies if p.id == policy_id), None
    )

    if policy_to_delete:
        print("\n4. Found policy to delete:")
        print(f"   ID: {policy_to_delete.id}")
        print(f"   Name: {policy_to_delete.name}")
        print(f"   Created On: {policy_to_delete.created_on}")
        print(f"   Members: {len(policy_to_delete.members)}")
    else:
        print(
            f"\n4. WARNING: Policy with ID '{policy_id}' not found in the list of policies."
        )
        print("   Attempting to delete anyway...")

    # Delete the policy
    print(f"\n5. Deleting policy: {policy_id}")
    success = await policies_manager.delete(policy_id=policy_id)

    # Display result
    if success:
        print("\n6. ✓ Policy successfully deleted!")

        # Verify deletion by fetching policies again
        print("\n7. Verifying deletion by fetching policies again...")
        await policies_manager.get()

        if policy_id not in {p.id for p in policies_manager.policies}:
            print("   ✓ Confirmed: Policy no longer exists")
        else:
            print("   ⚠ Warning: Policy still appears in the list")
    else:
        print("\n6. ✗ Failed to delete policy")
        print("   The API returned an unsuccessful response")

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)

    return success


if __name__ == "__main__":
    load_dotenv(".env")
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Delete a scheduler policy from a Domo instance"
    )
    parser.add_argument(
        "--domo-instance",
        type=str,
        default=os.environ.get("DOMO_INSTANCE"),
        help="Domo instance URL (default: from DOMO_INSTANCE env var)",
    )
    parser.add_argument(
        "--domo-access-token",
        type=str,
        default=os.environ.get("DOMO_ACCESS_TOKEN"),
        help="Domo access token (default: from DOMO_ACCESS_TOKEN env var)",
    )
    parser.add_argument(
        "--policy-id",
        type=str,
        default=os.environ.get("SCHEDULER_POLICY_ID"),
        help="Policy ID to delete (default: from SCHEDULER_POLICY_ID env var)",
    )

    args = parser.parse_args()

    # Validate required parameters
    if not args.domo_instance:
        raise ValueError(
            "DOMO_INSTANCE must be provided via argument or environment variable"
        )
    if not args.domo_access_token:
        raise ValueError(
            "DOMO_ACCESS_TOKEN must be provided via argument or environment variable"
        )
    if not args.policy_id:
        raise ValueError(
            "SCHEDULER_POLICY_ID must be provided via argument or environment variable"
        )

    # Run the async main function
    asyncio.run(main(args.domo_instance, args.domo_access_token, args.policy_id))
