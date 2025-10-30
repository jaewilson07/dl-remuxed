import os

from dotenv import load_dotenv

import domolibrary2.classes.DomoDataset as dmds
import domolibrary2.client.auth as dmda

assert load_dotenv(".env")

from dc_logger.client.base import (
    Handler_BufferSettings,
    HandlerInstance,
    Logger,
    get_global_logger,
    set_global_logger,
)
from dc_logger.logs.services.file import File_ServiceConfig, FileHandler

json_config = File_ServiceConfig(
    destination="LOGGER/classes/DomoDataset/get_federated_dataset_by_id.json",
    output_mode="file",
    format="json",
    append=True,
)

json_file_handler = FileHandler(
    buffer_settings=Handler_BufferSettings(), service_config=json_config
)

json_handler_instance = HandlerInstance(
    service_handler=json_file_handler, handler_name="json_file"
)

logger: Logger = get_global_logger()
logger.handlers = [json_handler_instance]
set_global_logger(logger)


async def main():
    child_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_CHILD_INSTANCE"],
        domo_access_token=os.environ["DOMO_CHILD_ACCESS_TOKEN"],
    )

    await dmds.DomoCard.get_by_id(
        os.environ["CHILD_CARD_ID"], auth=child_auth
    )

    parent_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_PARENT_INSTANCE"],
        domo_access_token=os.environ["DOMO_PARENT_ACCESS_TOKEN"],
    )

    assert await parent_auth.who_am_i()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
