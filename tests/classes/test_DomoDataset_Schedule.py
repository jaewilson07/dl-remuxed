"""
Test DomoDataset_Default class with Schedule integration
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

# Load environment variables
load_dotenv()

import domolibrary2.client.auth as dmda
from domolibrary2.classes.DomoDataset.dataset_default import DomoDataset_Default
from domolibrary2.classes.subentity.schedule import DomoSchedule


# Setup auth
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_INSTANCE", "test"),
    domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", "test_token"),
)


def test_dataset_schedule_from_dict():
    """Test that DomoDataset_Default initializes Schedule from raw data"""
    
    # Test 1: Dataset with advanced schedule
    dataset_data = {
        "id": "abc-123",
        "name": "Test Dataset",
        "description": "Test dataset with schedule",
        "displayType": "TABLE",
        "dataProviderType": "API",
        "scheduleStartDate": "2024-01-01T12:00:00",
        "advancedScheduleJson": {
            "frequency": "HOURLY",
            "minute": 15,
            "interval": 2,
            "timezone": "UTC",
        },
        "isActive": True,
    }
    
    dataset = DomoDataset_Default.from_dict(dataset_data, auth=token_auth)
    
    assert dataset.id == "abc-123"
    assert dataset.name == "Test Dataset"
    assert dataset.Schedule is not None, "Schedule should be initialized"
    assert isinstance(dataset.Schedule, DomoSchedule), "Schedule should be a DomoSchedule instance"
    assert dataset.Schedule.frequency.value == "HOURLY"
    
    print(f"✅ Test 1 passed: Dataset with advanced schedule")
    print(f"   Schedule: {dataset.Schedule.get_human_readable_schedule()}")
    
    # Test 2: Dataset with simple schedule
    dataset_simple_data = {
        "id": "def-456",
        "name": "Test Dataset Simple",
        "displayType": "TABLE",
        "dataProviderType": "API",
        "scheduleExpression": "MANUAL",
    }
    
    dataset_simple = DomoDataset_Default.from_dict(dataset_simple_data, auth=token_auth)
    
    assert dataset_simple.Schedule is not None, "Schedule should be initialized"
    assert isinstance(dataset_simple.Schedule, DomoSchedule)
    assert dataset_simple.Schedule.frequency.value == "MANUAL"
    
    print(f"✅ Test 2 passed: Dataset with simple schedule")
    print(f"   Schedule: {dataset_simple.Schedule.get_human_readable_schedule()}")
    
    # Test 3: Dataset without schedule
    dataset_no_schedule_data = {
        "id": "ghi-789",
        "name": "Test Dataset No Schedule",
        "displayType": "TABLE",
        "dataProviderType": "API",
    }
    
    dataset_no_schedule = DomoDataset_Default.from_dict(dataset_no_schedule_data, auth=token_auth)
    
    assert dataset_no_schedule.Schedule is None, "Schedule should be None when no schedule data"
    
    print(f"✅ Test 3 passed: Dataset without schedule")
    
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("Testing DomoDataset_Default Schedule Integration")
    print("=" * 70)
    
    try:
        test_dataset_schedule_from_dict()
        print("\n" + "=" * 70)
        print("✅ All DomoDataset_Default schedule tests passed!")
        print("=" * 70)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
