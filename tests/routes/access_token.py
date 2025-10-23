import domolibrary2.client.auth as dmda

# import domolibrary2.routes.access_token as access_token_routes
from dotenv import load_dotenv
import os

# from dc_logger.client.base import (
#     Logger,
#     HandlerInstance,
#     Handler_BufferSettings,
#     set_global_logger,
# )

# from dc_logger.logs.services.file import FileHandler, File_ServiceConfig

load_dotenv()

# json_config = File_ServiceConfig(
#     destination="./LOGGER/routes/test_access_tokens.json",
#     output_mode="file",
#     format="json",
#     append=True,
# )

# buffer_settings = Handler_BufferSettings()

# json_file_handler = FileHandler(
#     buffer_settings=buffer_settings, service_config=json_config
# )

# # Create handler instance
# json_handler_instance = HandlerInstance(
#     service_handler=json_file_handler, handler_name="json_file"
# )

# logger = Logger(app_name="test_access_tokens", handlers=[json_handler_instance])

# set_global_logger(logger)


# async def test_logger():
#     """Test logger functionality."""

#     await logger.info(message="Starting test_logger function.")

#     domo_auth = dmda.DomoTokenAuth(
#         domo_access_token=os.getenv("DOMO_ACCESS_TOKEN"),
#         domo_instance=os.getenv("DOMO_INSTANCE"),
#     )

    res = await access_token_routes.get_access_tokens(auth=domo_auth)

    # logger.info(message="Completed get_access_tokens request.", data=res.response)

    assert res.is_success


def main():
    """Main function to run the test."""
    import asyncio

    asyncio.run(test_logger())


if __name__ == "__main__":
    main()
