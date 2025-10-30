"""
Datadog Logging Example for Domo Library

This example demonstrates how to properly set up Datadog logging by overriding
the global logger with a custom Datadog configuration.
"""

import asyncio
import os

from dc_logger.client.base import (
    HandlerBufferSettings,
    HandlerInstance,
    Logger,
    set_global_logger,
)
from dc_logger.logs.services.cloud.datadog import DatadogHandler, DatadogServiceConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Datadog configuration
datadog_config = DatadogServiceConfig(
    api_key=os.getenv("DATADOG_API_KEY"),
    app_key=os.getenv("DATADOG_APP_KEY"),  # Optional
    site=os.getenv("DATADOG_SITE", "datadoghq.com"),
    service=os.getenv("DATADOG_SERVICE", "domolibrary"),
    env=os.getenv("DATADOG_ENV", "production"),
)

buffer_settings = HandlerBufferSettings()

# Datadog handler
datadog_handler = DatadogHandler(config=datadog_config)

# Create handler instance
datadog_handler_instance = HandlerInstance(
    service_handler=datadog_handler, handler_name="datadog"
)

# Create logger with Datadog handler and override global logger
logger = Logger(app_name="datadog_example", handlers=[datadog_handler_instance])
set_global_logger(logger)


async def main():
    """Example with properly configured Datadog logging."""

    # Get credentials from environment
    DOMO_INSTANCE = os.getenv("DOMO_INSTANCE")
    DOMO_ACCESS_TOKEN = os.getenv("DOMO_ACCESS_TOKEN")
    PARENT_DATASET = os.getenv("PARENT_DATASET")
    PARENT_CARD = os.getenv("PARENT_CARD")

    if not all([DOMO_INSTANCE, DOMO_ACCESS_TOKEN, PARENT_DATASET, PARENT_CARD]):
        print("Missing required environment variables. Please check your .env file.")
        return

    if not os.getenv("DATADOG_API_KEY"):
        print("Missing DATADOG_API_KEY environment variable.")
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
        domo_instance=DOMO_INSTANCE, domo_access_token=DOMO_ACCESS_TOKEN
    )

    # Test authentication - this will be logged to Datadog
    auth_result = await auth.who_am_i()
    await logger.info(message="Authentication completed", data=auth_result.response)

    # Test dataset route - this will be logged to Datadog with entity information
    dataset_result = await dataset_routes.get_dataset_by_id(
        dataset_id=PARENT_DATASET, auth=auth
    )
    await logger.info(
        message="Dataset retrieval completed", data=dataset_result.response
    )

    # Test card route - this will be logged to Datadog with entity information
    card_result = await card_routes.get_card_metadata(auth=auth, card_id=PARENT_CARD)
    await logger.info(message="Card retrieval completed", data=card_result.response)

    # Test user route - get all users, this will be logged to Datadog
    users_result = await user_routes.get_all_users(auth=auth)
    await logger.info(
        message="Users retrieval completed",
        data={"user_count": len(users_result.response) if users_result.response else 0},
    )

    print(f"Authentication successful: {auth_result.is_success}")
    print(f"Dataset retrieval successful: {dataset_result.is_success}")
    print(f"Card retrieval successful: {card_result.is_success}")
    print(f"Users retrieval successful: {users_result.is_success}")
    print(f"All operations logged to Datadog at: {datadog_config.site}")


if __name__ == "__main__":
    asyncio.run(main())
