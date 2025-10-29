"""
Console Logging Example for Domo Library

This example demonstrates how to properly set up console logging by overriding
the global logger with a custom console configuration.
"""

import asyncio
import os
from dotenv import load_dotenv

from dc_logger.client.base import (
    Logger,
    HandlerInstance,
    HandlerBufferSettings,
    set_global_logger,
)
from dc_logger.logs.services.console import ConsoleServiceConfig, ConsoleHandler

# Load environment variables
load_dotenv()

# Console configuration
console_config = ConsoleServiceConfig(
    output_mode="console",
    format="json"
)

buffer_settings = HandlerBufferSettings()

# Console handler
console_handler = ConsoleHandler(
    buffer_settings=buffer_settings, service_config=console_config
)

# Create handler instance
console_handler_instance = HandlerInstance(
    service_handler=console_handler, handler_name="default_console"
)

# Create logger with console handler and override global logger
logger = Logger(app_name="console_example", handlers=[console_handler_instance])
set_global_logger(logger)


async def main():
    """Example with properly configured console logging."""
    
    # Get credentials from environment
    DOMO_INSTANCE = os.getenv("DOMO_INSTANCE")
    DOMO_ACCESS_TOKEN = os.getenv("DOMO_ACCESS_TOKEN")
    
    if not all([DOMO_INSTANCE, DOMO_ACCESS_TOKEN]):
        print("Missing required environment variables. Please check your .env file.")
        return
    
    # Import Domo classes after logger setup
    from domolibrary2.client.auth import DomoTokenAuth
    
    # Create authentication object
    auth = DomoTokenAuth(
        domo_instance=DOMO_INSTANCE,
        domo_access_token=DOMO_ACCESS_TOKEN
    )
    
    # Test authentication - this will be logged to console with our custom configuration
    result = await auth.who_am_i()

    await logger.info(message="Authentication successful", data=result.response)

if __name__ == "__main__":
    asyncio.run(main())