__all__ = ["DomoGrant", "DomoGrants"]

from dataclasses import dataclass, field
from typing import List

import httpx

from ..client import DomoAuth as dmda
from ..routes import grant as grant_routes
from ..utils import DictDot as util_dd


@dataclass
class DomoGrant:
    id: str
    display_group: str = None
    title: str = None
    depends_on_ls: list[str] = None
    description: str = None
    role_membership_ls: list[str] = field(default=None)

    def __post_init__(self):
        self.id = str(self.id)

    def __eq__(self, other):
        if not isinstance(other, DomoGrant):
            return False

        return self.id == other.id

    @classmethod
    def _from_dict(cls, obj):
        dd = obj
        if not isinstance(dd, util_dd.DictDot):
            dd = util_dd.DictDot(obj)

        return cls(
            id=dd.authority,
            display_group=dd.authorityUIGroup,
            depends_on_ls=dd.dependsOnAuthorities,
            title=dd.title,
            description=dd.description,
            role_membership_ls=[str(role) for role in dd.roleIds],
        )


@dataclass
class DomoGrants:
    auth: dmda.DomoAuth = field(repr=False)

    grants: List[DomoGrant] = field(default=None)

    async def get(
        self,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        return_raw: bool = False,
    ):
        res = await grant_routes.get_grants(
            auth=self.auth, debug_api=debug_api, session=session
        )

        if return_raw or not res.is_success:
            return res

        self.grants = [DomoGrant._from_dict(obj) for obj in res.response]

        return self.grants
