"""
Example Usage of the Unified Access Control System

This example demonstrates how the new unified access control system
intelligently maps users and groups across different Domo objects.
"""

import asyncio
from domolibrary2.client.auth import DomoTokenAuth
from domolibrary2.classes.subentity import (
    DomoObjectAccessManager,
    AccessLevel,
    AccessType,
)


async def example_unified_access_control():
    """
    Example showing how to use the unified access control system
    across different Domo object types.
    """

    # Initialize authentication
    auth = DomoTokenAuth(domo_instance="your-instance", domo_access_token="your-token")

    # Create the unified access manager
    access_manager = DomoObjectAccessManager(auth)

    # Example 1: Check account access
    print("=== Account Access Example ===")
    from domolibrary2.classes.DomoAccount import DomoAccount_Default

    account = await DomoAccount_Default.get_by_id(auth=auth, account_id="123")
    account_access = await access_manager.get_object_access_summary(account)

    for entity_id, summary in account_access.items():
        print(f"Entity {entity_id} ({summary.entity_type.value}):")
        print(f"  Effective Access: {summary.effective_access_level.value}")
        print(f"  Direct Access: {summary.direct_access_level.value}")
        print(f"  Inherited Access: {summary.inherited_access_level.value}")

        for grant in summary.access_grants:
            print(f"    - {grant.access_level.value} via {grant.access_type.value}")
            if grant.inherited_from:
                print(f"      Inherited from: {grant.inherited_from}")

    # Example 2: Check group membership
    print("\n=== Group Membership Example ===")
    from domolibrary2.classes.DomoGroup import DomoGroup

    group = await DomoGroup.get_by_id(auth=auth, group_id="456")
    group_access = await access_manager.get_object_access_summary(group)

    for entity_id, summary in group_access.items():
        print(f"Member {entity_id}:")
        print(f"  Role: {summary.effective_access_level.value}")

        # Show if they're an owner vs regular member
        if summary.effective_access_level == AccessLevel.OWNER:
            print("  Type: Group Owner")
        else:
            print("  Type: Group Member")

    # Example 3: Check card access
    print("\n=== Card Access Example ===")
    from domolibrary2.classes.DomoCard import DomoCard

    card = await DomoCard.get_by_id(auth=auth, card_id="789")
    card_access = await access_manager.get_object_access_summary(card)

    for entity_id, summary in card_access.items():
        print(f"User/Group {entity_id}:")
        print(f"  Access Level: {summary.effective_access_level.value}")

        # Show how access was granted
        direct_grants = [
            g for g in summary.access_grants if g.access_type == AccessType.DIRECT
        ]
        inherited_grants = [
            g for g in summary.access_grants if g.access_type == AccessType.INHERITED
        ]

        if direct_grants:
            print(f"  Direct: {direct_grants[0].access_level.value}")

        if inherited_grants:
            for grant in inherited_grants:
                print(
                    f"  Inherited from group {grant.inherited_from}: {grant.access_level.value}"
                )

    # Example 4: Cross-object access analysis
    print("\n=== Cross-Object Access Analysis ===")

    user_id = "user123"

    # Check this user's access across different object types
    objects_to_check = [account, group, card]

    print(f"Access summary for user {user_id}:")
    for obj in objects_to_check:
        controller = access_manager.get_controller(obj)
        user_summary = await controller.get_access_summary(user_id)

        print(
            f"  {type(obj).__name__} '{obj.id}': {user_summary.effective_access_level.value}"
        )

        # Show access path
        for grant in user_summary.access_grants:
            if grant.access_type == AccessType.INHERITED:
                print(f"    Via group: {grant.inherited_from}")
            elif grant.access_type == AccessType.DIRECT:
                print(f"    Direct access")


async def example_access_patterns():
    """
    Examples of common access patterns and how they're represented
    in the unified system.
    """

    print("=== Common Access Patterns ===")

    # Pattern 1: Department Group Access
    print("\n1. Department Group Access Pattern:")
    print("   - Sales group has EDITOR access to Sales dashboard")
    print("   - All sales users inherit EDITOR access")
    print("   - Sales manager has direct OWNER access")
    print(
        "   - Result: Manager gets OWNER (highest of EDITOR inherited + OWNER direct)"
    )

    # Pattern 2: PDP Policy Access
    print("\n2. PDP Policy Access Pattern:")
    print("   - Regional dataset has PDP policy for 'West Region'")
    print("   - Users tagged with 'West Region' get VIEWER access via policy")
    print("   - Data analyst has direct EDITOR access")
    print("   - Result: Analyst gets EDITOR, regional users get VIEWER")

    # Pattern 3: Hierarchical Group Access
    print("\n3. Hierarchical Group Access Pattern:")
    print("   - 'All Employees' group has VIEWER access to company dashboard")
    print("   - 'Managers' group (subset of employees) has EDITOR access")
    print("   - 'Executives' group (subset of managers) has ADMIN access")
    print("   - CEO has direct OWNER access")
    print("   - Result: CEO gets OWNER, Executives get ADMIN, etc.")

    # Pattern 4: Temporary Access
    print("\n4. Temporary Access Pattern:")
    print("   - Contractor added to project group for 3 months")
    print("   - Group has CONTRIBUTOR access to project datasets")
    print("   - Access automatically expires when group membership expires")
    print("   - System tracks expiry dates and access history")


if __name__ == "__main__":
    # Run examples
    asyncio.run(example_unified_access_control())
    asyncio.run(example_access_patterns())
