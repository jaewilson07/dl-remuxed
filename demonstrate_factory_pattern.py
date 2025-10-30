#!/usr/bin/env python3
"""
Demonstrate the DomoSchedule factory method logic without full imports
"""


def demonstrate_factory_logic():
    """Show how the factory method determines schedule types"""

    print("DomoSchedule Factory Method Logic Demonstration")
    print("=" * 55)

    # Simulate the factory method logic
    def determine_schedule_type_logic(obj):
        """Simulate DomoSchedule.determine_schedule_type logic"""

        # Check for advanced schedule (has advancedScheduleJson)
        if "advancedScheduleJson" in obj and obj["advancedScheduleJson"]:
            return "DomoAdvancedSchedule"

        # Check for cron expression
        if "scheduleExpression" in obj:
            expression = obj["scheduleExpression"]

            # Simple expressions (MANUAL, ONCE)
            if expression in ["MANUAL", "ONCE"]:
                return "DomoSimpleSchedule"

            # Cron expressions (contain spaces and numbers)
            elif " " in expression and any(c.isdigit() for c in expression):
                return "DomoCronSchedule"

        # Default to simple schedule
        return "DomoSimpleSchedule"

    # Test cases
    test_cases = [
        {
            "description": "Advanced Schedule with JSON",
            "data": {
                "advancedScheduleJson": {"frequency": "DAILY", "hour": 9, "minute": 30}
            },
        },
        {
            "description": "Cron Schedule - Daily at 9 AM",
            "data": {"scheduleExpression": "0 9 * * *"},
        },
        {
            "description": "Cron Schedule - Weekdays at 2:30 PM",
            "data": {"scheduleExpression": "30 14 * * 1-5"},
        },
        {
            "description": "Simple Schedule - Manual",
            "data": {"scheduleExpression": "MANUAL"},
        },
        {
            "description": "Simple Schedule - Run Once",
            "data": {"scheduleExpression": "ONCE"},
        },
        {"description": "Empty Schedule Data", "data": {}},
        {
            "description": "Advanced Weekly Schedule",
            "data": {
                "advancedScheduleJson": {
                    "frequency": "WEEKLY",
                    "daysOfWeek": [1, 3, 5],
                    "hour": 14,
                    "minute": 30,
                }
            },
        },
    ]

    print("\nFactory Method Decision Tree:")
    print("1. Has 'advancedScheduleJson'? → DomoAdvancedSchedule")
    print("2. Has 'scheduleExpression'?")
    print("   • 'MANUAL' or 'ONCE' → DomoSimpleSchedule")
    print("   • Contains spaces & numbers → DomoCronSchedule")
    print("3. Default → DomoSimpleSchedule")

    print(f"\nTesting {len(test_cases)} scenarios:")
    print("-" * 55)

    for i, test_case in enumerate(test_cases, 1):
        data = test_case["data"]
        description = test_case["description"]
        determined_type = determine_schedule_type_logic(data)

        print(f"{i}. {description}")
        print(f"   Data: {data}")
        print(f"   → Type: {determined_type}")
        print()

    print("Benefits of Factory Pattern:")
    print("=" * 30)
    print("✓ Automatic type detection based on input data")
    print("✓ Single entry point for schedule creation")
    print("✓ Handles multiple input formats transparently")
    print("✓ Extensible for new schedule types")
    print("✓ Maintains backward compatibility")

    print("\nInheritance Hierarchy Summary:")
    print("=" * 30)
    print("DomoSchedule (Abstract Base Class)")
    print("├── Common interface: get_human_readable_schedule()")
    print("├── Factory method: determine_schedule_type()")
    print("├── Utility functions: _parse_datetime_input(), etc.")
    print("│")
    print("├── DomoAdvancedSchedule")
    print("│   └── Handles JSON-based schedule definitions")
    print("│")
    print("├── DomoCronSchedule")
    print("│   └── Handles cron expression parsing")
    print("│")
    print("└── DomoSimpleSchedule")
    print("    └── Handles MANUAL and ONCE schedules")


if __name__ == "__main__":
    demonstrate_factory_logic()
