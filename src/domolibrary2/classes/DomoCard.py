__all__ = ["DomoCard", "Card_DownloadSourceCode"]

import json
import os
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, List, Optional

import httpx
from dc_logger.decorators import log_call, LogDecoratorConfig

from ..client.entities import DomoEntity_w_Lineage
from ..client.auth import DomoAuth
from ..client.exceptions import DomoError
from ..routes import card as card_routes
from ..utils import (
    DictDot as util_dd,
    chunk_execution as dmce,
    files as dmfi,
)
from ..utils.logging import DomoEntityObjectProcessor
from .DomoUser import DomoUser
from .DomoGroup import DomoGroup
from .subentity.lineage import DomoLineage


@dataclass
class DomoCard(DomoEntity_w_Lineage):
    id: str
    auth: DomoAuth = field(repr=False)
    Lineage: Optional[DomoLineage] = field(repr=False, default=None)

    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    urn: Optional[str] = None
    chart_type: Optional[str] = None
    dataset_id: Optional[str] = None

    datastore_id: Optional[str] = None

    domo_collections: List[Any] = field(default_factory=list)
    domo_source_code: Any = None

    certification: Optional[dict] = None
    owners: List[Any] = field(default_factory=list)

    datasets: List[Any] = field(repr=False, default_factory=list)

    def __post_init__(self):
        # self.Definition = CardDefinition(self)
        self.Lineage = DomoLineage.from_parent(auth=self.auth, parent=self)

    @property
    def display_url(self) -> str:
        return f"https://{self.auth.domo_instance}.domo.com/kpis/details/{self.id}"

    @classmethod
    async def from_dict(
        cls, auth: DomoAuth, obj: dict, is_suppress_errors: bool = False
    ):
        from . import DomoGroup as dmgr

        dd = obj
        if isinstance(obj, dict):
            dd = util_dd.DictDot(obj)

        card = cls(
            auth=auth,
            id=dd.id,
            raw=obj,
            title=dd.title,
            description=dd.description,
            type=dd.type,
            urn=dd.urn,
            certification=dd.certification,
            chart_type=dd.metadata and dd.metadata.chartType,
            dataset_id=dd.datasources[0].dataSourceId if dd.datasources else None,
            Lineage=None,  # type: ignore
        )

        tasks = []
        for user in dd.owners:
            try:
                if user.type == "USER":
                    tasks.append(DomoUser.get_by_id(auth=auth, id=user.id))
                if user.type == "GROUP":
                    tasks.append(dmgr.DomoGroup.get_by_id(group_id=user.id, auth=auth))

            except DomoError as e:
                if not is_suppress_errors:
                    raise e from e
                else:
                    print(
                        f"Suppressed error getting owner {user.id} for card {card.id}: {e}"
                    )

        card.owners = await dmce.gather_with_concurrency(n=60, *tasks)

        if obj.get("domoapp", {}).get("id"):
            card.datastore_id = obj["domoapp"]["id"]

        return card

    @classmethod
    @log_call(
        level_name="entity",
        config=LogDecoratorConfig(result_processor=DomoEntityObjectProcessor())
    )
    async def get_by_id(
        cls,
        auth: DomoAuth,
        entity_id: str,
        optional_parts: str = "certification,datasources,drillPath,owners,properties,domoapp",
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
        is_suppress_errors: bool = False,
    ):
        res = await card_routes.get_card_metadata(
            auth=auth,
            card_id=entity_id,
            optional_parts=optional_parts,
            debug_api=debug_api,
            session=session,
            parent_class=cls.__name__,
        )

        if return_raw:
            return res

        domo_card = await cls.from_dict(
            auth=auth, obj=res.response, is_suppress_errors=is_suppress_errors
        )

        return domo_card

    @classmethod
    async def get_entity_by_id(
        cls, auth: DomoAuth, entity_id: str, is_suppress_errors: bool = False, **kwargs
    ):
        return await cls.get_by_id(
            auth=auth,
            entity_id=entity_id,
            is_suppress_errors=is_suppress_errors,
            **kwargs,
        )

    async def get_datasets(
        self,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ):
        res = await card_routes.get_card_metadata(
            auth=self.auth,
            card_id=self.id,
            optional_parts="datasources",
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
        )

        res.response = res.response["datasources"]

        if return_raw:
            return res

        from .DomoDataset.core import DomoDataset

        self.datasets = await dmce.gather_with_concurrency(
            *[
                DomoDataset.get_by_id(dataset_id=obj["dataSourceId"], auth=self.auth)
                for obj in res.response
            ],
            n=10,
        )

        return self.datasets

    async def share(
        self,
        auth: Optional[DomoAuth] = None,
        domo_users: Optional[List[DomoUser]] = None,  # DomoUsers to share card with,
        domo_groups: Optional[List[DomoGroup]] = None,  # DomoGroups to share card with
        message: Optional[str] = None,  # message for automated email
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ):
        from ..routes import datacenter as datacenter_routes

        if domo_groups:
            domo_groups = (
                domo_groups if isinstance(domo_groups, list) else [domo_groups]
            )
        if domo_users:
            domo_users = domo_users if isinstance(domo_users, list) else [domo_users]

        res = await datacenter_routes.share_resource(
            auth=auth or self.auth,
            resource_ids=[self.id],
            resource_type=datacenter_routes.ShareResource_Enum.CARD,
            group_ids=[group.id for group in domo_groups] if domo_groups else None,
            user_ids=[user.id for user in domo_users] if domo_users else None,
            message=message,
            debug_api=debug_api,
            session=session,
        )

        return res

    async def get_collections(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        debug_num_stacks_to_drop=2,
    ):
        from . import DomoAppDb as dmdb

        domo_collections = await dmdb.AppDbCollections.get_collections(
            datastore_id=self.datastore_id,
            auth=self.auth,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            return_raw=return_raw,
        )

        if return_raw:
            return domo_collections

        self.domo_collections = await dmce.gather_with_concurrency(
            *[
                dmdb.AppDbCollection.get_by_id(
                    collection_id=domo_collection.id,
                    auth=self.auth,
                    debug_api=debug_api,
                )
                for domo_collection in domo_collections
            ],
            n=60,
        )

        return self.domo_collections

    async def get_source_code(
        self, debug_api: bool = False, try_auto_share: bool = False
    ):
        await self.get_collections(debug_api=debug_api)

        collection_name = "ddx_app_client_code"
        code_collection = next(
            (
                domo_collection
                for domo_collection in self.domo_collections
                if domo_collection.name == collection_name
            ),
            None,
        )

        if not code_collection:
            raise Card_DownloadSourceCode(
                card=deepcopy(self),
                auth=self.auth,
                message=f"collection - {collection_name} not found for {self.title} - {self.id}",
            )

        documents = await code_collection.query_documents(
            debug_api=debug_api, try_auto_share=try_auto_share
        )

        if not documents:
            raise Card_DownloadSourceCode(
                card=deepcopy(self),
                auth=self.auth,
                message=f"collection - {collection_name} - {code_collection.id} - unable to retrieve documents for {self.title} - {self.id}",
            )

        self.domo_source_code = documents[0]

        return self.domo_source_code

    async def download_source_code(
        self,
        download_folder="./EXPORT/",
        file_name=None,
        debug_api: bool = False,
        try_auto_share: bool = False,
    ):
        doc = await self.get_source_code(
            debug_api=debug_api, try_auto_share=try_auto_share
        )

        if file_name:
            download_path = os.path.join(
                download_folder, dmfi.change_extension(file_name, new_extension=".json")
            )
            dmfi.upsert_folder(download_path)

            with open(download_path, "w+", encoding="utf-8") as f:
                f.write(json.dumps(doc.content))
                return doc

        ddx_type = next(iter(doc.content))

        for key, value in doc.content[ddx_type].items():
            if key == "js":
                file_name = "app.js"
            elif key == "html":
                file_name = "index.html"
            elif key == "css":
                file_name = "styles.css"
            else:
                file_name = f"{key}.txt"

            download_path = os.path.join(
                download_folder, f"{ddx_type}/{self.id}/{file_name}"
            )
            dmfi.upsert_folder(download_path)

            with open(download_path, "w+", encoding="utf-8") as f:
                f.write(value)

        return doc


class Card_DownloadSourceCode(DomoError):
    def __init__(self, card: DomoCard, auth: DomoAuth, message: str):
        super().__init__(
            parent_class=card.__class__.__name__, entity_id=card.id, message=message
        )
