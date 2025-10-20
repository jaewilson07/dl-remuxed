__all__ = ["DomoConnector"]

import datetime as dt
from dataclasses import dataclass, field
from typing import List

import httpx

from ..client import auth as dmda
from ..utils import convert as cd
from ..utils import DictDot as util_dd
from ..utils import convert as cd


@dataclass
class DomoConnector:
    id: str
    label: str
    title: str
    sub_title: str
    description: str
    create_date: dt.datetime
    last_modified: dt.datetime
    publisher_name: str
    writeback_enabled: bool
    tags: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, obj: dict):
        dd = util_dd.DictDot(obj)

        return cls(
            id=dd.databaseId,
            label=dd.label,
            title=dd.title,
            sub_title=dd.subTitle,
            description=dd.description,
            create_date=cd.convert_epoch_millisecond_to_datetime(dd.createDate),
            last_modified=cd.convert_epoch_millisecond_to_datetime(dd.lastModified),
            publisher_name=dd.publisherName,
            writeback_enabled=dd.writebackEnabled,
            tags=dd.tags,
            capabilities=dd.capabilities,
        )


@dataclass
class DomoConnectors:
    auth: dmda.DomoAuth = field(repr=False)

    domo_connectors: List[DomoConnector] = field(default=None)

    async def get(
        self,
        search_text=None,
        additional_filters_ls=None,
        return_raw: bool = False,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        from ..routes import datacenter as datacenter_routes

        res = await datacenter_routes.get_connectors(
            auth=self.auth,
            search_text=search_text,
            additional_filters_ls=additional_filters_ls,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            session=session,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        if len(res.response) == 0:
            self.domo_connectors = []

        self.domo_connectors = [DomoConnector.from_dict(obj) for obj in res.response]
        return self.domo_connectors
