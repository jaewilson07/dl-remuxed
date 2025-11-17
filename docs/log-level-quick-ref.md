> Last updated: 2025-11-17

# Logging & Colored Logger Quick Reference

domolibrary2 uses an async, colored logger by default. This guide shows how
to use it in scripts and notebooks and how to control log levels.

## 1. Basic Colored Logging

Importing `domolibrary2` automatically configures colored logging globally.

```python
import domolibrary2  # initializes colored logger

from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()

await logger.debug("Debug details")        # Cyan
await logger.info("Dataset uploaded")      # Green
await logger.warning("Rate limit warning") # Yellow
await logger.error("Upload failed")        # Bold red
```

Existing code that already uses `logger.info()`, `logger.warning()`, etc.
will automatically produce colored output—no changes required.

### Optional: Override Color per Message

```python
await logger.info("Custom color", color="magenta")
```

## 2. Controlling Log Levels (Everywhere)

Use `set_level` to control verbosity:

```python
from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()

logger.set_level("DEBUG")   # show everything
logger.set_level("INFO")    # default
logger.set_level("WARNING") # hide INFO/DEBUG
logger.set_level("ERROR")   # only errors/critical
```

Check the current level:

```python
print(logger.get_level())  # e.g. "INFO"
```

### Available Levels

From most verbose to least:

| Level    | Value | Shows                                      |
|----------|-------|--------------------------------------------|
| DEBUG    | 10    | All messages                               |
| INFO     | 20    | Info, warnings, errors (default)           |
| WARNING  | 30    | Only warnings and errors                   |
| ERROR    | 40    | Only errors and critical                   |
| CRITICAL | 50    | Only critical failures                     |

## 3. Jupyter Notebook Patterns

Start your notebook with a cell that configures logging:

```python
from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()
logger.set_level("WARNING")  # recommended for notebooks

print(f"Current log level: {logger.get_level()}")
```

Then run your normal Domo code in later cells. Only warnings and errors
will appear, keeping your notebook output clean:

```python
import os
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoDataset as dmds

auth = dmda.DomoTokenAuth(
		domo_instance=os.environ["DOMO_INSTANCE"],
		domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

dataset = await dmds.DomoDataset.get_by_id(
		auth=auth,
		dataset_id="abc123",
)

print(f"Got dataset: {dataset.name}")
```

When debugging a specific section, temporarily raise the level:

```python
logger.set_level("DEBUG")
await dataset.refresh(is_suppress_no_config=True)
logger.set_level("WARNING")  # restore quiet mode
```

## 4. Common Recipes

### Quiet Batch Processing

```python
logger = get_colored_logger()
logger.set_level("WARNING")

for ds_id in dataset_ids:
		ds = await dmds.DomoDataset.get_by_id(auth=auth, dataset_id=ds_id)
		await ds.refresh(is_suppress_no_config=True)
```

### Verbose Debugging

```python
logger = get_colored_logger()
logger.set_level("DEBUG")

dataset = await dmds.DomoDataset.get_by_id(auth=auth, dataset_id="problem-dataset")
```

### Production vs. Development Toggle

```python
logger = get_colored_logger()

# Production
logger.set_level("WARNING")

# Development
# logger.set_level("DEBUG")
```

## 5. Notes

- The `@log_call` decorator logs at INFO level; set `WARNING` or higher
	to hide those messages.
- Colors appear in terminals that support ANSI escape codes (VS Code
	terminal, Windows Terminal, iTerm2, most CI consoles).
- In environments where colors are undesirable, consider using the
	`NO_COLOR` environment variable.
logger.set_level('WARNING')

# Your code runs quietly now
auth = dmda.DomoTokenAuth(...)
# No INFO logs! Only warnings/errors show
\\\

---

**💡 Pro Tip**: Start with WARNING level, switch to DEBUG only when troubleshooting!
