"""
Test DomoDataflow class with Schedule integration
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

# Load environment variables
load_dotenv()

import domolibrary2.client.auth as dmda
from domolibrary2.classes.DomoDataflow.Dataflow import DomoDataflow
from domolibrary2.classes.subentity.schedule import DomoSchedule


# Setup auth
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_INSTANCE", "test"),
    domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", "test_token"),
)


def test_dataflow_schedule_from_dict():
    """Test that DomoDataflow initializes Schedule from raw data"""
    
    # Test 1: Dataflow with advanced schedule
    dataflow_data = {
        "id": "12345",
        "name": "Test Dataflow",
        "description": "Test dataflow with schedule",
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
    
    dataflow = DomoDataflow.from_dict(dataflow_data, auth=token_auth)
    
    assert dataflow.id == "12345"
    assert dataflow.name == "Test Dataflow"
    assert dataflow.Schedule is not None, "Schedule should be initialized"
    assert isinstance(dataflow.Schedule, DomoSchedule), "Schedule should be a DomoSchedule instance"
    assert dataflow.Schedule.frequency.value == "DAILY"
    
    print(f"✅ Test 1 passed: Dataflow with advanced schedule")
    print(f"   Schedule: {dataflow.Schedule.get_human_readable_schedule()}")
    
    # Test 2: Dataflow with cron expression
    dataflow_cron_data = {
        "id": "67890",
        "name": "Test Dataflow Cron",
        "scheduleExpression": "0 8 * * 1-5",  # 8 AM weekdays
        "isActive": True,
    }
    
    dataflow_cron = DomoDataflow.from_dict(dataflow_cron_data, auth=token_auth)
    
    assert dataflow_cron.Schedule is not None, "Schedule should be initialized"
    assert isinstance(dataflow_cron.Schedule, DomoSchedule)
    
    print(f"✅ Test 2 passed: Dataflow with cron expression")
    print(f"   Schedule: {dataflow_cron.Schedule.get_human_readable_schedule()}")
    
    # Test 3: Dataflow without schedule
    dataflow_no_schedule_data = {
        "id": "11111",
        "name": "Test Dataflow No Schedule",
    }
    
    dataflow_no_schedule = DomoDataflow.from_dict(dataflow_no_schedule_data, auth=token_auth)
    
    assert dataflow_no_schedule.Schedule is None, "Schedule should be None when no schedule data"
    
    print(f"✅ Test 3 passed: Dataflow without schedule")
    
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Testing DomoDataflow Schedule Integration")
    print("=" * 70)
    
    try:
        test_dataflow_schedule_from_dict()
        print("\n" + "=" * 70)
        print("✅ All DomoDataflow schedule tests passed!")
        print("=" * 70)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
