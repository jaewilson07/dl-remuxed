"""Page management and collection operations."""

__all__ = ["DomoPages"]

from dataclasses import dataclass, field
from typing import list

import httpx

from ...client import exceptions as dmde
from ...client.auth import DomoAuth
from ...routes import page as page_routes
from ...utils import chunk_execution as dmce
from .core import DomoPage


@dataclass
class DomoPages:
    auth: DomoAuth = field(repr=False)
    pages: list[DomoPage] = None

    async def get(self, **kwargs):
        """calls get_admin_summary to retrieve all pages in an instance"""
        return await self.get_admin_summary(**kwargs)

    async def get_admin_summary(
        self,
        search_title: str = None,
        parent_page_id: int = None,
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        """use admin_summary to retrieve all pages in an instance -- regardless of user access
        NOTE: some Page APIs will not return results if page access isn't explicitly shared
        """

        res = await page_routes.get_pages_adminsummary(
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            search_title=search_title,
            page_parent_id=parent_page_id,
        )

        if return_raw:
            return res

        self.pages = await dmce.gather_with_concurrency(
            n=60,
            *[
                DomoPage._from_adminsummary(
                    page_obj, auth=self.auth, debug_api=debug_api, session=session
                )
                for page_obj in res.response
            ],
        )

        return self.pages


async def get_children(self: DomoPage, is_suppress_errors: bool = False):
    async def _get_children_recur(parent_page, is_suppress_errors: bool = False):
        parent_page.children = parent_page.children or []

        try:
            child_pages = await DomoPages(auth=parent_page.auth).get(
                parent_page_id=parent_page.id,
                # is_suppress_errors=is_suppress_errors
            )

            parent_page.children = [
                child
                for child in child_pages
                if child is not None and child.parent_page_id == parent_page.id
            ]

            await dmce.gather_with_concurrency(
                n=10,
                *[
                    _get_children_recur(
                        parent_page=cp,
                        is_suppress_errors=is_suppress_errors,
                    )
                    for cp in parent_page.children
                ],
            )

            return self.children

        except dmde.DomoError as e:
            print(
                f"cannot access child page -- https://{parent_page.auth.domo_instance}.domo.com/page/{parent_page.id} -- is it shared\nwith you?"
            )
            if not is_suppress_errors:
                raise e from e

    self.children = await _get_children_recur(
        parent_page=self,
        is_suppress_errors=is_suppress_errors,
    )

    return self.children


def flatten_children(self: DomoPage, path=None, hierarchy=0, results=None):
    results = results or []

    path = f"{path} > {self.title}" if path else self.title

    results.append({"hierarchy": hierarchy, "path": path, "page": self})

    if self.children:
        [
            child.flatten_children(path, hierarchy + 1, results)
            for child in self.children
        ]

    return results


async def get_parents(self: DomoPage, page=None):
    page = page or self

    if not page.parent_page_id:
        return self.custom_attributes

    if not self.top_page_id:
        page_as = next(
            pg
            for pg in (await DomoPages(auth=self.auth).get(search_title=page.id))
            if pg.id == page.id
        )
        page.top_page_id = page_as.top_page_id
        self.top_page = page_as

    if page.id == page.top_page_id:
        self.custom_attributes["top_page"] = page

    parent_page_as = next(
        pg
        for pg in (
            await DomoPages(auth=self.auth).get(search_title=page.parent_page_id)
        )
        if pg.id == page.parent_page_id
    )

    if self.parent_page_id == parent_page_as.id:
        self.parent_page = parent_page_as

    page.custom_attributes["parent_page"] = parent_page_as

    if not self.custom_attributes.get("path"):
        self.custom_attributes["path"] = []

    self.custom_attributes["path"].append(parent_page_as)

    if page.id != self.top_page_id:
        await self.get_parents(page=parent_page_as)

    return self.custom_attributes
