# 🎚️ Log Level Control - Quick Reference

## For Your Jupyter Notebook

Add this to your first cell:

\\\python
from domolibrary2.utils.logging import get_colored_logger

logger = get_colored_logger()
logger.set_level('WARNING')  # 👈 Quiet mode - only warnings/errors
\\\

## One-Line Commands

\\\python
# Quiet (recommended for notebooks)
get_colored_logger().set_level('WARNING')

# Very quiet (only errors)
get_colored_logger().set_level('ERROR')

# Normal (default)
get_colored_logger().set_level('INFO')

# Verbose (debugging)
get_colored_logger().set_level('DEBUG')
\\\

## What You'll See

| Level     | Shows                          | Use When                  |
|-----------|--------------------------------|---------------------------|
| DEBUG     | Everything                     | Debugging issues          |
| INFO      | Success messages + above       | Default (can be noisy)    |
| WARNING   | Warnings + errors only         | **Recommended for notebooks** |
| ERROR     | Errors only                    | Production scripts        |

## Colors

- 🟢 INFO = Green
- 🟡 WARNING = Yellow
- 🔴 ERROR = Red
- 🔵 DEBUG = Cyan

## Example

\\\python
# First cell in your notebook
from domolibrary2.utils.logging import get_colored_logger
import domolibrary2.client.auth as dmda

# Quiet mode
logger = get_colored_logger()
logger.set_level('WARNING')

# Your code runs quietly now
auth = dmda.DomoTokenAuth(...)
# No INFO logs! Only warnings/errors show
\\\

---

**💡 Pro Tip**: Start with WARNING level, switch to DEBUG only when troubleshooting!
