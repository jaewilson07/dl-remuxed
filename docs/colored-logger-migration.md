# Colored Logger Migration Summary

## Overview
Migrated all logger instances from `get_global_logger()` to `get_colored_logger()` to enable automatic color-coding of log messages by severity level.

## Default Color Scheme
- **DEBUG**: cyan (🔍 diagnostics)
- **INFO**: green (✅ success/info)
- **WARNING**: yellow (⚠️ warnings)
- **ERROR**: bold_red (❌ errors)
- **CRITICAL**: bold_red (🚨 critical failures)

## Files Updated

### 1. New Files Created
- `src/domolibrary2/utils/logging/colored_logger.py`
  - ColoredLogger class with automatic color application
  - get_colored_logger() singleton factory function

- `src/domolibrary2/utils/logging/__init__.py`
  - Exported ColoredLogger and get_colored_logger

### 2. Logger Instances Updated
- ✅ `src/domolibrary2/classes/DomoAccount/account_default.py`
  - Changed: `from dc_logger.client.base import get_global_logger`
  - To: `from ...utils.logging import get_colored_logger`
  - Changed: `logger = get_global_logger()`
  - To: `logger = get_colored_logger()`

- ✅ `src/domolibrary2/classes/DomoUser.py`
  - Changed: `from dc_logger.client.base import get_global_logger`
  - To: `from ..utils.logging import get_colored_logger`
  - Changed: `logger = get_global_logger()`
  - To: `logger = get_colored_logger()`

- ✅ `src/domolibrary2/utils/upload_data.py`
  - Changed: `from dc_logger.client.base import Logger, get_global_logger`
  - To: `from dc_logger.client.base import Logger` + `from ..utils.logging import get_colored_logger`
  - Changed: `logger = get_global_logger()`
  - To: `logger = get_colored_logger()`

## Usage Examples

### Basic Usage (Automatic Colors)
```python
from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()

# Messages are automatically colored by level
await logger.info("Dataset created successfully")      # Green
await logger.warning("Rate limit approaching")         # Yellow
await logger.error("Failed to upload data")            # Bold Red
await logger.debug("Request payload: {...}")           # Cyan
```

### Override Default Color
```python
# Use custom color for specific message
await logger.info("Special notification", color="magenta")
await logger.warning("Custom warning", color="blue")
```

### Custom Default Colors
```python
# Create logger with custom color scheme
logger = get_colored_logger(
    debug_color="dim_cyan",
    info_color="blue",
    warning_color="yellow",
    error_color="red",
    critical_color="bold_red"
)
```

### Available Colors
From `dc_logger.color_utils`:
- Basic: `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- Styled: `bold_red`, `dim_blue`, etc. (prefix with `bold_` or `dim_`)

## Benefits

1. **Visual Clarity**: Different log levels are instantly recognizable in console output
2. **Consistency**: Colors are applied automatically without manual colorize() calls
3. **Maintainability**: Single place to configure color scheme for entire application
4. **Backward Compatible**: Wraps dc_logger without breaking existing functionality
5. **Flexible**: Can override colors per-message or customize defaults

## Routes Note
Route functions use the `@log_call` decorator which handles its own logging. The colored logger is primarily used for:
- Class methods that need manual logging
- Utility functions
- Error handling and warnings
- Debug output

## Testing
All existing logger calls continue to work as before, but now with automatic color-coding based on severity level.

## Next Steps (Optional)
- Consider adding color configuration via environment variables
- Add support for NO_COLOR environment variable for CI/CD environments
- Create color themes (dark mode, light mode, accessibility mode)
