# DomoCard.Datasets Manager

## Overview

The `DomoCard.Datasets` property provides a manager interface for accessing all datasets associated with a card. This follows the same pattern as other manager classes in the library (e.g., `DomoUsers`, `DomoStreams`).

## Architecture

```
DomoCard
└── Datasets: CardDatasets
    └── get() → list[DomoDataset]
```

The `CardDatasets` manager is automatically initialized when a `DomoCard` is created, with a parent reference to the card and shared authentication.

## Usage

### Basic Usage

```python
import domolibrary2.classes.DomoCard as dmdc

# Get a card
card = await dmdc.DomoCard.get_by_id(
    auth=auth,
    card_id="card-123",
)

# Access datasets through the Datasets manager
datasets = await card.Datasets.get()

print(f"Card '{card.title}' uses {len(datasets)} dataset(s)")

for dataset in datasets:
    print(f"  - {dataset.name} (ID: {dataset.id})")
```

### With Session Reuse

```python
import httpx

async with httpx.AsyncClient() as session:
    # Get card
    card = await dmdc.DomoCard.get_by_id(
        auth=auth,
        card_id="card-123",
        session=session,
    )

    # Get datasets (reuses session)
    datasets = await card.Datasets.get(session=session)
```

### Accessing Dataset Properties

```python
# Get datasets
datasets = await card.Datasets.get()

for dataset in datasets:
    # All DomoDataset properties available
    print(f"Dataset: {dataset.name}")
    print(f"  Rows: {dataset.rows}")
    print(f"  Columns: {dataset.columns}")
    print(f"  Owner: {dataset.owner.display_name if dataset.owner else 'N/A'}")

    # Access dataset schema
    schema = await dataset.get_schema()
    print(f"  Schema columns: {len(schema.columns)}")
```

## CardDatasets Class

CardDatasets inherits from `DomoManager`, following the established pattern for entity collection managers.

### Class Definition

```python
@dataclass
class CardDatasets(DomoManager):
    """Manager for datasets associated with a DomoCard"""

    parent: DomoCard
    auth: DomoAuth = field(repr=False)
```

### Properties

- `parent: DomoCard` - Reference to the parent card
- `auth: DomoAuth` - Authentication (inherited from parent, not shown in repr)

### Methods

#### get()

Retrieves all datasets associated with the card.

```python
async def get(
    self,
    debug_api: bool = False,
    session: httpx.AsyncClient | None = None,
) -> list[DomoDataset]:
    """Get all datasets associated with this card"""
```

**Parameters:**
- `debug_api: bool` - Enable API debugging output
- `session: httpx.AsyncClient | None` - Optional session for request reuse

**Returns:**
- `list[DomoDataset]` - List of dataset objects associated with the card

**Behavior:**
1. Checks card's `datasources` in raw metadata
2. If not present, fetches card metadata with datasources
3. Extracts dataset IDs from datasources
4. Fetches all datasets concurrently (n=60)
5. Updates parent card's `datasets` field
6. Returns list of `DomoDataset` instances

## Examples

### Example 1: Analyze Card Dependencies

```python
async def analyze_card_dependencies(card_id: str, auth):
    """Analyze what datasets a card depends on"""

    card = await dmdc.DomoCard.get_by_id(auth=auth, card_id=card_id)
    datasets = await card.Datasets.get()

    print(f"\nCard: {card.title}")
    print(f"Type: {card.chart_type}")
    print(f"Datasets: {len(datasets)}\n")

    for i, dataset in enumerate(datasets, 1):
        print(f"{i}. {dataset.name}")
        print(f"   ID: {dataset.id}")
        print(f"   Rows: {dataset.rows:,}")
        print(f"   Last Updated: {dataset.last_updated}")
```

### Example 2: Audit Card Data Sources

```python
async def audit_card_datasources(cards: list[dmdc.DomoCard]):
    """Audit all datasets used across multiple cards"""

    all_datasets = {}

    for card in cards:
        datasets = await card.Datasets.get()

        for dataset in datasets:
            if dataset.id not in all_datasets:
                all_datasets[dataset.id] = {
                    "dataset": dataset,
                    "cards": []
                }
            all_datasets[dataset.id]["cards"].append(card)

    # Report
    print(f"Total unique datasets: {len(all_datasets)}")
    print(f"\nDatasets used by multiple cards:")

    for ds_id, info in all_datasets.items():
        if len(info["cards"]) > 1:
            print(f"  {info['dataset'].name}")
            print(f"    Used by {len(info['cards'])} cards:")
            for card in info["cards"]:
                print(f"      - {card.title}")
```

### Example 3: Refresh Card Data

```python
async def refresh_card_data(card: dmdc.DomoCard):
    """Trigger refresh of all datasets used by a card"""

    datasets = await card.Datasets.get()

    print(f"Refreshing {len(datasets)} dataset(s) for card '{card.title}'")

    for dataset in datasets:
        if dataset.dataflow_id:
            # Trigger dataflow execution
            print(f"  Triggering dataflow for {dataset.name}...")
            # await dataset.execute_dataflow()
        else:
            print(f"  {dataset.name} - No dataflow to execute")
```

### Example 4: Compare Card Datasets

```python
async def compare_card_datasets(card1: dmdc.DomoCard, card2: dmdc.DomoCard):
    """Compare datasets used by two cards"""

    datasets1 = await card1.Datasets.get()
    datasets2 = await card2.Datasets.get()

    ids1 = {ds.id for ds in datasets1}
    ids2 = {ds.id for ds in datasets2}

    shared = ids1 & ids2
    only_card1 = ids1 - ids2
    only_card2 = ids2 - ids1

    print(f"Card 1: {card1.title}")
    print(f"  Datasets: {len(datasets1)}")

    print(f"\nCard 2: {card2.title}")
    print(f"  Datasets: {len(datasets2)}")

    print(f"\nShared datasets: {len(shared)}")
    print(f"Only in Card 1: {len(only_card1)}")
    print(f"Only in Card 2: {len(only_card2)}")
```

## Integration with Existing Features

### With Lineage

```python
# Get card with lineage
card = await dmdc.DomoCard.get_by_id(auth=auth, card_id="card-123")

# Get datasets
datasets = await card.Datasets.get()

# Check lineage for each dataset
for dataset in datasets:
    downstream = await card.Lineage.get_downstream(entity=dataset)
    print(f"{dataset.name} is used by {len(downstream)} other entities")
```

### With Card Properties

```python
card = await dmdc.DomoCard.get_by_id(auth=auth, card_id="card-123")

# Access both card properties and datasets
print(f"Card: {card.title}")
print(f"Type: {card.type}")
print(f"Chart Type: {card.chart_type}")
print(f"Primary Dataset: {card.dataset_id}")

# Get all datasets (might include more than primary)
datasets = await card.Datasets.get()
print(f"Total Datasets: {len(datasets)}")
```

## Implementation Notes

### Datasources Field

The manager uses the `datasources` field from the card's raw metadata. This field is populated when:
- Card is fetched with `optional_parts="datasources"`
- Card metadata is refreshed

If `datasources` is not present, the manager automatically fetches it.

### Dataset Types

The manager returns proper `DomoDataset` instances, which may be:
- `DomoDataset` - Standard dataset
- `FederatedDomoDataset` - Federated dataset
- `DomoPublishDataset` - Published dataset

The correct type is automatically determined by `DomoDataset.get_by_id()`.

### Concurrency

The manager fetches datasets concurrently with a limit of 60 simultaneous requests, matching the pattern used throughout the library.

### Caching

The manager updates the parent card's `datasets` field, so subsequent calls to `card.datasets` will have the loaded datasets without additional API calls (unless you call `card.Datasets.get()` again).

## Comparison with Other Managers

| Manager | Parent | Returns | Pattern |
|---------|--------|---------|---------|
| `DomoUsers` | Global | `list[DomoUser]` | `users = await DomoUsers(auth).get()` |
| `DomoStreams` | DomoDataset | `list[DomoStream]` | `streams = await dataset.Streams.get()` |
| `CardDatasets` | DomoCard | `list[DomoDataset]` | `datasets = await card.Datasets.get()` |

All follow the same manager pattern with:
- Inherit from `DomoManager` base class
- Dataclass structure
- `get()` method implementation
- Parent reference (where applicable)
- Shared authentication
- `auth` field with `repr=False`

## Error Handling

```python
from domolibrary2.client.exceptions import DomoError

try:
    datasets = await card.Datasets.get()
except DomoError as e:
    print(f"Error fetching datasets: {e}")
    # Handle error
```

## See Also

- [DomoCard Documentation](../classes/DomoCard.md)
- [DomoDataset Documentation](../classes/DomoDataset.md)
- [Manager Pattern Guide](../patterns/manager-pattern.md)
