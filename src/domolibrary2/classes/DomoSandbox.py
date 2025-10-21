__all__ = ["DomoRepository", "DomoSandbox"]

import datetime as dt
from dataclasses import dataclass, field
from typing import List

import dateutil.parser as dtut
import httpx
import pandas as pd

from ..client import entities as dmee
from ..routes import sandbox as sandbox_routes
from . import DomoLineage as dmdl


@dataclass
class DomoRepository(dmee.DomoEntity_w_Lineage):
    auth: DomoAuth = field(repr=False)
    id: str

    name: str
    last_updated_dt: dt.datetime
    commit_dt: dt.datetime
    commit_version: str

    content_page_id_ls: List[str] = None
    content_card_id_ls: List[str] = None
    content_dataflow_id_ls: List[str] = None
    content_view_id_ls: List[str] = None

    def __post_init__(self):
        self.Lineage = dmdl.DomoLineage_Sandbox.from_parent(parent=self, auth=self.auth)

    @property
    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/sandbox/repositories/{self.id}"

    @classmethod
    def from_dict(cls, auth: DomoAuth, obj: dict):
        return cls(
            id=obj["id"],
            auth=auth,
            name=obj["name"],
            content_page_id_ls=obj["repositoryContent"]["pageIds"],
            content_card_id_ls=obj["repositoryContent"]["cardIds"],
            content_dataflow_id_ls=obj["repositoryContent"]["dataflowIds"],
            content_view_id_ls=obj["repositoryContent"]["viewIds"],
            last_updated_dt=dtut.parse(obj["updated"]).replace(tzinfo=None),
            commit_dt=dtut.parse(obj["lastCommit"]["completed"]).replace(tzinfo=None),
            commit_version=obj["lastCommit"]["commitName"],
            raw=obj,
            Lineage=None,
        )

    @classmethod
    async def get_by_id(
        cls,
        repository_id: str,
        auth: DomoAuth,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        res = await sandbox_routes.get_repo_from_id(
            repository_id=repository_id,
            auth=auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=cls.__name__,
        )

        return cls.from_dict(obj=res.response, auth=auth)

    @classmethod
    def _get_entity_by_id(
        cls,
        entity_id: str,
        auth: DomoAuth,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        return cls.get_by_id(
            repository_id=entity_id,
            auth=auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

    def convert_lineage_to_dataframe(self, return_raw: bool = False) -> pd.DataFrame:
        flat_lineage_ls = self.Lineage._flatten_lineage()

        output_ls = [
            {
                "sandbox_id": self.id,
                "sandbox_name": self.name,
                "version": self.commit_version,
                "commit_dt": self.commit_dt,
                "last_updated_dt": self.last_updated_dt,
                "entity_type": row.get("entity_type"),
                "entity_id": row.get("entity_id"),
            }
            for row in flat_lineage_ls
        ]

        if return_raw:
            return output_ls

        return pd.DataFrame(output_ls)


@dataclass
class DomoSandbox(DomoManager):
    auth: DomoAuth = field(repr=False)

    repositories: List[DomoRepository] = None

    async def get_repositories(
        self, debug_api: bool = False, session: httpx.AsyncClient = None
    ):
        res = await sandbox_routes.get_shared_repos(
            auth=self.auth, debug_api=debug_api, session=session, parent_class=self
        )

        self.repositories = [
            DomoRepository.from_dict(obj=obj, auth=self.auth) for obj in res.response
        ]

        return self.repositories

    async def get(self, debug_api: bool = False, session: httpx.AsyncClient = None):
        await self.get_repositories(debug_api=debug_api, session=session)

        return self.repositories
