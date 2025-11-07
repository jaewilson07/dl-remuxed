# Colored Logger Quick Reference

## ✅ Migration Complete!

All logger instances in domolibrary2 now use colored logging by default.

## Visual Guide

When you see logs in your terminal, they will appear as:

| Level     | Color         | Example Output                                    |
|-----------|---------------|---------------------------------------------------|
| DEBUG     | 🔵 Cyan       | \[2025-11-06] DEBUG - Connecting to API...\     |
| INFO      | 🟢 Green      | \[2025-11-06] INFO - Dataset uploaded\          |
| WARNING   | 🟡 Yellow     | \[2025-11-06] WARNING - Rate limit approaching\ |
| ERROR     | 🔴 Bold Red   | \[2025-11-06] ERROR - Upload failed\            |
| CRITICAL  | 🔴 Bold Red   | \[2025-11-06] CRITICAL - System failure\        |

## How to Use

### In Your Code
\\\python
from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()

# These will automatically be colored:
await logger.info("Success message")      # 🟢 Green
await logger.warning("Warning message")   # 🟡 Yellow
await logger.error("Error message")       # 🔴 Red
\\\

### No Changes Required
Existing code using \logger.info()\, \logger.warning()\, etc. will automatically
be colored. No code changes needed!

### Override Color (Optional)
\\\python
await logger.info("Custom color", color="magenta")
\\\

## Updated Files

✅ **DomoAccount** - account_default.py
✅ **DomoUser** - DomoUser.py
✅ **Utils** - upload_data.py

## Available Colors

- red, green, yellow, blue, magenta, cyan, white
- bold_red, bold_green, bold_blue, etc.
- dim_red, dim_green, dim_blue, etc.

---

**Note**: Colors appear in terminal/console output. In log files or CI/CD environments,
the raw ANSI codes may appear. Consider setting NO_COLOR environment variable in those cases.
