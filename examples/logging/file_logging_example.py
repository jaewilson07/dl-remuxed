"""
File Logging Example for Domo Library

This example demonstrates how to properly set up file logging with multiple formats
(JSON, CSV, and plain text) using multiple handlers on the same logger.
"""

import asyncio
import os

from dc_logger.client.base import (
    HandlerBufferSettings,
    HandlerInstance,
    Logger,
    set_global_logger,
)
from dc_logger.logs.services.file import FileHandler, FileServiceConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Multiple file configurations
json_config = FileServiceConfig(
    destination="./LOGGER/file_logging_example/file_auth_example.json",
    output_mode="file",
    format="json",
    append=True,
)

csv_config = FileServiceConfig(
    destination="./LOGGER/file_logging_example/file_auth_example.csv",
    output_mode="file",
    format="csv",
    append=True,
)

text_config = FileServiceConfig(
    destination="./LOGGER/file_logging_example/file_auth_example.log",
    output_mode="file",
    format="text",
    append=True,
)

buffer_settings = HandlerBufferSettings()

# Create handlers for each format
json_handler = FileHandler(
    buffer_settings=buffer_settings, service_config=json_config
)
csv_handler = FileHandler(
    buffer_settings=buffer_settings, service_config=csv_config
)
text_handler = FileHandler(
    buffer_settings=buffer_settings, service_config=text_config
)

# Create handler instances
json_handler_instance = HandlerInstance(
    service_handler=json_handler, handler_name="json_file"
)
csv_handler_instance = HandlerInstance(
    service_handler=csv_handler, handler_name="csv_file"
)
text_handler_instance = HandlerInstance(
    service_handler=text_handler, handler_name="text_file"
)

# Create logger with multiple handlers and override global logger
logger = Logger(
    app_name="multi_format_example",
    handlers=[json_handler_instance, csv_handler_instance, text_handler_instance]
)
set_global_logger(logger)


async def main():
    """Example with properly configured multi-format file logging."""

    # Get credentials from environment
    DOMO_INSTANCE = os.getenv("DOMO_INSTANCE")
    DOMO_ACCESS_TOKEN = os.getenv("DOMO_ACCESS_TOKEN")
    PARENT_DATASET = os.getenv("PARENT_DATASET")
    PARENT_CARD = os.getenv("PARENT_CARD")

    if not all([DOMO_INSTANCE, DOMO_ACCESS_TOKEN, PARENT_DATASET, PARENT_CARD]):
        print("Missing required environment variables. Please check your .env file.")
        return

    # Import Domo classes after logger setup
    from domolibrary2.client.auth import DomoTokenAuth
    from domolibrary2.routes import (
        card as card_routes,
        dataset as dataset_routes,
        user as user_routes,
    )

    # Create authentication object
    auth = DomoTokenAuth(
        domo_instance=DOMO_INSTANCE,
        domo_access_token=DOMO_ACCESS_TOKEN
    )

    # Test authentication - this will be logged to all three file formats
    auth_result = await auth.who_am_i()
    await logger.info(message="Authentication completed", data=auth_result.response)

    # Test dataset route - this will be logged to all three file formats with entity information
    dataset_result = await dataset_routes.get_dataset_by_id(
        dataset_id=PARENT_DATASET,
        auth=auth
    )
    await logger.info(message="Dataset retrieval completed", data=dataset_result.response)

    # Test card route - this will be logged to all three file formats with entity information
    card_result = await card_routes.get_card_metadata(
        auth=auth,
        card_id=PARENT_CARD
    )
    await logger.info(message="Card retrieval completed", data=card_result.response)

    # Test user route - get all users, this will be logged to all three file formats
    users_result = await user_routes.get_all_users(auth=auth)
    await logger.info(message="Users retrieval completed", data={"user_count": len(users_result.response) if users_result.response else 0})

    print(f"Authentication successful: {auth_result.is_success}")
    print(f"Dataset retrieval successful: {dataset_result.is_success}")
    print(f"Card retrieval successful: {card_result.is_success}")
    print(f"Users retrieval successful: {users_result.is_success}")
    print("Check the log files:")
    print(f"  - JSON format: {json_config.destination}")
    print(f"  - CSV format: {csv_config.destination}")
    print(f"  - Text format: {text_config.destination}")


if __name__ == "__main__":
    asyncio.run(main())
