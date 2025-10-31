# Domo Trigger System - Quick Reference

## Import

```python
from domolibrary2.classes.subentity import (
    DomoTriggerSettings,
    DomoTrigger,
    DomoTriggerEvent_Schedule,
    DomoTriggerEvent_DatasetUpdated,
    DomoTriggerCondition,
    TriggerEventType,
)
```

## Parse Trigger Settings

```python
# From API response
trigger_settings = DomoTriggerSettings.from_dict(api_response["triggerSettings"])

# From parent entity (DomoDataflow)
trigger_settings = DomoTriggerSettings.from_parent(parent=dataflow, obj=obj)
```

## Access Triggers

```python
# Count
len(trigger_settings)

# Iterate
for trigger in trigger_settings:
    print(trigger.title)

# Index
first_trigger = trigger_settings[0]

# By ID
trigger = trigger_settings.get_trigger_by_id(1)
```

## Filter Triggers

```python
# Get schedule-based triggers
schedule_triggers = trigger_settings.get_schedule_triggers()

# Get dataset-based triggers
dataset_triggers = trigger_settings.get_dataset_triggers()

# Check if any exist
has_schedules = trigger_settings.has_any_schedules()
has_datasets = trigger_settings.has_any_dataset_triggers()
```

## Display

```python
# Human-readable summary
print(trigger_settings.get_human_readable_summary())
# or
print(str(trigger_settings))

# Individual trigger
print(trigger.get_human_readable_description())
# or
print(str(trigger))
```

## Query Trigger Events

```python
# Check trigger types
if trigger.has_schedule_event():
    schedule_events = trigger.get_schedule_events()

if trigger.has_dataset_event():
    dataset_events = trigger.get_dataset_events()

# Iterate events
for event in trigger.trigger_events:
    print(event.event_type)
    print(event.get_human_readable_description())
```

## Work with Schedule Events

```python
for event in trigger.get_schedule_events():
    if event.schedule:
        # Access DomoSchedule object
        print(event.schedule.frequency)
        print(event.schedule.get_human_readable_schedule())
        print(f"Hour: {event.schedule.hour}, Minute: {event.schedule.minute}")
```

## Work with Dataset Events

```python
for event in trigger.get_dataset_events():
    print(f"Dataset: {event.dataset_id}")
    print(f"On data changed: {event.trigger_on_data_changed}")
```

## Serialize

```python
# To dictionary
settings_dict = trigger_settings.to_dict()

# Individual trigger
trigger_dict = trigger.to_dict()

# Individual event
event_dict = event.to_dict()
```

## Common Patterns

### Analyze Dataflow Triggers

```python
dataflow = await DomoDataflow.get_by_id(auth=auth, dataflow_id="123")

if dataflow.TriggerSettings:
    print(f"Triggers: {len(dataflow.TriggerSettings)}")
    print(dataflow.TriggerSettings.get_human_readable_summary())
else:
    print("Manual execution only")
```

### Filter by Schedule Frequency

```python
from domolibrary2.classes.subentity.schedule import ScheduleFrequencyEnum

daily_triggers = []
for trigger in trigger_settings.get_schedule_triggers():
    for event in trigger.get_schedule_events():
        if event.schedule and event.schedule.frequency == ScheduleFrequencyEnum.DAILY:
            daily_triggers.append(trigger)
```

### Find Triggers for Specific Dataset

```python
target_dataset = "abc-123"
triggers_for_dataset = []

for trigger in trigger_settings.get_dataset_triggers():
    for event in trigger.get_dataset_events():
        if event.dataset_id == target_dataset:
            triggers_for_dataset.append(trigger)
```

### Create Trigger Settings

```python
# Schedule event
schedule_event = DomoTriggerEvent_Schedule.from_dict({
    "type": "SCHEDULE",
    "schedule": {
        "second": "0",
        "minute": "0",
        "hour": "9",
        "dayOfMonth": "*",
        "month": "*",
        "dayOfWeek": "MON-FRI",
        "year": "*"
    }
})

# Dataset event
dataset_event = DomoTriggerEvent_DatasetUpdated.from_dict({
    "type": "DATASET_UPDATED",
    "datasetId": "input-id",
    "triggerOnDataChanged": True
})

# Create trigger
trigger = DomoTrigger(
    trigger_id=1,
    title="Weekday Morning",
    trigger_events=[schedule_event],
    trigger_conditions=[]
)

# Create settings
settings = DomoTriggerSettings(
    triggers=[trigger],
    zone_id="America/New_York",
    locale="en_US"
)
```

## Trigger Settings Properties

```python
trigger_settings.triggers         # list[DomoTrigger]
trigger_settings.zone_id          # str (timezone)
trigger_settings.locale           # str (locale)
trigger_settings.raw              # dict (original data)
trigger_settings.parent           # Parent entity
```

## Trigger Properties

```python
trigger.trigger_id                # int
trigger.title                     # str
trigger.trigger_events            # list[DomoTriggerEvent_Base]
trigger.trigger_conditions        # list[DomoTriggerCondition]
trigger.raw                       # dict (original data)
```

## Event Properties

### Schedule Event
```python
event.event_type                  # TriggerEventType.SCHEDULE
event.schedule_id                 # str | None
event.schedule                    # DomoSchedule_Base | None
```

### Dataset Event
```python
event.event_type                  # TriggerEventType.DATASET_UPDATED
event.dataset_id                  # str
event.trigger_on_data_changed     # bool
```

## API Response Structure

```json
{
  "triggerSettings": {
    "triggers": [
      {
        "triggerId": 1,
        "title": "Trigger Title",
        "triggerEvents": [
          {
            "type": "SCHEDULE",
            "schedule": { /* cron components */ }
          },
          {
            "type": "DATASET_UPDATED",
            "datasetId": "abc-123",
            "triggerOnDataChanged": true
          }
        ],
        "triggerConditions": []
      }
    ],
    "zoneId": "UTC",
    "locale": "en_US"
  }
}
```

## When to Use

| Entity Type | Use DomoSchedule | Use DomoTriggerSettings |
|-------------|------------------|-------------------------|
| DomoStream  | ✅ Yes           | ❌ No                   |
| DomoDataflow| ❌ No            | ✅ Yes                  |
| DomoConnector| ✅ Yes          | ❌ No                   |

## Common Errors

```python
# ❌ Wrong: Trying to subscript function name
trigger_settings["triggerSettings"]  # If trigger_settings is the function

# ✅ Right: Parse the dict first
settings = DomoTriggerSettings.from_dict(data["triggerSettings"])

# ❌ Wrong: Assuming settings always exist
print(dataflow.TriggerSettings.triggers)  # May be None

# ✅ Right: Check first
if dataflow.TriggerSettings:
    print(dataflow.TriggerSettings.triggers)
```
