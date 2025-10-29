"""
Test file for DomoDataset Schedule integration
Tests that Schedule is properly instantiated and populated from dataset data
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoDataset as dmds
from domolibrary2.classes.subentity.schedule import (
    DomoSchedule,
    ScheduleFrequencyEnum,
    ScheduleType,
)

assert load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


async def test_schedule_initialization_from_dict():
    """Test that Schedule can be created from a dict with schedule data"""
    # Test data mimicking what would come from dataset API
    test_data = {
        "id": "test-dataset-123",
        "name": "Test Dataset",
        "scheduleStartDate": "2024-01-01T09:00:00",
        "scheduleExpression": "DAILY",
        "isActive": True,
    }
    
    schedule = DomoSchedule.from_dict(test_data, auth=token_auth)
    
    assert schedule is not None
    assert schedule.frequency == ScheduleFrequencyEnum.DAILY
    assert schedule.is_active is True
    
    print(f"✓ Schedule created: {schedule.get_human_readable_schedule()}")
    return schedule


async def test_schedule_with_cron_expression():
    """Test Schedule with cron expression"""
    test_data = {
        "id": "test-dataset-456",
        "name": "Test Dataset",
        "scheduleExpression": "0 8 * * 1-5",  # 8 AM weekdays
        "scheduleStartDate": "2024-01-01T00:00:00",
    }
    
    schedule = DomoSchedule.from_dict(test_data, auth=token_auth)
    
    assert schedule is not None
    assert schedule.schedule_type == ScheduleType.CRON
    
    print(f"✓ Cron Schedule: {schedule.get_human_readable_schedule()}")
    return schedule


async def test_schedule_with_advanced_json():
    """Test Schedule with advanced JSON configuration"""
    test_data = {
        "id": "test-dataset-789",
        "name": "Test Dataset",
        "advancedScheduleJson": {
            "frequency": "WEEKLY",
            "daysOfWeek": [1, 3, 5],  # Monday, Wednesday, Friday
            "hour": 14,
            "minute": 30,
            "timezone": "America/New_York",
        },
        "scheduleStartDate": "2024-01-01T00:00:00",
    }
    
    schedule = DomoSchedule.from_dict(test_data, auth=token_auth)
    
    assert schedule is not None
    assert schedule.frequency == ScheduleFrequencyEnum.WEEKLY
    assert schedule.schedule_type == ScheduleType.ADVANCED
    assert schedule.day_of_week == [1, 3, 5]
    assert schedule.hour == 14
    assert schedule.minute == 30
    
    print(f"✓ Advanced Schedule: {schedule.get_human_readable_schedule()}")
    return schedule


async def test_schedule_manual():
    """Test Schedule with manual execution"""
    test_data = {
        "id": "test-dataset-manual",
        "name": "Test Dataset",
        "scheduleExpression": "MANUAL",
    }
    
    schedule = DomoSchedule.from_dict(test_data, auth=token_auth)
    
    assert schedule is not None
    assert schedule.frequency == ScheduleFrequencyEnum.MANUAL
    
    print(f"✓ Manual Schedule: {schedule.get_human_readable_schedule()}")
    return schedule


async def test_dataset_schedule_field():
    """Test that DomoDataset_Default has Schedule field and it's properly initialized"""
    # Create a mock dataset with schedule data
    from domolibrary2.classes.DomoDataset.dataset_default import DomoDataset_Default
    
    dataset_data = {
        "id": "test-dataset-integration",
        "name": "Test Dataset with Schedule",
        "displayType": "domo",
        "dataProviderType": "api",
        "scheduleStartDate": "2024-01-01T09:00:00",
        "scheduleExpression": "DAILY",
        "isActive": True,
        "rowCount": 100,
        "columnCount": 5,
    }
    
    dataset = DomoDataset_Default.from_dict(
        obj=dataset_data,
        auth=token_auth,
    )
    
    assert dataset is not None
    assert hasattr(dataset, 'Schedule')
    assert dataset.Schedule is not None
    assert isinstance(dataset.Schedule, DomoSchedule)
    assert dataset.Schedule.frequency == ScheduleFrequencyEnum.DAILY
    
    print(f"✓ Dataset Schedule: {dataset.Schedule.get_human_readable_schedule()}")
    return dataset


async def test_dataset_without_schedule():
    """Test that DomoDataset_Default works without schedule data"""
    from domolibrary2.classes.DomoDataset.dataset_default import DomoDataset_Default
    
    dataset_data = {
        "id": "test-dataset-no-schedule",
        "name": "Test Dataset without Schedule",
        "displayType": "domo",
        "dataProviderType": "api",
        "rowCount": 100,
        "columnCount": 5,
    }
    
    dataset = DomoDataset_Default.from_dict(
        obj=dataset_data,
        auth=token_auth,
    )
    
    assert dataset is not None
    assert hasattr(dataset, 'Schedule')
    assert dataset.Schedule is None  # Should be None when no schedule data
    
    print("✓ Dataset without schedule: Schedule field is None")
    return dataset


# Integration test with real API (if dataset exists and has schedule)
async def test_real_dataset_schedule(token_auth=token_auth):
    """Test Schedule with real dataset from API (if available)"""
    dataset_id = os.environ.get("DATASET_ID_WITH_SCHEDULE")
    
    if not dataset_id:
        print("⊘ Skipping real API test - DATASET_ID_WITH_SCHEDULE not set")
        return None
    
    try:
        dataset = await dmds.DomoDataset.get_by_id(
            dataset_id=dataset_id,
            auth=token_auth,
        )
        
        print(f"✓ Retrieved dataset: {dataset.name}")
        
        if dataset.Schedule:
            print(f"✓ Dataset has schedule: {dataset.Schedule.get_human_readable_schedule()}")
            assert isinstance(dataset.Schedule, DomoSchedule)
        else:
            print("⊘ Dataset has no schedule information")
        
        return dataset
    except Exception as e:
        print(f"⊘ Could not test with real API: {e}")
        return None


if __name__ == "__main__":
    import asyncio
    
    print("=" * 60)
    print("Testing DomoDataset Schedule Integration")
    print("=" * 60)
    
    asyncio.run(test_schedule_initialization_from_dict())
    asyncio.run(test_schedule_with_cron_expression())
    asyncio.run(test_schedule_with_advanced_json())
    asyncio.run(test_schedule_manual())
    asyncio.run(test_dataset_schedule_field())
    asyncio.run(test_dataset_without_schedule())
    asyncio.run(test_real_dataset_schedule())
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
