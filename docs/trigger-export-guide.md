# export_as_dict() Method Guide

## Overview

The `export_as_dict()` method provides a unified, human-readable dictionary export format for trigger configurations. It extends the standard `to_dict()` method by including human-readable descriptions and leveraging DomoSchedule's `export_as_dict()` for consistent schedule formatting.

## Hierarchy

```
DomoTriggerSettings.export_as_dict()
    └── Calls DomoTrigger.export_as_dict() for each trigger
        └── Calls DomoTriggerEvent_*.export_as_dict() for each event
            └── For schedule events: Calls DomoSchedule.export_as_dict()
```

## Methods Available

### DomoTriggerSettings.export_as_dict()

Returns a comprehensive dictionary with:
- All triggers (with human-readable descriptions)
- Zone ID and locale
- Summary text
- Statistics (total, schedule, dataset counts)

```python
exported = dataflow.TriggerSettings.export_as_dict()

# Structure:
{
    "triggers": [...],  # Each trigger with export_as_dict()
    "zoneId": "America/New_York",
    "locale": "en_US",
    "summary": "Triggers (2):\n  • ...",
    "stats": {
        "totalTriggers": 2,
        "scheduleTriggers": 1,
        "datasetTriggers": 1
    }
}
```

### DomoTrigger.export_as_dict()

Returns trigger details with:
- Trigger ID and title
- All events (with human-readable descriptions)
- All conditions (with human-readable descriptions)
- Human-readable summary

```python
exported = trigger.export_as_dict()

# Structure:
{
    "triggerId": 1,
    "title": "Daily Morning Run",
    "triggerEvents": [...],  # Each event with export_as_dict()
    "triggerConditions": [...],
    "humanReadable": "'Daily Morning Run' | Events: Schedule: Custom schedule"  # String summary
}
```

### DomoTriggerEvent_Schedule.export_as_dict()

Returns schedule event details with:
- Event type
- Human-readable description (shows cron expression for custom schedules)
- Schedule ID (if present)
- Full schedule details using DomoSchedule.export_as_dict()

```python
exported = schedule_event.export_as_dict()

# Structure:
{
    "type": "SCHEDULE",
    "humanReadable": "Schedule: 0 0 9 * * * *",  # Shows cron expression
    "scheduleId": "schedule-1",
    "schedule": {
        "frequency": "CUSTOM_CRON",
        "scheduleType": "CRON",
        "interval": 1,
        "hour": 9,
        "minute": 0,
        "timezone": "America/New_York",
        "expression": "0 0 9 * * * *",
        ...
    }
}
```

### DomoTriggerEvent_DatasetUpdated.export_as_dict()

Returns dataset event details with:
- Event type
- Human-readable description
- Dataset ID
- Trigger on data changed flag

```python
exported = dataset_event.export_as_dict()

# Structure:
{
    "type": "DATASET_UPDATED",
    "humanReadable": "Dataset abc-123 updated (when data changes)",
    "datasetId": "abc-123",
    "triggerOnDataChanged": true
}
```

### DomoTriggerCondition.export_as_dict()

Returns condition details with:
- Condition type
- Parameters
- Human-readable description

```python
exported = condition.export_as_dict()

# Structure:
{
    "type": "DATASET_ROW_COUNT",
    "parameters": {
        "operator": "GREATER_THAN",
        "threshold": 1000
    },
    "humanReadable": "Condition: DATASET_ROW_COUNT"
}
```

## Usage Examples

### Example 1: Export Full Trigger Configuration

```python
import json
from domolibrary2.classes.DomoDataflow import DomoDataflow

# Get dataflow
dataflow = await DomoDataflow.get_by_id(auth=auth, dataflow_id="df-123")

if dataflow.TriggerSettings:
    # Export as comprehensive dictionary
    exported = dataflow.TriggerSettings.export_as_dict()

    # Save to JSON file
    with open("trigger_config.json", "w") as f:
        json.dump(exported, f, indent=2)

    # Display summary
    print(exported["summary"])
    print(f"\nStats: {exported['stats']}")
```

### Example 2: Compare to_dict() vs export_as_dict()

```python
# to_dict() - Minimal, for API submission
minimal = dataflow.TriggerSettings.to_dict()
print("Minimal (to_dict):", json.dumps(minimal, indent=2))

# export_as_dict() - Comprehensive, human-readable
detailed = dataflow.TriggerSettings.export_as_dict()
print("Detailed (export_as_dict):", json.dumps(detailed, indent=2))
```

Output comparison:

```json
// to_dict() - Minimal
{
  "triggers": [
    {
      "triggerId": 1,
      "title": "Daily Run",
      "triggerEvents": [
        {
          "type": "SCHEDULE",
          "id": "schedule-1",
          "schedule": { ... }
        }
      ],
      "triggerConditions": []
    }
  ],
  "zoneId": "UTC",
  "locale": "en_US"
}

// export_as_dict() - Comprehensive
{
  "triggers": [
    {
      "triggerId": 1,
      "title": "Daily Run",
      "triggerEvents": [
        {
          "type": "SCHEDULE",
          "humanReadable": "Schedule: Every 1 day(s) at 09:00",
          "scheduleId": "schedule-1",
          "schedule": {
            "frequency": "DAILY",
            "hour": 9,
            "minute": 0,
            ...
          }
        }
      ],
      "triggerConditions": [],
      "humanReadable": "'Daily Run' | Events: Schedule: Every 1 day(s) at 09:00"
    }
  ],
  "zoneId": "UTC",
  "locale": "en_US",
  "summary": "Triggers (1):\n  • 'Daily Run' | Events: ...",
  "stats": {
    "totalTriggers": 1,
    "scheduleTriggers": 1,
    "datasetTriggers": 0
  }
}
```

### Example 3: Custom Export Function

You can provide a custom export function to override the default behavior:

```python
def custom_export(trigger_settings):
    """Custom export with additional fields"""
    default = trigger_settings.export_as_dict()

    # Add custom fields
    default["customField"] = "customValue"
    default["exportedAt"] = datetime.now().isoformat()

    return default

# Use custom export
exported = dataflow.TriggerSettings.export_as_dict(override_fn=custom_export)
```

### Example 4: Export Individual Triggers

```python
# Export specific trigger
trigger = dataflow.TriggerSettings.get_trigger_by_id(1)
trigger_export = trigger.export_as_dict()

print(f"Trigger: {trigger_export['title']}")
print(f"Description: {trigger_export['humanReadable']}")

# Export events
for event_dict in trigger_export["triggerEvents"]:
    print(f"  Event: {event_dict['humanReadable']}")

    if event_dict["type"] == "SCHEDULE":
        schedule = event_dict["schedule"]
        print(f"    Frequency: {schedule['frequency']}")
        print(f"    Expression: {schedule.get('expression', 'N/A')}")
```

### Example 5: Generate Documentation

```python
def generate_trigger_documentation(dataflow):
    """Generate human-readable trigger documentation"""

    if not dataflow.TriggerSettings:
        return "No triggers configured (manual execution only)"

    exported = dataflow.TriggerSettings.export_as_dict()

    doc = []
    doc.append(f"# Dataflow: {dataflow.name}")
    doc.append(f"ID: {dataflow.id}")
    doc.append("")
    doc.append("## Trigger Configuration")
    doc.append(f"Timezone: {exported['zoneId']}")
    doc.append(f"Total Triggers: {exported['stats']['totalTriggers']}")
    doc.append("")

    for trigger_dict in exported["triggers"]:
        doc.append(f"### Trigger {trigger_dict['triggerId']}: {trigger_dict['title']}")
        doc.append(f"**Description**: {trigger_dict['humanReadable']}")
        doc.append("")

        doc.append("**Events**:")
        for event in trigger_dict["triggerEvents"]:
            doc.append(f"- {event['humanReadable']}")

            if event["type"] == "SCHEDULE" and "schedule" in event:
                schedule = event["schedule"]
                doc.append(f"  - Frequency: {schedule['frequency']}")
                if schedule.get('expression'):
                    doc.append(f"  - Expression: `{schedule['expression']}`")

        doc.append("")

    return "\n".join(doc)

# Generate and print
documentation = generate_trigger_documentation(dataflow)
print(documentation)
```

## Comparison: to_dict() vs export_as_dict()

| Feature | to_dict() | export_as_dict() |
|---------|-----------|------------------|
| **Purpose** | API submission | Human-readable export |
| **Size** | Minimal | Comprehensive |
| **Human-readable** | ❌ No | ✅ Yes |
| **Statistics** | ❌ No | ✅ Yes |
| **Schedule details** | Minimal | Full (via DomoSchedule) |
| **Descriptions** | ❌ No | ✅ Yes |
| **Use case** | Update API | Documentation, analysis |

## Benefits

1. **Consistency**: Uses DomoSchedule.export_as_dict() for schedules
2. **Readability**: Includes human-readable descriptions
3. **Completeness**: Includes statistics and summaries
4. **Flexibility**: Supports custom export functions
5. **Documentation**: Perfect for generating reports

## Integration with DomoSchedule

The schedule event's `export_as_dict()` calls `DomoSchedule.export_as_dict()`:

```python
# DomoTriggerEvent_Schedule.export_as_dict()
if self.schedule:
    result["schedule"] = self.schedule.export_as_dict()  # Uses DomoSchedule
```

This ensures:
- ✅ Consistent schedule format
- ✅ All schedule properties included
- ✅ Same behavior as Stream schedules
- ✅ Automatic updates when DomoSchedule changes

## See Also

- [DomoSchedule Documentation](schedule-guide.md)
- [Trigger System Guide](trigger-system-guide.md)
- [Trigger-Schedule Relationship](trigger-schedule-relationship.md)
