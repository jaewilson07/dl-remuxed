"""Core DomoPage entity class and basic operations."""

__all__ = ["DomoPage"]

from dataclasses import dataclass, field
from typing import Optional

import httpx

from ...client.auth import DomoAuth
from ...entities.entities import DomoEntity_w_Lineage
from ...routes import page as page_routes
from ...utils import (
    DictDot as util_dd,
    chunk_execution as dmce,
)
from .. import (
    DomoUser as dmu,
)
from ..subentity import DomoLineage
from . import page_content as dmpg_c


@dataclass
class DomoPage(DomoEntity_w_Lineage):
    id: int
    auth: DomoAuth = field(repr=False)
    Lineage: Optional[DomoLineage] = field(repr=False, default=None)

    title: str = None
    top_page_id: int = None
    parent_page_id: int = None
    is_locked: bool = None

    collections: list = field(default_factory=list)

    owners: list = field(default_factory=list)
    cards: list = field(default_factory=list)

    custom_attributes: dict = field(default_factory=dict)

    parent_page: dict = None  # DomoPage
    top_page: dict = None  # DomoPage
    children: list = field(default_factory=list)

    # parent_hierarchy: [dict] = None
    # flat_children: list = None

    layout: dmpg_c.PageLayout = field(default_factory=dict)

    cards: list["DomoCard"] = None
    datasets: list["DomoDataset"] = None

    def __post_init__(self):
        self.Lineage = dmdl.DomoLineage_Page.from_parent(parent=self)

    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/page/{self.id}"

    async def _get_domo_owners_from_dd(
        self,
        owners: util_dd.DictDot,
        suppress_no_results_error: bool = True,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 3,
    ):
        if not owners or len(owners) == 0:
            return []

        from .. import DomoGroup as dmg

        domo_groups = []
        domo_users = []

        owner_group_ls = [
            owner.id for owner in owners if owner.type == "GROUP" and owner.id
        ]

        if len(owner_group_ls) > 0:
            domo_groups = await dmce.gather_with_concurrency(
                n=60,
                *[
                    dmg.DomoGroup.get_by_id(
                        group_id=group_id,
                        auth=self.auth,
                        debug_api=debug_api,
                        session=session,
                        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                    )
                    for group_id in owner_group_ls
                ],
            )

        owner_user_ls = [
            owner.id for owner in owners if owner.type == "USER" and owner.id
        ]

        if len(owner_user_ls) > 0:
            domo_users = await dmu.DomoUsers.by_id(
                user_ids=owner_user_ls,
                only_allow_one=False,
                auth=self.auth,
                session=session,
                debug_api=debug_api,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                suppress_no_results_error=suppress_no_results_error,
            )

        owner_ce = (domo_groups or []) + (domo_users or [])

        res = []
        for owner in owner_ce:
            if isinstance(owner, list):
                [res.append(member) for member in owner]
            else:
                res.append(owner)

        return res

    @classmethod
    async def _from_content_stacks_v3(
        cls,
        page_obj,
        suppress_no_results_error: bool = True,
        auth: DomoAuth = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 3,
    ):
        # from . import DomoCard as dc

        dd = page_obj
        if isinstance(page_obj, dict):
            dd = util_dd.DictDot(page_obj)

        pg = cls(
            id=int(dd.id),
            title=dd.title,
            raw=page_obj,
            parent_page_id=int(dd.page.parentPageId) if dd.page.parentPageId else None,
            collections=dd.collections,
            auth=auth,
            Lineage=None,
        )

        if hasattr(dd, "pageLayoutV4") and dd.pageLayoutV4 is not None:
            pg.layout = dmpg_c.PageLayout.from_dict(dd=dd.pageLayoutV4)

        if dd.page.owners and len(dd.page.owners) > 0:
            pg.owners = await pg._get_domo_owners_from_dd(
                dd.page.owners,
                suppress_no_results_error=suppress_no_results_error,
                debug_api=debug_api,
                session=session,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            )

        return pg

    @classmethod
    async def get_by_id(
        cls,
        page_id: str,
        auth: DomoAuth,
        suppress_no_results_error: bool = True,
        return_raw: bool = False,
        debug_api: bool = False,
        include_layout: bool = False,
        # if True, will drill down to all the Children.  Set to False to prevent calculating children
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
        id=None,
    ):
        page_id = page_id or id

        res = await page_routes.get_page_by_id(
            auth=auth,
            page_id=page_id,
            debug_api=debug_api,
            include_layout=include_layout,
            session=session,
            parent_class=cls.__name__,
        )

        if return_raw:
            return res

        pg = await cls._from_content_stacks_v3(
            page_obj=res.response,
            auth=auth,
            session=session,
            debug_api=debug_api,
            suppress_no_results_error=suppress_no_results_error,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        pg.custom_attributes["parent_page"] = None
        pg.custom_attributes["top_page"] = None

        return pg

    @classmethod
    async def get_entity_by_id(cls, entity_id: str, **kwargs):
        return await cls.get_by_id(page_id=entity_id, **kwargs)

    @classmethod
    async def from_dict(cls, **kwargs):
        return await cls._from_content_stacks_v3(**kwargs)

    @classmethod
    async def _from_adminsummary(
        cls,
        page_obj,
        auth: DomoAuth,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
    ):
        from .. import DomoCard as dmc

        dd = page_obj

        if isinstance(page_obj, dict):
            dd = util_dd.DictDot(page_obj)

        page_id = int(dd.id or dd.pageId)

        parent_page_id = int(dd.parentPageId) if dd.parentPageId else page_id

        top_page_id = int(dd.topPageId) if dd.topPageId else parent_page_id

        pg = cls(
            id=page_id,
            title=dd.title or dd.pageTitle,
            raw=page_obj,
            parent_page_id=parent_page_id,
            top_page_id=top_page_id,
            collections=dd.collections,
            is_locked=dd.locked,
            auth=auth,
            Lineage=None,
        )

        if dd.page and dd.page.owners and len(dd.page.owners) > 0:
            pg.owners = await pg._get_domo_owners_from_dd(
                dd.page.owners, debug_api=debug_api, session=session
            )

        if dd.cards and len(dd.cards) > 0:
            pg.cards = await dmce.gather_with_concurrency(
                n=60,
                *[
                    dmc.DomoCard.get_by_id(
                        id=card.id, auth=auth, session=session, debug_api=debug_api
                    )
                    for card in dd.cards
                ],
            )

        return pg

    @classmethod
    async def _from_bootstrap(
        cls,
        page_obj,
        auth: DomoAuth = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        dd = page_obj
        if isinstance(page_obj, dict):
            dd = util_dd.DictDot(page_obj)

        pg = cls(id=int(dd.id), title=dd.title, raw=page_obj, auth=auth, Lineage=None)

        if isinstance(dd.owners, list) and len(dd.owners) > 0:
            pg.owners = await pg._get_domo_owners_from_dd(
                dd.owners, debug_api=debug_api, session=session
            )

        if isinstance(dd.children, list) and len(dd.children) > 0:
            pg.children = await dmce.gather_with_concurrency(
                n=60,
                *[
                    cls._from_bootstrap(
                        page_obj=child_dd,
                        auth=auth,
                        debug_api=debug_api,
                        session=session,
                    )
                    for child_dd in dd.children
                    if child_dd.type == "page"
                ],
            )

            [print(other_dd) for other_dd in dd.children if other_dd.type != "page"]

        return pg
