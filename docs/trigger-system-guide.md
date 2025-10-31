# Domo Trigger System

## Overview

The Domo Trigger System provides a comprehensive framework for managing execution triggers in Domo entities like DataFlows. Unlike the simpler `DomoSchedule` classes (which handle single schedule events), the trigger system supports **multiple, complex trigger configurations** including:

- **Schedule-based triggers** (cron-like time-based execution)
- **Dataset update triggers** (execute when specific datasets are updated)
- **Trigger conditions** (conditional logic for trigger execution)
- **Multiple triggers per entity** (e.g., a DataFlow with both scheduled and dataset-triggered execution)

## Architecture

```
DomoTriggerSettings (Container)
├── triggers: list[DomoTrigger]
├── zone_id: str (e.g., "UTC")
└── locale: str (e.g., "en_US")

DomoTrigger (Individual trigger configuration)
├── trigger_id: int
├── title: str
├── trigger_events: list[DomoTriggerEvent_Base]
│   ├── DomoTriggerEvent_Schedule
│   │   └── schedule: DomoSchedule_Base
│   └── DomoTriggerEvent_DatasetUpdated
│       ├── dataset_id: str
│       └── trigger_on_data_changed: bool
└── trigger_conditions: list[DomoTriggerCondition]
```

## Core Classes

### 1. DomoTriggerSettings

The top-level container managing all triggers for an entity.

```python
from domolibrary2.classes.subentity import DomoTriggerSettings

# Parse from API response
trigger_settings = DomoTriggerSettings.from_dict(api_response["triggerSettings"])

# Access triggers
print(f"Total triggers: {len(trigger_settings.triggers)}")
print(f"Timezone: {trigger_settings.zone_id}")

# Get specific trigger types
schedule_triggers = trigger_settings.get_schedule_triggers()
dataset_triggers = trigger_settings.get_dataset_triggers()

# Human-readable summary
print(trigger_settings.get_human_readable_summary())

# Iterate through triggers
for trigger in trigger_settings:
    print(trigger.title)
```

### 2. DomoTrigger

Represents a single trigger configuration with its events and conditions.

```python
# Access a specific trigger
trigger = trigger_settings.get_trigger_by_id(1)

print(f"Title: {trigger.title}")
print(f"Description: {trigger.get_human_readable_description()}")

# Check trigger types
if trigger.has_schedule_event():
    schedule_events = trigger.get_schedule_events()
    for event in schedule_events:
        print(f"Schedule: {event.schedule.get_human_readable_schedule()}")

if trigger.has_dataset_event():
    dataset_events = trigger.get_dataset_events()
    for event in dataset_events:
        print(f"Dataset: {event.dataset_id}")
```

### 3. DomoTriggerEvent Types

#### Schedule Events

Triggers based on time schedules (cron-like):

```python
from domolibrary2.classes.subentity import DomoTriggerEvent_Schedule

# Schedule event with cron expression
event_data = {
    "type": "SCHEDULE",
    "id": "schedule-id-123",
    "schedule": {
        "second": "0",
        "minute": "30",
        "hour": "14",
        "dayOfMonth": "*",
        "month": "*",
        "dayOfWeek": "MON",
        "year": "*"
    }
}

event = DomoTriggerEvent_Schedule.from_dict(event_data)
print(event.get_human_readable_description())
# Output: "Schedule: Custom schedule"
```

#### Dataset Update Events

Triggers based on dataset updates:

```python
from domolibrary2.classes.subentity import DomoTriggerEvent_DatasetUpdated

event_data = {
    "type": "DATASET_UPDATED",
    "datasetId": "abc-123",
    "triggerOnDataChanged": True
}

event = DomoTriggerEvent_DatasetUpdated.from_dict(event_data)
print(event.get_human_readable_description())
# Output: "Dataset abc-123 updated (when data changes)"
```

### 4. DomoTriggerCondition

Conditions that must be met for triggers to fire:

```python
from domolibrary2.classes.subentity import DomoTriggerCondition

condition_data = {
    "type": "DATASET_ROW_COUNT",
    "parameters": {
        "operator": "GREATER_THAN",
        "threshold": 1000
    }
}

condition = DomoTriggerCondition.from_dict(condition_data)
print(condition.get_human_readable_description())
```

## Example: DataFlow with Multiple Triggers

```python
# Example API response structure
dataflow_response = {
    "id": "dataflow-123",
    "name": "Sales ETL",
    "triggerSettings": {
        "triggers": [
            {
                "triggerId": 1,
                "title": "Daily Morning Run",
                "triggerEvents": [
                    {
                        "type": "SCHEDULE",
                        "id": "schedule-1",
                        "schedule": {
                            "second": "0",
                            "minute": "0",
                            "hour": "6",
                            "dayOfMonth": "*",
                            "month": "*",
                            "dayOfWeek": "*",
                            "year": "*"
                        }
                    }
                ],
                "triggerConditions": []
            },
            {
                "triggerId": 2,
                "title": "Sales Data Updated",
                "triggerEvents": [
                    {
                        "type": "DATASET_UPDATED",
                        "datasetId": "sales-dataset-id",
                        "triggerOnDataChanged": True
                    }
                ],
                "triggerConditions": []
            },
            {
                "triggerId": 3,
                "title": "Weekend Batch",
                "triggerEvents": [
                    {
                        "type": "SCHEDULE",
                        "schedule": {
                            "second": "0",
                            "minute": "0",
                            "hour": "2",
                            "dayOfMonth": "?",
                            "month": "*",
                            "dayOfWeek": "SAT",
                            "year": "*"
                        }
                    }
                ],
                "triggerConditions": []
            }
        ],
        "zoneId": "America/New_York",
        "locale": "en_US"
    }
}

# Parse trigger settings
trigger_settings = DomoTriggerSettings.from_dict(
    dataflow_response["triggerSettings"]
)

# Analyze triggers
print(f"DataFlow has {len(trigger_settings)} triggers")
print(f"Timezone: {trigger_settings.zone_id}")
print()

for trigger in trigger_settings:
    print(f"Trigger: {trigger.title}")
    print(f"  ID: {trigger.trigger_id}")
    print(f"  Description: {trigger.get_human_readable_description()}")
    print()

# Get specific trigger types
print("Schedule-based triggers:")
for trigger in trigger_settings.get_schedule_triggers():
    print(f"  - {trigger.title}")

print("\nDataset-based triggers:")
for trigger in trigger_settings.get_dataset_triggers():
    print(f"  - {trigger.title}")
```

## Integration with DomoDataflow

You can integrate `DomoTriggerSettings` into `DomoDataflow` as a subentity:

```python
from dataclasses import dataclass, field
from domolibrary2.classes.subentity import DomoTriggerSettings

@dataclass
class DomoDataflow(DomoEntity_w_Lineage):
    # ... existing fields ...

    TriggerSettings: DomoTriggerSettings = None

    def __post_init__(self):
        # Initialize trigger settings if present in raw data
        if self.raw.get("triggerSettings"):
            self.TriggerSettings = DomoTriggerSettings.from_dict(
                self.raw["triggerSettings"],
                parent=self
            )

    @classmethod
    def from_dict(cls, obj, auth):
        dataflow = cls(
            auth=auth,
            id=obj.get("id"),
            raw=obj,
            # ... other fields ...
        )
        return dataflow

# Usage
dataflow = await DomoDataflow.get_by_id(auth=auth, dataflow_id="123")

if dataflow.TriggerSettings:
    print(f"Dataflow has {len(dataflow.TriggerSettings)} triggers")
    print(dataflow.TriggerSettings.get_human_readable_summary())
```

## Comparison: DomoSchedule vs DomoTriggerSettings

### DomoSchedule (Simple)
- **Single schedule** per entity
- Perfect for **Streams** (one update schedule)
- Direct time-based configuration
- No conditional logic

```python
# DomoStream with simple schedule
stream.Schedule = DomoSchedule.from_dict({
    "scheduleExpression": "DAILY at 9:00 AM",
    "timezone": "UTC"
})
```

### DomoTriggerSettings (Complex)
- **Multiple triggers** per entity
- Perfect for **DataFlows** (multiple execution conditions)
- Supports schedules, dataset updates, and conditions
- Complex conditional logic

```python
# DomoDataflow with multiple triggers
dataflow.TriggerSettings = DomoTriggerSettings.from_dict({
    "triggers": [
        {"title": "Daily", "triggerEvents": [...]},
        {"title": "On dataset update", "triggerEvents": [...]}
    ]
})
```

## API Methods

### DomoTriggerSettings

```python
# Access and query
len(trigger_settings)                      # Number of triggers
trigger_settings[0]                        # Get first trigger
trigger_settings.get_trigger_by_id(1)      # Get specific trigger

# Filter by type
trigger_settings.get_schedule_triggers()   # All schedule triggers
trigger_settings.get_dataset_triggers()    # All dataset triggers

# Boolean checks
trigger_settings.has_any_schedules()       # Any schedule triggers?
trigger_settings.has_any_dataset_triggers() # Any dataset triggers?

# Display
trigger_settings.get_human_readable_summary()  # Full summary
str(trigger_settings)                          # Same as summary

# Serialization
trigger_settings.to_dict()                 # Convert to dict
```

### DomoTrigger

```python
# Access
trigger.trigger_id                         # Numeric ID
trigger.title                              # Human-readable title
trigger.trigger_events                     # List of events
trigger.trigger_conditions                 # List of conditions

# Query
trigger.has_schedule_event()               # Has schedule?
trigger.has_dataset_event()                # Has dataset update?
trigger.get_schedule_events()              # Get schedule events
trigger.get_dataset_events()               # Get dataset events

# Display
trigger.get_human_readable_description()   # Description
str(trigger)                               # Same as description
```

## Benefits

1. **Unified Model**: Single data structure for all trigger types
2. **Type Safety**: Strongly-typed event and condition classes
3. **Human Readable**: Built-in methods for displaying trigger configurations
4. **Extensible**: Easy to add new trigger event types
5. **Integration**: Works seamlessly with existing DomoSchedule infrastructure
6. **Round-trip Serialization**: Parse from API, modify, serialize back

## Future Enhancements

- Add support for webhook triggers
- Implement trigger validation logic
- Add trigger execution history tracking
- Support for more complex condition types
- Trigger dependency graphs (trigger chains)
