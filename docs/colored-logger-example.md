# Colored Logger Example

from domolibrary2.utils.logging import get_colored_logger

# Get the colored logger (singleton pattern)
logger = get_colored_logger()

# Now all your logs will be automatically colored:
await logger.info("This will be GREEN")         # ✅ Success messages
await logger.warning("This will be YELLOW")     # ⚠️  Warnings
await logger.error("This will be BOLD RED")     # ❌ Errors
await logger.debug("This will be CYAN")         # 🔍 Debug info

# You can override the default color for a specific message:
await logger.info("Custom colored message", color="magenta")

# Or customize the default colors when creating the logger:
custom_logger = get_colored_logger(
    info_color="blue",
    warning_color="yellow",
    error_color="red",
    debug_color="cyan"
)
