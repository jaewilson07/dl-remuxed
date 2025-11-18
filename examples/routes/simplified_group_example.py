"""
Example demonstrating simplified group route function signatures.

The new pattern uses RouteContext.build_context() classmethod with **context_kwargs
to provide a clean API while maintaining full flexibility.
"""

import asyncio
import os
from dotenv import load_dotenv

import domolibrary2.auth as dmda
from domolibrary2.routes.group import (
    get_all_groups,
    search_groups_by_name,
    create_group,
)

load_dotenv()


async def main():
    # Setup authentication
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    print("=" * 60)
    print("Simplified Route Function API Examples")
    print("=" * 60)

    # Example 1: Call with just debug_api (most common use case)
    print("\n1. Simple call with debug_api:")
    print("   get_all_groups(auth=auth, debug_api=True, maximum=5)")
    res = await get_all_groups(auth=auth, debug_api=True, maximum=5)
    print(f"   ✓ Found {len(res.response)} groups")

    # Example 2: Call with multiple context parameters
    print("\n2. Call with multiple context parameters:")
    print("   search_groups_by_name(auth=auth, search_name='Test', ")
    print("                         debug_api=False, parent_class='MyClass')")
    try:
        res = await search_groups_by_name(
            auth=auth,
            search_name="Test Groupie",
            is_exact_match=False,
            debug_api=False,
            parent_class="ExampleScript",
        )
        print(f"   ✓ Found groups matching 'Test'")
    except Exception as e:
        print(f"   ℹ No groups found (expected): {type(e).__name__}")

    # Example 3: Using explicit RouteContext (advanced use case)
    print("\n3. Advanced: Using explicit RouteContext:")
    print("   from domolibrary2.client.context import RouteContext")
    print("   context = RouteContext(debug_api=True, parent_class='Advanced')")
    print("   get_all_groups(auth=auth, context=context, maximum=3)")
    from domolibrary2.client.context import RouteContext

    context = RouteContext(debug_api=True, parent_class="AdvancedExample")
    res = await get_all_groups(auth=auth, context=context, maximum=3)
    print(f"   ✓ Found {len(res.response)} groups using explicit context")

    # Example 4: Session reuse pattern
    print("\n4. Session reuse (performance optimization):")
    print("   import httpx")
    print("   async with httpx.AsyncClient() as session:")
    print("       res1 = await get_all_groups(auth=auth, session=session, maximum=2)")
    print("       res2 = await get_all_groups(auth=auth, session=session, maximum=2)")
    import httpx

    async with httpx.AsyncClient() as session:
        res1 = await get_all_groups(auth=auth, session=session, maximum=2)
        res2 = await get_all_groups(auth=auth, session=session, maximum=2)
        print(f"   ✓ Made 2 calls with shared session")
        print(f"     Call 1: {len(res1.response)} groups")
        print(f"     Call 2: {len(res2.response)} groups")

    print("\n" + "=" * 60)
    print("Benefits of Simplified API:")
    print("=" * 60)
    print("✓ Cleaner function signatures (no boilerplate params)")
    print("✓ Users can pass debug_api=True directly")
    print("✓ All RouteContext fields available via **kwargs")
    print("✓ Explicit RouteContext still supported for advanced cases")
    print("✓ Type hints and IDE autocomplete still work")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
