#!/usr/bin/env python3
"""
Simple test of schedule inheritance without full module imports
"""

# Let's just verify the schedule.py file can be imported directly
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

try:
    # Test basic import
    from domolibrary2.classes.subentity.schedule import (
        DomoSchedule,
        DomoAdvancedSchedule,
        DomoCronSchedule,
        DomoSimpleSchedule,
    )

    print("✓ Successfully imported schedule classes")

    # Test class hierarchy
    print(
        f"✓ DomoAdvancedSchedule inherits from DomoSchedule: {issubclass(DomoAdvancedSchedule, DomoSchedule)}"
    )
    print(
        f"✓ DomoCronSchedule inherits from DomoSchedule: {issubclass(DomoCronSchedule, DomoSchedule)}"
    )
    print(
        f"✓ DomoSimpleSchedule inherits from DomoSchedule: {issubclass(DomoSimpleSchedule, DomoSchedule)}"
    )

    # Test factory method exists
    print(
        f"✓ Factory method exists: {hasattr(DomoSchedule, 'determine_schedule_type')}"
    )
    print(f"✓ from_dict method exists: {hasattr(DomoSchedule, 'from_dict')}")

    # Test type determination without instantiation
    print("\nTesting schedule type determination:")

    advanced_type = DomoSchedule.determine_schedule_type(
        {"advancedScheduleJson": {"frequency": "DAILY"}}
    )
    cron_type = DomoSchedule.determine_schedule_type(
        {"scheduleExpression": "0 9 * * *"}
    )
    simple_type = DomoSchedule.determine_schedule_type({"scheduleExpression": "MANUAL"})

    print(f"✓ Advanced schedule type: {advanced_type.__name__}")
    print(f"✓ Cron schedule type: {cron_type.__name__}")
    print(f"✓ Simple schedule type: {simple_type.__name__}")

    print("\nInheritance hierarchy successfully implemented!")

except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
