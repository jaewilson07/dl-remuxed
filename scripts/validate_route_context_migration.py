#!/usr/bin/env python3
"""
Validation script for RouteContext migration in routes/card.py

This script validates that all 4 functions in routes/card.py have been
successfully migrated to support the RouteContext pattern.
"""

import inspect
from domolibrary2.routes import card
from domolibrary2.client.context import RouteContext


def validate_function_signature(func_name, func):
    """Validate that a function has the correct signature with context parameter."""
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    
    # Check for context parameter
    if 'context' not in params:
        return False, f"Missing 'context' parameter"
    
    # Check that context comes after positional args (indicated by '*' separator)
    # Context should be keyword-only
    context_param = sig.parameters['context']
    if context_param.kind != inspect.Parameter.KEYWORD_ONLY:
        return False, f"'context' should be keyword-only (after '*')"
    
    # Check for backward compatibility parameters
    required_params = ['debug_api', 'session', 'parent_class', 'debug_num_stacks_to_drop']
    missing = [p for p in required_params if p not in params]
    if missing:
        return False, f"Missing backward compatibility parameters: {missing}"
    
    return True, "OK"


def main():
    """Run validation checks."""
    print("=" * 70)
    print("RouteContext Migration Validation for routes/card.py")
    print("=" * 70)
    print()
    
    # Functions to validate
    functions_to_check = [
        ('get_card_by_id', card.get_card_by_id),
        ('get_kpi_definition', card.get_kpi_definition),
        ('get_card_metadata', card.get_card_metadata),
        ('search_cards_admin_summary', card.search_cards_admin_summary),
    ]
    
    all_passed = True
    
    for func_name, func in functions_to_check:
        is_valid, message = validate_function_signature(func_name, func)
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{status} - {func_name}: {message}")
        if not is_valid:
            all_passed = False
    
    print()
    print("-" * 70)
    
    # Validate RouteContext class
    print("\nValidating RouteContext class:")
    
    try:
        # Test creation
        ctx = RouteContext(
            debug_api=True,
            debug_num_stacks_to_drop=2,
            parent_class="TestClass"
        )
        print("✅ PASS - RouteContext can be instantiated")
        
        # Test to_dict
        ctx_dict = ctx.to_dict()
        assert all(k in ctx_dict for k in ['session', 'debug_api', 'debug_num_stacks_to_drop', 'parent_class'])
        print("✅ PASS - RouteContext.to_dict() works correctly")
        
        # Test from_params
        ctx2 = RouteContext.from_params(debug_api=False, parent_class='TestClass2')
        assert ctx2.debug_api == False
        assert ctx2.parent_class == 'TestClass2'
        print("✅ PASS - RouteContext.from_params() works correctly")
        
    except Exception as e:
        print(f"❌ FAIL - RouteContext validation error: {e}")
        all_passed = False
    
    print()
    print("=" * 70)
    
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED")
        print("\nMigration Summary:")
        print("- All 4 functions successfully migrated")
        print("- Context parameter is keyword-only")
        print("- Backward compatibility maintained")
        print("- RouteContext class fully functional")
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
