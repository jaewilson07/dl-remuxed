#!/usr/bin/env python3
"""
Example demonstrating the DomoSchedule inheritance hierarchy and factory method
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from domolibrary2.classes.subentity.schedule import (
    DomoSchedule,
    DomoAdvancedSchedule,
    DomoCronSchedule,
    DomoSimpleSchedule,
)


def test_schedule_factory():
    """Test the schedule factory method with different input types"""

    print("=" * 50)
    print("DomoSchedule Inheritance Example")
    print("=" * 50)

    # Test 1: Advanced Schedule
    print("\n1. Advanced Schedule (JSON-based):")
    advanced_data = {
        "scheduleStartDate": "2024-01-01T09:00:00",
        "advancedScheduleJson": {
            "frequency": "DAILY",
            "hour": 9,
            "minute": 30,
            "interval": 1,
            "timezone": "America/New_York",
        },
        "isActive": True,
    }

    schedule1 = DomoSchedule.from_dict(advanced_data)
    print(f"Type: {type(schedule1).__name__}")
    print(f"Schedule Type: {schedule1.schedule_type.value}")
    print(f"Frequency: {schedule1.frequency.value}")
    print(f"Description: {schedule1.get_human_readable_schedule()}")
    print(f"Is Advanced Schedule: {isinstance(schedule1, DomoAdvancedSchedule)}")

    # Test 2: Cron Schedule
    print("\n2. Cron Schedule (Expression-based):")
    cron_data = {
        "scheduleStartDate": "2024-01-01T00:00:00",
        "scheduleExpression": "0 8 * * 1-5",  # 8 AM weekdays
        "isActive": True,
    }

    schedule2 = DomoSchedule.from_dict(cron_data)
    print(f"Type: {type(schedule2).__name__}")
    print(f"Schedule Type: {schedule2.schedule_type.value}")
    print(f"Frequency: {schedule2.frequency.value}")
    print(f"Description: {schedule2.get_human_readable_schedule()}")
    print(f"Is Cron Schedule: {isinstance(schedule2, DomoCronSchedule)}")

    # Test 3: Simple Schedule (Manual)
    print("\n3. Simple Schedule (Manual):")
    simple_data = {
        "scheduleStartDate": "2024-01-01T00:00:00",
        "scheduleExpression": "MANUAL",
        "isActive": True,
    }

    schedule3 = DomoSchedule.from_dict(simple_data)
    print(f"Type: {type(schedule3).__name__}")
    print(f"Schedule Type: {schedule3.schedule_type.value}")
    print(f"Frequency: {schedule3.frequency.value}")
    print(f"Description: {schedule3.get_human_readable_schedule()}")
    print(f"Is Simple Schedule: {isinstance(schedule3, DomoSimpleSchedule)}")

    # Test 4: Simple Schedule (Once)
    print("\n4. Simple Schedule (Run Once):")
    once_data = {
        "scheduleStartDate": "2024-12-25T00:00:00",
        "scheduleExpression": "ONCE",
        "isActive": True,
    }

    schedule4 = DomoSchedule.from_dict(once_data)
    print(f"Type: {type(schedule4).__name__}")
    print(f"Schedule Type: {schedule4.schedule_type.value}")
    print(f"Frequency: {schedule4.frequency.value}")
    print(f"Description: {schedule4.get_human_readable_schedule()}")
    print(f"Is Simple Schedule: {isinstance(schedule4, DomoSimpleSchedule)}")

    # Test 5: Complex Advanced Schedule
    print("\n5. Complex Advanced Schedule (Weekly):")
    weekly_data = {
        "scheduleStartDate": "2024-01-01T00:00:00",
        "advancedScheduleJson": {
            "frequency": "WEEKLY",
            "daysOfWeek": [1, 3, 5],  # Monday, Wednesday, Friday
            "hour": 14,
            "minute": 30,
            "timezone": "UTC",
        },
        "isActive": True,
    }

    schedule5 = DomoSchedule.from_dict(weekly_data)
    print(f"Type: {type(schedule5).__name__}")
    print(f"Schedule Type: {schedule5.schedule_type.value}")
    print(f"Frequency: {schedule5.frequency.value}")
    print(f"Description: {schedule5.get_human_readable_schedule()}")
    print(f"Days of Week: {schedule5.day_of_week}")

    # Test 6: Direct subclass instantiation
    print("\n6. Direct Subclass Creation:")
    direct_advanced = DomoAdvancedSchedule.from_dict(advanced_data)
    print(f"Direct creation type: {type(direct_advanced).__name__}")
    print(f"Same as factory? {type(direct_advanced) == type(schedule1)}")

    print("\n" + "=" * 50)
    print("Benefits of Inheritance Approach:")
    print("=" * 50)
    print("✓ Type safety - each schedule type has its own class")
    print("✓ Single Responsibility - each class handles one schedule type")
    print("✓ Extensibility - easy to add new schedule types")
    print("✓ Factory pattern - automatic type detection")
    print("✓ Polymorphism - all schedules share common interface")


def test_schedule_type_determination():
    """Test the schedule type determination logic"""

    print("\n" + "=" * 50)
    print("Schedule Type Determination Logic")
    print("=" * 50)

    test_cases = [
        # (description, data, expected_type)
        (
            "Advanced JSON",
            {"advancedScheduleJson": {"frequency": "DAILY"}},
            DomoAdvancedSchedule,
        ),
        ("Cron Expression", {"scheduleExpression": "0 9 * * *"}, DomoCronSchedule),
        ("Simple Manual", {"scheduleExpression": "MANUAL"}, DomoSimpleSchedule),
        ("Simple Once", {"scheduleExpression": "ONCE"}, DomoSimpleSchedule),
        ("No schedule data", {}, DomoSimpleSchedule),
        ("Complex cron", {"scheduleExpression": "30 14 * * 1,3,5"}, DomoCronSchedule),
    ]

    for description, data, expected_type in test_cases:
        determined_type = DomoSchedule.determine_schedule_type(data)
        result = "✓" if determined_type == expected_type else "✗"
        print(f"{result} {description}: {determined_type.__name__}")


if __name__ == "__main__":
    test_schedule_factory()
    test_schedule_type_determination()
