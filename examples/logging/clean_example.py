"""
Clean Example - Automatic Logging Demonstration

This example demonstrates the enhanced logging functionality without any manual setup.
All logging happens automatically through the @log_call decorators we've implemented.

The script will:
1. Authenticate to Domo
2. Get dataset information
3. Get card information

All operations will be automatically logged with rich entity information.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Domo classes
from domolibrary2.client.auth import DomoTokenAuth
from domolibrary2.routes import dataset as dataset_routes
from domolibrary2.routes import card as card_routes


async def main():
    """Main function demonstrating automatic logging."""
    
    # Get credentials from environment
    DOMO_INSTANCE = os.getenv("DOMO_INSTANCE")
    DOMO_ACCESS_TOKEN = os.getenv("DOMO_ACCESS_TOKEN")
    PARENT_DATASET = os.getenv("PARENT_DATASET")
    PARENT_CARD = os.getenv("PARENT_CARD")
    
    if not all([DOMO_INSTANCE, DOMO_ACCESS_TOKEN, PARENT_DATASET, PARENT_CARD]):
        print("Missing required environment variables. Please check your .env file.")
        return
    
    # Create authentication object
    auth = DomoTokenAuth(
        domo_instance=DOMO_INSTANCE,
        domo_access_token=DOMO_ACCESS_TOKEN
    )
    
    # Test authentication
    await auth.who_am_i()
    
    # Get dataset information
    dataset_response = await dataset_routes.get_dataset_by_id(
        dataset_id=PARENT_DATASET,
        auth=auth
    )
    
    # Get card information
    card_response = await card_routes.get_card_metadata(
        auth=auth,
        card_id=PARENT_CARD
    )
    
    # The script completes - all operations were automatically logged
    # Check the log files to see the rich entity information captured


if __name__ == "__main__":
    asyncio.run(main())
