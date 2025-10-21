__all__ = ["DomoAccessToken", "DomoAccessTokens"]

import asyncio
import datetime as dt
from dataclasses import dataclass, field
from typing import Any, List

import httpx

from ..client import entities as dmee
from ..routes import access_token as access_token_routes
from ..utils import chunk_execution as ce
from ..utils import convert as dmcv


@dataclass
class DomoAccessToken(dmee.DomoEntity):
    auth: DomoAuth = field(repr=False)
    id: int
    name: str
    owner: Any  # DomoUser
    expiration_date: dt.datetime
    token: str = field(repr=False)

    def __post_init__(self):
        if not isinstance(self.expiration_date, dt.datetime):
            self.expiration_date = dmcv.convert_epoch_millisecond_to_datetime(
                self.expiration_date
            )

    @property
    def days_till_expiration(self):
        return (self.expiration_date - dt.datetime.now()).days

    @property
    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/security/accesstokens"

    @classmethod
    async def from_dict(
        cls,
        auth: DomoAuth,
        obj: dict,
    ):
        from . import DomoUser as dmu

        owner = await dmu.DomoUser.get_by_id(user_id=obj["ownerId"], auth=auth)

        return cls(
            id=obj["id"],
            name=obj["name"],
            owner=owner,
            expiration_date=obj["expires"],
            auth=auth,
            token=obj.get("token"),
            raw=obj,
        )

    @classmethod
    async def get_by_id(
        cls,
        auth: DomoAuth,
        access_token_id: int,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        return_raw: bool = False,
    ):
        res = await access_token_routes.get_access_token_by_id(
            auth=auth,
            access_token_id=access_token_id,
            session=session,
            debug_api=debug_api,
            parent_class=cls.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return await cls.from_dict(obj=res.response, auth=auth)

    @classmethod
    async def generate(
        cls,
        duration_in_days: int,
        token_name: str,
        auth: DomoAuth,
        owner,  # DomoUser
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
        return_raw: bool = False,
    ):
        res = await access_token_routes.generate_access_token(
            user_id=owner.id,
            token_name=token_name,
            duration_in_days=duration_in_days,
            auth=auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=cls.__name__,
        )

        if return_raw:
            return res

        return await cls.from_dict(obj=res.response, auth=auth)

    async def revoke(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        return await access_token_routes.revoke_access_token(
            auth=self.auth,
            access_token_id=self.id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            session=session,
        )

    async def regenerate(
        self,
        session: httpx.AsyncClient = None,
        duration_in_days: int = 90,
        debug_api: bool = False,
        return_raw: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ):
        await self.revoke()

        await asyncio.sleep(3)

        new_token = await self.generate(
            duration_in_days=duration_in_days,
            token_name=self.name,
            auth=self.auth,
            owner=self.owner,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            return_raw=return_raw,
            parent_class=self.__class__.__name__,
        )

        self.id = new_token.id
        self.token = new_token.token
        self.expiration_date = new_token.expiration_date

        return self


@dataclass
class DomoAccessTokens(DomoManager):
    auth: DomoAuth = field(repr=False)

    domo_access_tokens: List[DomoAccessToken] = field(default=None)

    async def get(
        self,
        return_raw: bool = False,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        res = await access_token_routes.get_access_tokens(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return await ce.gather_with_concurrency(
            *[
                DomoAccessToken.from_dict(obj=obj, auth=self.auth)
                for obj in res.response
            ],
            n=10,
        )

    async def generate(
        self,
        duration_in_days: int,
        token_name: str,
        owner,  # DomoUser
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
        return_raw: bool = False,
    ):
        domo_access_token = await DomoAccessToken.generate(
            owner=owner,
            token_name=token_name,
            duration_in_days=duration_in_days,
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            return_raw=return_raw,
        )

        await self.get(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        return domo_access_token
