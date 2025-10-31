# DomoTrigger and DomoSchedule Relationship

## Overview

The DomoTrigger system is built **on top of** the existing DomoSchedule infrastructure, extending it to handle complex, multi-trigger scenarios while maintaining full compatibility and consistency.

## Architecture

```
DomoSchedule_Base (time-based execution)
├── DomoSimpleSchedule (MANUAL, ONCE)
├── DomoCronSchedule (cron expressions)
└── DomoAdvancedSchedule (advanced JSON config)

DomoTriggerSettings (multi-trigger container)
└── DomoTrigger (individual trigger)
    ├── DomoTriggerEvent_Schedule ──> Uses DomoSchedule_Base
    ├── DomoTriggerEvent_DatasetUpdated
    └── DomoTriggerCondition
```

## Key Design: Composition, Not Duplication

### DomoTriggerEvent_Schedule Uses DomoSchedule Factory

```python
@classmethod
def from_dict(cls, obj: dict[str, Any]) -> "DomoTriggerEvent_Schedule":
    """Create schedule event from trigger event dict

    Leverages DomoSchedule factory to determine the appropriate schedule type
    (Simple, Cron, or Advanced) based on the schedule data structure.
    """
    schedule_id = obj.get("id")
    schedule_data = obj.get("schedule")

    # Parse schedule if present using DomoSchedule factory
    schedule = None
    if schedule_data:
        # Build cron expression for DomoSchedule
        cron_expr = cls._build_cron_expression(schedule_data)

        # Create schedule dict for DomoSchedule factory
        schedule_dict = {
            "scheduleExpression": cron_expr,
            "timezone": schedule_data.get("timezone"),
        }

        # Use DomoSchedule factory to determine appropriate schedule type
        # This ensures consistency with how Streams handle schedules
        schedule_class = DomoSchedule.determine_schedule_type(schedule_dict)
        schedule = schedule_class.from_dict(schedule_dict, parent=None)

        # Store raw schedule data for round-trip serialization
        schedule.raw["raw_schedule"] = schedule_data

    return cls(schedule_id=schedule_id, schedule=schedule, raw=obj)
```

### Benefits of This Approach

1. **Consistency**: Schedule parsing works identically for Streams, Dataflows, and Connectors
2. **Reusability**: All DomoSchedule methods work on trigger schedules
3. **Maintainability**: Schedule logic is in one place
4. **Extensibility**: New schedule types automatically work in triggers

## When to Use Each

### Use DomoSchedule Directly

For entities with **single, simple schedules**:

```python
# DomoStream - one schedule, simple time-based
stream.Schedule = DomoSchedule.from_parent(
    parent=stream,
    obj=stream.raw.get("updateSchedule")
)

# Access schedule properties
print(stream.Schedule.frequency)  # ScheduleFrequencyEnum.DAILY
print(stream.Schedule.get_human_readable_schedule())  # "Every 1 day(s) at 09:00"
```

**Entities**:
- DomoStream
- DomoConnector
- Simple batch jobs

### Use DomoTriggerSettings

For entities with **complex, multi-trigger scenarios**:

```python
# DomoDataflow - multiple triggers, mixed types
dataflow.TriggerSettings = DomoTriggerSettings.from_dict(
    dataflow.raw.get("triggerSettings"),
    parent=dataflow
)

# Access triggers
for trigger in dataflow.TriggerSettings:
    for event in trigger.trigger_events:
        if isinstance(event, DomoTriggerEvent_Schedule):
            # event.schedule is a DomoSchedule_Base instance
            print(event.schedule.frequency)
            print(event.schedule.get_human_readable_schedule())
```

**Entities**:
- DomoDataflow (complex ETL with multiple triggers)
- Future: DomoWorkflow, DomoAutomation

## Comparison

| Feature | DomoSchedule | DomoTriggerSettings |
|---------|--------------|---------------------|
| **Purpose** | Single time-based schedule | Multiple complex triggers |
| **Schedule parsing** | Built-in | Delegates to DomoSchedule |
| **Multiple triggers** | ❌ No | ✅ Yes |
| **Dataset triggers** | ❌ No | ✅ Yes |
| **Conditions** | ❌ No | ✅ Yes |
| **Timezone support** | ✅ Yes | ✅ Yes (inherited) |
| **Human-readable** | ✅ Yes | ✅ Yes (inherited) |
| **Used by** | Stream, Connector | Dataflow |

## Code Examples

### Example 1: Access Schedule from Trigger

```python
# Get dataflow
dataflow = await DomoDataflow.get_by_id(auth=auth, dataflow_id="df-123")

# Access schedule triggers
for trigger in dataflow.TriggerSettings.get_schedule_triggers():
    for event in trigger.get_schedule_events():
        # event.schedule is a DomoSchedule_Base instance
        schedule = event.schedule

        # Use all DomoSchedule methods
        print(f"Frequency: {schedule.frequency.value}")
        print(f"Hour: {schedule.hour}")
        print(f"Minute: {schedule.minute}")
        print(f"Timezone: {schedule.timezone}")
        print(f"Description: {schedule.get_human_readable_schedule()}")

        # Check specific frequencies
        from domolibrary2.classes.subentity.schedule import ScheduleFrequencyEnum
        if schedule.frequency == ScheduleFrequencyEnum.DAILY:
            print("This is a daily schedule")
```

### Example 2: Compare Stream and Dataflow Schedules

```python
# Stream has simple DomoSchedule
stream = await DomoStream.get_by_id(auth=auth, stream_id="stream-123")
if stream.Schedule:
    print(f"Stream runs: {stream.Schedule.get_human_readable_schedule()}")

# Dataflow has TriggerSettings with embedded DomoSchedule
dataflow = await DomoDataflow.get_by_id(auth=auth, dataflow_id="df-123")
if dataflow.TriggerSettings:
    for trigger in dataflow.TriggerSettings.get_schedule_triggers():
        for event in trigger.get_schedule_events():
            # Same schedule parsing as Stream!
            print(f"Dataflow runs: {event.schedule.get_human_readable_schedule()}")
```

### Example 3: Filter by Schedule Type

```python
from domolibrary2.classes.subentity.schedule import (
    ScheduleFrequencyEnum,
    DomoSimpleSchedule,
    DomoCronSchedule,
    DomoAdvancedSchedule
)

# Find daily dataflows
for trigger in dataflow.TriggerSettings.get_schedule_triggers():
    for event in trigger.get_schedule_events():
        schedule = event.schedule

        # Check frequency (inherited from DomoSchedule)
        if schedule.frequency == ScheduleFrequencyEnum.DAILY:
            print(f"Daily trigger: {trigger.title}")

        # Check schedule type
        if isinstance(schedule, DomoCronSchedule):
            print(f"Uses cron: {schedule.schedule_expression}")
        elif isinstance(schedule, DomoAdvancedSchedule):
            print(f"Uses advanced config: {schedule.advanced_schedule_json}")
```

## Implementation Notes

### DomoSchedule Factory

The DomoSchedule factory (`DomoSchedule.determine_schedule_type`) automatically selects the appropriate subclass:

```python
# From schedule.py
@classmethod
def determine_schedule_type(cls, obj: dict[str, Any]) -> type["DomoSchedule_Base"]:
    """Determine the appropriate schedule subclass based on input data"""
    field_mappings = cls._extract_field_mappings(obj)

    # Check for advanced schedule JSON
    if field_mappings["advanced_json"]:
        return DomoAdvancedSchedule

    # Check for schedule expression (cron-like)
    if field_mappings["schedule_expr"]:
        expr = cls._normalize_expression(field_mappings["schedule_expr"])
        frequency, schedule_type = cls._detect_expression_type(expr)

        if schedule_type == ScheduleType.SIMPLE:
            return DomoSimpleSchedule
        else:
            return DomoCronSchedule

    # Default to simple schedule
    return DomoSimpleSchedule
```

### DomoTriggerEvent_Schedule Leverages This

```python
# From trigger.py
schedule_class = DomoSchedule.determine_schedule_type(schedule_dict)
schedule = schedule_class.from_dict(schedule_dict, parent=None)
```

This ensures:
- ✅ Consistent schedule parsing across all entities
- ✅ All schedule types (Simple, Cron, Advanced) work in triggers
- ✅ New schedule types automatically supported
- ✅ Same timezone handling
- ✅ Same human-readable output

## Future Extensibility

### Adding New Schedule Types

If a new schedule type is added to DomoSchedule:

```python
# In schedule.py
class DomoAdvancedSchedule_v2(DomoSchedule_Base):
    """New advanced schedule format"""
    pass
```

It automatically works in triggers with **no changes needed** to the trigger system:

```python
# Triggers automatically use the new schedule type
trigger_event.schedule  # Could be any DomoSchedule_Base subclass
```

### Adding New Trigger Event Types

The trigger system is also extensible:

```python
# Add webhook triggers
class DomoTriggerEvent_Webhook(DomoTriggerEvent_Base):
    webhook_url: str
    webhook_secret: str

    def get_human_readable_description(self) -> str:
        return f"Webhook: {self.webhook_url}"
```

## Summary

**DomoTriggerSettings extends DomoSchedule by:**
- 📦 **Wrapping**: Schedule events contain DomoSchedule_Base instances
- 🔄 **Reusing**: All schedule parsing logic from DomoSchedule
- ➕ **Adding**: Dataset triggers, conditions, multi-trigger support
- 🎯 **Targeting**: Complex scenarios (Dataflows) vs simple schedules (Streams)

The relationship is **composition**, not duplication:
```
DomoTriggerEvent_Schedule
    └── Contains: DomoSchedule_Base
        └── Uses: All DomoSchedule parsing and display logic
```

This ensures a consistent, maintainable architecture across the entire library.
