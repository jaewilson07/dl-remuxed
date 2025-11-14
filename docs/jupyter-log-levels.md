# Controlling Log Levels in Jupyter Notebooks

This guide shows how to control logging verbosity in your Jupyter notebooks.

## Quick Start

### Silence Most Logs (Show Only Warnings and Errors)

```python
from domolibrary2.utils.logging import get_colored_logger

# Get the logger and set to WARNING level
logger = get_colored_logger()
logger.set_level('WARNING')

# Now only WARNING, ERROR, and CRITICAL messages will show
# INFO and DEBUG messages are suppressed
```

### Show Only Errors

```python
from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()
logger.set_level('ERROR')

# Now only ERROR and CRITICAL messages will show
```

### Show Everything (Debug Mode)

```python
from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()
logger.set_level('DEBUG')

# Shows all messages including DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Complete Example for Notebooks

```python
# Cell 1: Setup and configure logging
from domolibrary2.utils.logging import get_colored_logger
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoDataset as dmds

# Set log level to WARNING to reduce noise
logger = get_colored_logger()
logger.set_level('WARNING')  # Only show warnings and errors

print(f"Current log level: {logger.get_level()}")
```

```python
# Cell 2: Your actual work
# Now only warnings and errors will be logged

auth = dmda.DomoTokenAuth(
    domo_instance="your-instance",
    domo_access_token="your-token"
)

# This will run quietly - only warnings/errors will show
dataset = await dmds.DomoDataset.get_by_id(
    auth=auth,
    dataset_id="abc123"
)

print(f"Got dataset: {dataset.name}")
```

```python
# Cell 3: If you need to debug something specific, temporarily enable DEBUG
logger.set_level('DEBUG')

# Now this will show all debug output
await dataset.refresh(is_suppress_no_config=True)

# Set it back when done
logger.set_level('WARNING')
```

## Available Log Levels

From most verbose to least:

| Level    | Value | What Shows                                    |
|----------|-------|-----------------------------------------------|
| DEBUG    | 10    | Everything (debug, info, warnings, errors)    |
| INFO     | 20    | Info, warnings, errors (default)              |
| WARNING  | 30    | Only warnings and errors                      |
| ERROR    | 40    | Only errors and critical                      |
| CRITICAL | 50    | Only critical failures                        |

## Common Patterns

### Quiet Batch Processing

```python
# For batch processing where you don't want noise
logger = get_colored_logger()
logger.set_level('WARNING')

# Process many items quietly
for ds_id in dataset_ids:
    ds = await dmds.DomoDataset.get_by_id(auth=auth, dataset_id=ds_id)
    await ds.refresh(is_suppress_no_config=True)
    # Only warnings/errors will show
```

### Verbose Debugging

```python
# When something isn't working and you need details
logger = get_colored_logger()
logger.set_level('DEBUG')

# See everything
dataset = await dmds.DomoDataset.get_by_id(auth=auth, dataset_id="problem-dataset")
```

### Production Script

```python
# At the top of your notebook/script
from domolibrary2.utils.logging import get_colored_logger

# Production: only show warnings and errors
logger = get_colored_logger()
logger.set_level('WARNING')

# Development: show everything
# logger.set_level('DEBUG')
```

## Checking Current Level

```python
logger = get_colored_logger()
print(f"Current log level: {logger.get_level()}")
# Output: Current log level: INFO
```

## Tips

1. **Start Quiet**: Begin with `WARNING` level and only increase verbosity when debugging
2. **Cell-Specific**: You can change the level in any cell - it affects all subsequent logging
3. **Persistent**: The level persists across cells until you change it again
4. **Notebook Start**: Put your preferred level in the first cell of your notebook

## Common Issues

### Too Much Noise

```python
# If you see too many INFO messages
logger.set_level('WARNING')
```

### Missing Debug Info

```python
# If you need more detail
logger.set_level('DEBUG')  # or 'INFO'
```

### @log_call Decorator Logs

Note: The `@log_call` decorator in route functions logs at INFO level. To hide these:

```python
logger.set_level('WARNING')  # Will hide @log_call INFO messages
```

## Example: Clean Notebook Output

```python
# ========================================
# CONFIGURATION
# ========================================

from domolibrary2.utils.logging import get_colored_logger
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoDataset as dmds

# Suppress routine logging
logger = get_colored_logger()
logger.set_level('WARNING')

# ========================================
# AUTHENTICATION
# ========================================

auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"]
)

# ========================================
# MAIN LOGIC
# ========================================

# No INFO logs cluttering your output!
datasets = []
for ds_id in my_dataset_ids:
    ds = await dmds.DomoDataset.get_by_id(auth=auth, dataset_id=ds_id)
    await ds.refresh(is_suppress_no_config=True)
    datasets.append(ds)

print(f"Processed {len(datasets)} datasets")
# Only warnings/errors were shown above
```

---

**Default Level**: INFO
**Recommended for Notebooks**: WARNING
**For Debugging**: DEBUG
