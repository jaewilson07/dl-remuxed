# Domo Trigger System Architecture

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     DomoDataflow                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  TriggerSettings                           │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │               Trigger 1: "Daily Run"                 │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │  Event: SCHEDULE                             │    │  │  │
│  │  │  │  - Every day at 9:00 AM                      │    │  │  │
│  │  │  │  - Uses DomoCronSchedule internally          │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │           Trigger 2: "On Data Update"            │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │  Event: DATASET_UPDATED                      │    │  │  │
│  │  │  │  - Dataset ID: abc-123                       │    │  │  │
│  │  │  │  - Trigger on data changed: true             │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │         Trigger 3: "Weekend Batch"               │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │  Event: SCHEDULE                             │    │  │  │
│  │  │  │  - Every Saturday at 2:00 AM                 │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │  Condition: DATASET_ROW_COUNT                │    │  │  │
│  │  │  │  - Threshold: > 1000 rows                    │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  Timezone: America/New_York                               │  │
│  │  Locale: en_US                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Class Relationships

```
                    ┌─────────────┐
                    │  DomoBase   │
                    └──────┬──────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
    ┌──────▼──────┐              ┌────────▼────────┐
    │DomoTrigger  │              │DomoTrigger     │
    │Settings     │              │Event_Base      │
    └──────┬──────┘              └────────┬────────┘
           │                              │
           │ contains multiple      ┌─────┴─────┬──────────────┐
           │                        │           │              │
    ┌──────▼──────┐         ┌───────▼────┐ ┌───▼──────┐ ┌────▼───────┐
    │DomoTrigger  │         │Schedule    │ │Dataset   │ │Generic     │
    │(individual) │         │Event       │ │Event     │ │Event       │
    └──────┬──────┘         └────────────┘ └──────────┘ └────────────┘
           │                      │
           │ contains multiple    │ contains
           │                      │
    ┌──────▼──────────┐    ┌──────▼────────┐
    │TriggerEvent     │    │DomoSchedule   │
    │(multiple types) │    │_Base          │
    └─────────────────┘    │(cron parser)  │
    ┌─────────────────┐    └───────────────┘
    │TriggerCondition │
    │(optional)       │
    └─────────────────┘
```

## Data Flow

```
┌──────────────────┐
│  API Response    │
│  {               │
│   triggerSettings│
│   ...            │
│  }               │
└────────┬─────────┘
         │
         │ DomoTriggerSettings.from_dict()
         ▼
┌────────────────────┐
│ DomoTriggerSettings│
│ - triggers[]       │
│ - zone_id          │
│ - locale           │
└────────┬───────────┘
         │
         │ for each trigger
         ▼
┌─────────────────┐
│  DomoTrigger    │
│  - id           │
│  - title        │
│  - events[]     │
│  - conditions[] │
└────────┬────────┘
         │
         │ for each event
         ▼
┌─────────────────────┐
│DomoTriggerEvent_Base│ ◄─── Factory determines type
└────────┬────────────┘
         │
    ┌────┴────┬─────────────┐
    │         │             │
    ▼         ▼             ▼
┌────────┐┌─────────┐┌──────────┐
│Schedule││Dataset  ││Generic   │
│Event   ││Event    ││Event     │
└────────┘└─────────┘└──────────┘
```

## Usage Patterns

### Pattern 1: Simple Query

```
User wants to know: "What triggers does this dataflow have?"

dataflow.TriggerSettings ──→ get_human_readable_summary()
                              │
                              ▼
                         "Triggers (3):
                          • Daily Run
                          • On Data Update
                          • Weekend Batch"
```

### Pattern 2: Filter by Type

```
User wants: "Show me only schedule-based triggers"

dataflow.TriggerSettings ──→ get_schedule_triggers()
                              │
                              ▼
                         [Trigger 1, Trigger 3]
                              │
                              ▼
                         for each: get_human_readable_description()
```

### Pattern 3: Find Dataset Dependencies

```
User wants: "Which dataflows are triggered by dataset X?"

For each dataflow:
  TriggerSettings ──→ get_dataset_triggers()
                      │
                      ▼
                  Check each event.dataset_id
                      │
                      ▼
                  If matches: add to results
```

## Event Type Decision Tree

```
                    Parse trigger event
                            │
                            ▼
                    Check "type" field
                            │
            ┌───────────────┼───────────────┐
            │               │               │
       "SCHEDULE"    "DATASET_UPDATED"   Other
            │               │               │
            ▼               ▼               ▼
    ┌───────────────┐  ┌────────────┐  ┌──────────┐
    │Schedule Event │  │Dataset     │  │Generic   │
    │               │  │Event       │  │Event     │
    │- Parse cron   │  │- dataset_id│  │- type    │
    │- Create       │  │- trigger_on│  │- raw     │
    │  DomoSchedule │  │  _changed  │  └──────────┘
    └───────────────┘  └────────────┘
```

## Integration Flow

```
┌──────────────────────────────────────────────────────────┐
│                    DomoDataflow                           │
│                                                           │
│  1. Fetch from API                                        │
│     GET /v2/dataflows/{id}                                │
│                                                           │
│  2. Response includes triggerSettings                     │
│     {                                                     │
│       "id": "df-123",                                     │
│       "name": "Sales ETL",                                │
│       "triggerSettings": {...}                            │
│     }                                                     │
│                                                           │
│  3. from_dict() creates DomoDataflow                      │
│     └─→ Calls __post_init__()                            │
│         └─→ Checks for raw["triggerSettings"]            │
│             └─→ Creates DomoTriggerSettings.from_dict()  │
│                                                           │
│  4. User accesses triggers                                │
│     dataflow.TriggerSettings.triggers                     │
│                                                           │
│  5. User queries/filters                                  │
│     dataflow.TriggerSettings.get_schedule_triggers()      │
│                                                           │
│  6. User gets human-readable output                       │
│     print(dataflow.TriggerSettings)                       │
└──────────────────────────────────────────────────────────┘
```

## Comparison Matrix

```
┌─────────────────┬────────────────┬──────────────────────┐
│ Feature         │ DomoSchedule   │ DomoTriggerSettings  │
├─────────────────┼────────────────┼──────────────────────┤
│ Single schedule │       ✓        │          ✓           │
│ Multiple        │       ✗        │          ✓           │
│ Dataset trigger │       ✗        │          ✓           │
│ Conditions      │       ✗        │          ✓           │
│ Timezone        │       ✓        │          ✓           │
│ Human-readable  │       ✓        │          ✓           │
│ Used by         │ Streams        │      DataFlows       │
└─────────────────┴────────────────┴──────────────────────┘
```

## Memory Layout (Approximate)

```
DomoTriggerSettings (object)
├── triggers: list          ─┐
│   └── [ptr, ptr, ptr]      │
├── zone_id: str "UTC"        │ ~200 bytes base
├── locale: str "en_US"       │
└── raw: dict               ─┘

DomoTrigger (per trigger)    ~300 bytes each
├── trigger_id: int
├── title: str
├── trigger_events: list
└── trigger_conditions: list

DomoTriggerEvent (per event) ~150 bytes each
├── event_type: enum
└── [type-specific fields]

Total for typical dataflow with 3 triggers:
~200 + (3 × 300) + (4 × 150) = ~1,700 bytes
```

This is a lightweight, efficient structure suitable for thousands of dataflows.
