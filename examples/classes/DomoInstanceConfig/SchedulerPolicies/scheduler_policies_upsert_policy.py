"""
Example: Upsert (Create or Update) a Scheduler Policy

This script demonstrates how to create a new scheduler policy or update an existing one.
Policy data is read from a JSON file (default: sample_policy.json).

Usage:
    # Create a new policy from sample JSON
    python scheduler_policies_upsert_policy.py

    # Update an existing policy
    python scheduler_policies_upsert_policy.py --policy-id "f6bd6eee-e5e9-4082-b43d-147b2b75f90d"

    # Use a custom JSON file
    python scheduler_policies_upsert_policy.py --policy-file my_policy.json

Environment Variables:
    DOMO_INSTANCE: Your Domo instance URL (e.g., 'mycompany.domo.com')
    DOMO_ACCESS_TOKEN: Your Domo access token
    SCHEDULER_POLICY_ID: (Optional) Policy ID to update. If not provided, creates new policy

Example:
    export DOMO_INSTANCE="mycompany.domo.com"
    export DOMO_ACCESS_TOKEN="your-access-token-here"
    python scheduler_policies_upsert_policy.py
"""

import asyncio
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from domolibrary2.client.auth import DomoTokenAuth
from domolibrary2.classes.DomoInstanceConfig.scheduler_policies import (
    DomoScheduler_Policies,
    DomoScheduler_Policy,
    DomoScheduler_Policy_Frequencies,
    DomoScheduler_Policy_Member,
    DomoScheduler_Policy_Restrictions,
)


def load_policy_from_json(json_file_path: str) -> dict:
    """
    Load policy data from a JSON file.

    Args:
        json_file_path: Path to the JSON file containing policy data

    Returns:
        dict: Policy data from the JSON file

    Expected JSON format:
    {
        "name": "Policy Name",
        "frequencies": {
            "connectorFrequency": 60,
            "dataflowFrequency": 0
        },
        "members": [
            {"type": "GROUP", "id": "123"},
            {"type": "USER", "id": "456"}
        ]
    }
    """
    if not Path(json_file_path).exists():
        raise FileNotFoundError(f"Policy JSON file not found: {json_file_path}")

    with open(json_file_path, "r") as f:
        return json.load(f)


async def main(
    domo_instance: str,
    domo_access_token: str,
    policy_json_file: str,
    policy_id: Optional[str] = None,
):
    """
    Main function to create or update a scheduler policy.

    Args:
        domo_instance: The Domo instance URL
        domo_access_token: The Domo access token for authentication
        policy_json_file: Path to JSON file containing policy data
        policy_id: Optional policy ID to update (if None, creates new policy)
    """
    print("=" * 80)
    print("UPSERTING SCHEDULER POLICY")
    print("=" * 80)

    # Load policy data from JSON file
    print(f"\n1. Loading policy data from: {policy_json_file}")
    policy_data = load_policy_from_json(policy_json_file)
    print(f"   ✓ Loaded policy: {policy_data.get('name', 'Unnamed')}")

    # Create authentication object
    print(f"\n2. Authenticating with Domo instance: {domo_instance}")
    token_auth = DomoTokenAuth(
        domo_instance=domo_instance,
        domo_access_token=domo_access_token,
    )

    # Create DomoScheduler_Policies instance and get existing policies
    print(
        "\n3. Creating DomoScheduler_Policies instance and fetching existing policies..."
    )
    policies_manager = DomoScheduler_Policies(auth=token_auth, parent=None, parent_id="")  # type: ignore
    await policies_manager.get()
    print(f"   Found {len(policies_manager.policies)} existing policies")

    # Parse members from JSON
    members = [
        DomoScheduler_Policy_Member(
            type=m["type"],  # type: ignore
            id=str(m["id"]),
        )
        for m in policy_data.get("members", [])
    ]

    # Create or prepare policy object
    if policy_id:
        print(f"\n4. Updating existing policy: {policy_id}")
        # Find existing policy
        existing_policy = next(
            (p for p in policies_manager.policies if p.id == policy_id), None
        )
        if not existing_policy:
            raise ValueError(f"Policy with ID {policy_id} not found")

        # Update fields from JSON
        existing_policy.name = policy_data["name"]
        existing_policy.frequencies.connector_frequency = (
            DomoScheduler_Policy_Restrictions(
                policy_data["frequencies"]["connectorFrequency"]
            )
        )
        existing_policy.frequencies.dataflow_frequency = (
            DomoScheduler_Policy_Restrictions(
                policy_data["frequencies"]["dataflowFrequency"]
            )
        )
        existing_policy.members = members
        policy = existing_policy
    else:
        print("\n4. Creating new policy")
        # Create new policy from JSON data
        policy = DomoScheduler_Policy(
            id=None,  # None indicates this is a new policy
            name=policy_data["name"],
            created_on=datetime.now(timezone.utc),
            frequencies=DomoScheduler_Policy_Frequencies(
                connector_frequency=DomoScheduler_Policy_Restrictions(
                    policy_data["frequencies"]["connectorFrequency"]
                ),
                dataflow_frequency=DomoScheduler_Policy_Restrictions(
                    policy_data["frequencies"]["dataflowFrequency"]
                ),
            ),
            members=members,
        )

    # Display policy details
    print("\n5. Policy details:")
    print(f"   Name: {policy.name}")
    print(
        f"   Connector Frequency: {policy.frequencies.connector_frequency.name} ({policy.frequencies.connector_frequency.value} min)"
    )
    print(
        f"   Dataflow Frequency: {policy.frequencies.dataflow_frequency.name} ({policy.frequencies.dataflow_frequency.value} min)"
    )
    print(f"   Members ({len(policy.members)}):")
    for member in policy.members:
        print(f"     - {member.type}: {member.id}")

    # Upsert the policy
    print("\n6. Upserting policy...")
    result_policy = await policies_manager.upsert(policy)

    # Display result
    print("\n7. Policy successfully upserted!")
    print(f"   Policy ID: {result_policy.id}")
    print(f"   Name: {result_policy.name}")
    print(f"   Created On: {result_policy.created_on}")

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)

    return result_policy


if __name__ == "__main__":
    load_dotenv(".env")

    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    default_json_file = script_dir / "sample_policy.json"

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Create or update a scheduler policy in a Domo instance. "
        "Policy data is read from a JSON file."
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
        help="Policy ID to update (if not provided, creates new policy)",
    )
    parser.add_argument(
        "--policy-file",
        type=str,
        default=str(default_json_file),
        help=f"Path to JSON file with policy data (default: {default_json_file})",
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
    asyncio.run(
        main(
            domo_instance=args.domo_instance,
            domo_access_token=args.domo_access_token,
            policy_json_file=args.policy_file,
            policy_id=args.policy_id,
        )
    )
