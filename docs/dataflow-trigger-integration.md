# DomoDataflow TriggerSettings Integration Guide

## Overview

`DomoDataflow` now includes integrated support for `DomoTriggerSettings`, allowing you to access and manage complex trigger configurations directly from dataflow objects.

## What Changed

### Added Import
```python
from ..subentity.trigger import DomoTriggerSettings
```

### Added Field
```python
@dataclass
class DomoDataflow(DomoEntity_w_Lineage):
    # ... existing fields ...
    TriggerSettings: DomoTriggerSettings = None  # trigger configuration for dataflow execution
```

### Updated `__post_init__`
```python
def __post_init__(self):
    # ... existing initialization ...

    # Initialize TriggerSettings if present in raw data
    if self.raw.get("triggerSettings"):
        self.TriggerSettings = DomoTriggerSettings.from_dict(
            self.raw["triggerSettings"], parent=self
        )
```

### Updated `from_dict`
```python
@classmethod
def from_dict(cls, obj, auth, version_id=None, version_number=None):
    domo_dataflow = cls(
        # ... existing fields ...
        TriggerSettings=None,  # Will be initialized in __post_init__
    )
```

## Usage Examples

### Basic Access

```python
import asyncio
from domolibrary2.classes.DomoDataflow import DomoDataflow
from domolibrary2.client.auth import DomoTokenAuth

async def check_dataflow_triggers():
    auth = DomoTokenAuth(
        domo_instance="your-instance",
        domo_access_token="your-token"
    )

    # Get a dataflow
    dataflow = await DomoDataflow.get_by_id(
        auth=auth,
        dataflow_id="your-dataflow-id"
    )

    # Check if dataflow has triggers
    if dataflow.TriggerSettings:
        print(f"Dataflow '{dataflow.name}' has {len(dataflow.TriggerSettings)} triggers")
        print(dataflow.TriggerSettings.get_human_readable_summary())
    else:
        print(f"Dataflow '{dataflow.name}' has no trigger settings (manual execution)")

asyncio.run(check_dataflow_triggers())
```

### Query Trigger Types

```python
async def analyze_triggers(dataflow: DomoDataflow):
    if not dataflow.TriggerSettings:
        print("No triggers configured")
        return

    # Get schedule-based triggers
    schedule_triggers = dataflow.TriggerSettings.get_schedule_triggers()
    if schedule_triggers:
        print(f"\n📅 Schedule-based triggers ({len(schedule_triggers)}):")
        for trigger in schedule_triggers:
            print(f"  • {trigger.title}")
            for event in trigger.get_schedule_events():
                if event.schedule:
                    print(f"    Schedule: {event.schedule.get_human_readable_schedule()}")

    # Get dataset-based triggers
    dataset_triggers = dataflow.TriggerSettings.get_dataset_triggers()
    if dataset_triggers:
        print(f"\n📊 Dataset-based triggers ({len(dataset_triggers)}):")
        for trigger in dataset_triggers:
            print(f"  • {trigger.title}")
            for event in trigger.get_dataset_events():
                change_text = "when data changes" if event.trigger_on_data_changed else "on every update"
                print(f"    Dataset: {event.dataset_id} ({change_text})")
```

### Find Dependencies

```python
async def find_dataflows_triggered_by_dataset(auth, dataset_id: str):
    """Find all dataflows triggered by a specific dataset"""
    from domolibrary2.classes.DomoDataflow import DomoDataflows

    # Get all dataflows
    dataflows = await DomoDataflows(auth=auth).get()

    triggered_dataflows = []
    for dataflow in dataflows:
        if not dataflow.TriggerSettings:
            continue

        # Check each trigger
        for trigger in dataflow.TriggerSettings.get_dataset_triggers():
            for event in trigger.get_dataset_events():
                if event.dataset_id == dataset_id:
                    triggered_dataflows.append({
                        'dataflow': dataflow,
                        'trigger': trigger,
                        'on_change': event.trigger_on_data_changed
                    })

    # Display results
    print(f"Dataflows triggered by dataset {dataset_id}:")
    for item in triggered_dataflows:
        print(f"  • {item['dataflow'].name}")
        print(f"    Trigger: {item['trigger'].title}")
        print(f"    Condition: {'Data changed' if item['on_change'] else 'Every update'}")

    return triggered_dataflows
```

### Analyze All Dataflows

```python
async def analyze_all_dataflow_triggers(auth):
    """Generate statistics about dataflow triggers"""
    from domolibrary2.classes.DomoDataflow import DomoDataflows

    dataflows = await DomoDataflows(auth=auth).get()

    stats = {
        'total': len(dataflows),
        'with_triggers': 0,
        'manual_only': 0,
        'with_schedules': 0,
        'with_dataset_triggers': 0,
        'multi_trigger': 0
    }

    for df in dataflows:
        if df.TriggerSettings:
            stats['with_triggers'] += 1

            if len(df.TriggerSettings) > 1:
                stats['multi_trigger'] += 1

            if df.TriggerSettings.has_any_schedules():
                stats['with_schedules'] += 1

            if df.TriggerSettings.has_any_dataset_triggers():
                stats['with_dataset_triggers'] += 1
        else:
            stats['manual_only'] += 1

    # Display statistics
    print("Dataflow Trigger Statistics:")
    print(f"  Total dataflows: {stats['total']}")
    print(f"  With triggers: {stats['with_triggers']} ({stats['with_triggers']/stats['total']*100:.1f}%)")
    print(f"  Manual only: {stats['manual_only']} ({stats['manual_only']/stats['total']*100:.1f}%)")
    print(f"  With schedules: {stats['with_schedules']}")
    print(f"  With dataset triggers: {stats['with_dataset_triggers']}")
    print(f"  Multiple triggers: {stats['multi_trigger']}")

    return stats
```

### Filter Dataflows by Trigger Configuration

```python
async def find_daily_dataflows(auth):
    """Find all dataflows that run daily"""
    from domolibrary2.classes.DomoDataflow import DomoDataflows
    from domolibrary2.classes.subentity.schedule import ScheduleFrequencyEnum

    dataflows = await DomoDataflows(auth=auth).get()
    daily_dataflows = []

    for df in dataflows:
        if not df.TriggerSettings:
            continue

        for trigger in df.TriggerSettings.get_schedule_triggers():
            for event in trigger.get_schedule_events():
                if event.schedule and event.schedule.frequency == ScheduleFrequencyEnum.DAILY:
                    daily_dataflows.append({
                        'dataflow': df,
                        'trigger': trigger,
                        'schedule': event.schedule
                    })
                    break

    # Display results
    print(f"Found {len(daily_dataflows)} dataflows with daily schedules:")
    for item in daily_dataflows:
        df = item['dataflow']
        schedule = item['schedule']
        print(f"  • {df.name}")
        print(f"    Schedule: {schedule.get_human_readable_schedule()}")

    return daily_dataflows
```

### Pretty Print Trigger Information

```python
def display_dataflow_info(dataflow: DomoDataflow):
    """Display comprehensive dataflow information including triggers"""
    print("=" * 80)
    print("DATAFLOW INFORMATION")
    print("=" * 80)
    print(f"Name: {dataflow.name}")
    print(f"ID: {dataflow.id}")
    print(f"Owner: {dataflow.owner}")
    print(f"Description: {dataflow.description or 'N/A'}")
    print(f"URL: {dataflow.display_url}")

    if dataflow.TriggerSettings:
        print("\n" + "=" * 80)
        print("TRIGGER CONFIGURATION")
        print("=" * 80)
        print(f"Timezone: {dataflow.TriggerSettings.zone_id}")
        print(f"Locale: {dataflow.TriggerSettings.locale}")
        print(f"Total Triggers: {len(dataflow.TriggerSettings)}")
        print()
        print(dataflow.TriggerSettings.get_human_readable_summary())
    else:
        print("\n" + "=" * 80)
        print("TRIGGER CONFIGURATION")
        print("=" * 80)
        print("No triggers configured (manual execution only)")
```

## Integration Patterns

### Pattern 1: Health Check

Check if critical dataflows have proper trigger configurations:

```python
async def check_dataflow_health(auth, critical_dataflow_ids: list[str]):
    """Verify critical dataflows have proper triggers configured"""
    issues = []

    for df_id in critical_dataflow_ids:
        df = await DomoDataflow.get_by_id(auth=auth, dataflow_id=df_id)

        if not df.TriggerSettings:
            issues.append(f"⚠️  {df.name}: No triggers configured")
        elif len(df.TriggerSettings) == 0:
            issues.append(f"⚠️  {df.name}: Empty trigger settings")
        else:
            print(f"✅ {df.name}: {len(df.TriggerSettings)} trigger(s) configured")

    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(issue)

    return len(issues) == 0
```

### Pattern 2: Dependency Mapping

Build a dependency graph based on dataset triggers:

```python
async def build_dependency_graph(auth):
    """Build a graph of dataflow dependencies based on dataset triggers"""
    from domolibrary2.classes.DomoDataflow import DomoDataflows

    dataflows = await DomoDataflows(auth=auth).get()
    dependency_graph = {}

    for df in dataflows:
        if not df.TriggerSettings:
            continue

        dependencies = []
        for trigger in df.TriggerSettings.get_dataset_triggers():
            for event in trigger.get_dataset_events():
                dependencies.append(event.dataset_id)

        if dependencies:
            dependency_graph[df.id] = {
                'name': df.name,
                'depends_on': dependencies
            }

    return dependency_graph
```

### Pattern 3: Execution Schedule Report

Generate a report of when dataflows are scheduled to run:

```python
async def generate_schedule_report(auth):
    """Generate a report of all scheduled dataflow executions"""
    from domolibrary2.classes.DomoDataflow import DomoDataflows
    from domolibrary2.classes.subentity.schedule import ScheduleFrequencyEnum

    dataflows = await DomoDataflows(auth=auth).get()
    schedule_report = {
        'DAILY': [],
        'WEEKLY': [],
        'MONTHLY': [],
        'HOURLY': [],
        'CUSTOM': []
    }

    for df in dataflows:
        if not df.TriggerSettings:
            continue

        for trigger in df.TriggerSettings.get_schedule_triggers():
            for event in trigger.get_schedule_events():
                if event.schedule:
                    freq = event.schedule.frequency.value
                    schedule_report.get(freq, schedule_report['CUSTOM']).append({
                        'dataflow': df.name,
                        'trigger': trigger.title,
                        'schedule': event.schedule.get_human_readable_schedule()
                    })

    # Print report
    for frequency, items in schedule_report.items():
        if items:
            print(f"\n{frequency} Schedules ({len(items)}):")
            for item in items:
                print(f"  • {item['dataflow']}")
                print(f"    {item['schedule']}")

    return schedule_report
```

## Benefits

1. **Direct Access**: No need to manually parse `raw` dict
2. **Type Safety**: Strongly-typed `DomoTriggerSettings` object
3. **Query Methods**: Built-in filtering and search
4. **Human-Readable**: Easy-to-understand trigger descriptions
5. **Consistent API**: Same pattern as other subentities (History, Lineage)

## Backward Compatibility

- Dataflows without trigger settings work as before (`TriggerSettings` is `None`)
- All existing code continues to work unchanged
- No breaking changes to existing API

## See Also

- [Trigger System Guide](trigger-system-guide.md) - Comprehensive trigger documentation
- [Trigger Quick Reference](trigger-quick-reference.md) - API cheatsheet
- [Trigger Architecture](trigger-architecture-visual.md) - Visual diagrams
