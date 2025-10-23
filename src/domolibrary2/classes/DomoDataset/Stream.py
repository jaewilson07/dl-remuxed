from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

import httpx

from ...client.auth import DomoAuth
from ...entities import DomoEntity, DomoManager
from ...routes import stream as stream_routes
from ...utils import chunk_execution as dmce
from .stream_config import StreamConfig

__all__ = [
    "DomoStream",
    "DomoStreams",
]


@dataclass
class DomoStream(DomoEntity):
    """A class for interacting with a Domo Stream (dataset connector)"""

    id: str

    transport_description: str = None
    transport_version: int = None
    update_method: str = None
    data_provider_name: str = None
    data_provider_key: str = None
    account_id: str = None
    account_display_name: str = None
    account_userid: str = None

    has_mapping: bool = False
    configuration: List[StreamConfig] = field(default_factory=list)
    configuration_tables: List[str] = field(default_factory=list)
    configuration_query: str = None

    parent: Any = None  # DomoDataset

    @property
    def dataset_id(self) -> str:
        return self.parent.id

    @classmethod
    def from_parent(cls, parent, stream_id):
        return cls(
            parent=parent, auth=parent.auth, id=stream_id, Relations=None, raw=None
        )

    @property
    def entity_type(self):
        return "STREAM"

    @property
    def display_url(self):
        """Generate URL to view this stream in the Domo UI"""
        return f"https://{self.auth.domo_instance}.domo.com/datasources/{self.dataset_id}/details/data/table"

    @classmethod
    def from_dict(cls, auth, obj):
        data_provider = obj.get("dataProvider", {})
        transport = obj.get("transport", {})
        datasource = obj.get("dataSource", {})

        account = obj.get("account", {})

        sd = cls(
            auth=auth,
            parent=None,  # Will be set by caller if needed
            id=obj["id"],
            transport_description=transport.get("description"),
            transport_version=transport.get("version"),
            update_method=obj.get("updateMethod"),
            data_provider_name=data_provider.get("name"),
            data_provider_key=data_provider.get("key"),
            dataset_id=datasource.get("id"),
            raw=obj,
            Relations=None,
        )

        if account:
            sd.account_id = account.get("id")
            sd.account_display_name = account.get("displayName")
            sd.account_userid = account.get("userId")

        sd.configuration = [
            StreamConfig.from_json(
                obj=c_obj, data_provider_type=data_provider.get("key"), parent_stream=sd
            )
            for c_obj in obj.get("configuration", [])
        ]

        return sd

    def generate_config_rpt(self):
        res = {}

        for config in self.configuration:
            if config.stream_category != "default" and config.stream_category:
                obj = config.to_dict()
                res.update({obj["field"]: obj["value"]})

        return res

    @classmethod
    async def get_by_id(
        cls,
        auth: DomoAuth,
        stream_id: str,
        return_raw: bool = False,
        debug_num_stacks_to_drop=2,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ):
        """Get a stream by its ID.

        Args:
            auth: Authentication object
            stream_id: Unique stream identifier
            return_raw: Return raw response without processing
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            debug_api: Enable API debugging
            parent: Parent dataset entity
            session: HTTP client session

        Returns:
            DomoStream instance or ResponseGetData if return_raw=True

        Raises:
            Stream_GET_Error: If stream retrieval fails
        """
        res = await stream_routes.get_stream_by_id(
            auth=auth,
            stream_id=stream_id,
            session=session,
            parent_class=cls.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            debug_api=debug_api,
        )

        if return_raw:
            return res

        return cls.from_dict(auth=auth, obj=res.response)

    @classmethod
    async def get_entity_by_id(cls, entity_id: str, auth: DomoAuth, **kwargs):
        return await cls.get_by_id(stream_id=entity_id, auth=auth, **kwargs)

    @classmethod
    async def create(
        cls,
        cnfg_body,
        auth: DomoAuth = None,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
    ):
        return await stream_routes.create_stream(
            auth=auth, body=cnfg_body, session=session, debug_api=debug_api
        )

    async def update(
        self,
        cnfg_body,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
    ):
        res = await stream_routes.update_stream(
            auth=self.auth,
            stream_id=self.id,
            body=cnfg_body,
            session=session,
            debug_api=debug_api,
        )
        return res


@dataclass
class DomoStreams(DomoManager):
    streams: List[DomoStream] = field(default=None)

    async def get(
        self,
        search_dataset_name: str = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ):
        from ...routes import datacenter as datacenter_routes

        res = await datacenter_routes.search_datasets(
            auth=self.auth,
            entity_type=datacenter_routes.Datacenter_Enum.DATASET.value,
            session=session,
            search_text=search_dataset_name,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        self.streams = await dmce.gather_with_concurrency(
            *[
                DomoStream.get_by_id(self.auth, stream_id=obj["streamId"])
                for obj in res.response
            ],
            n=10,
        )

        return self.streams

    async def upsert(
        self,
        cnfg_body,
        match_name=None,
        auth: DomoAuth = None,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
    ):
        from ...routes import datacenter as datacenter_routes

        res = await datacenter_routes.search_datasets(
            auth=auth or self.auth,
            entity_type=datacenter_routes.Datacenter_Enum.DATASET.value,
            session=session,
            search_text=match_name,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )
        datasets = res.response

        existing_ds = next((ds for ds in datasets if ds.name == match_name), None)

        if existing_ds:
            domo_stream = await DomoStream.get_by_id(
                auth=auth, stream_id=existing_ds.stream_id
            )

            return await domo_stream.update(
                cnfg_body,
                session=session,
                debug_api=False,
            )

        else:
            return await DomoStream.create(
                cnfg_body, auth=auth, session=session, debug_api=debug_api
            )
