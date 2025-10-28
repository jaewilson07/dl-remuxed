"""
Example: Get all Scheduler Policies

This script demonstrates how to retrieve all scheduler policies from a Domo instance.

Usage:
    python scheduler_policies_get_policies.py [--domo-instance INSTANCE] [--domo-access-token TOKEN]

Environment Variables:
    DOMO_INSTANCE: Your Domo instance URL (e.g., 'mycompany.domo.com')
    DOMO_ACCESS_TOKEN: Your Domo access token

Example:
    export DOMO_INSTANCE="mycompany.domo.com"
    export DOMO_ACCESS_TOKEN="your-access-token-here"
    python scheduler_policies_get_policies.py
"""

import asyncio
import argparse
import os
from dotenv import load_dotenv
from pprint import pprint

from domolibrary2.client.auth import DomoTokenAuth
from domolibrary2.classes.DomoInstanceConfig.scheduler_policies import (
    DomoScheduler_Policies,
)


async def main(domo_instance: str, domo_access_token: str):
    """
    Main function to retrieve and display all scheduler policies.

    Args:
        domo_instance: The Domo instance URL
        domo_access_token: The Domo access token for authentication
    """
    print("=" * 80)
    print("GETTING SCHEDULER POLICIES")
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

    # Retrieve all policies
    print("\n3. Fetching all scheduler policies...")
    policies = await policies_manager.get()

    # Display results
    print(f"\n4. Found {len(policies)} scheduler policies:")
    print("-" * 80)

    for i, policy in enumerate(policies, 1):
        print(f"\nPolicy #{i}:")
        print(f"  ID: {policy.id}")
        print(f"  Name: {policy.name}")
        print(f"  Created On: {policy.created_on}")
        print(
            f"  Connector Frequency: {policy.frequencies.connector_frequency.name} ({policy.frequencies.connector_frequency.value} min)"
        )
        print(
            f"  Dataflow Frequency: {policy.frequencies.dataflow_frequency.name} ({policy.frequencies.dataflow_frequency.value} min)"
        )
        print(f"  Members ({len(policy.members)}):")
        for member in policy.members:
            print(f"    - {member.type}: {member.id}")

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)

    return policies


if __name__ == "__main__":
    load_dotenv(".env")
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Get all scheduler policies from a Domo instance"
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

    # Run the async main function
    asyncio.run(main(args.domo_instance, args.domo_access_token))
