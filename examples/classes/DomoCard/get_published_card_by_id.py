import domolibrary2.classes.DomoDataset as dmds
import domolibrary2.classes.DomoCard as dmdc
import domolibrary2.client.auth as dmda
import os

from pprint import pprint
from dotenv import load_dotenv

assert load_dotenv(".env")

from dc_logger.client.base import get_global_logger, set_global_logger
from dc_logger.client.base import HandlerBufferSettings, HandlerInstance, Logger
from dc_logger.logs.services.file import FileServiceConfig, FileHandler

json_config = FileServiceConfig(
    destination="LOGGER/classes/DomoDataset/get_federated_dataset_by_id.json",
    output_mode="file",
    format="json",
    append=True,
)

json_file_handler = FileHandler(
    buffer_settings=HandlerBufferSettings(), service_config=json_config
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

    child_card: dmdc.FederatedDomoCard = await dmdc.DomoCard.get_by_id(
        os.environ["CHILD_CARD_ID"], auth=child_auth
    )

    parent_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_PARENT_INSTANCE"],
        domo_access_token=os.environ["DOMO_PARENT_ACCESS_TOKEN"],
    )

    assert await parent_auth.who_am_i()

    parent_ds: dmds.DomoDataset = await child_card.get_federated_parent(
        parent_auth=parent_auth
    )

    pprint(
        {
            "title": "child_ds",
            "child instance": child_card.auth.domo_instance,
            "child_card_id": child_card.display_url(),
        }
    )

    pprint(
        {
            "title": "parent_ds",
            "parent instance": parent_ds.auth.domo_instance,
            "parent_ds_id": parent_ds.display_url(),
        }
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
