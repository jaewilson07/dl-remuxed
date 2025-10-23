__all__ = [
    "DomoRole",
    "SetRoleGrants_MissingGrants",
    "AddUser_Error",
    "DeleteRole_Error",
    "SearchRole_NotFound",
    "DomoRoles",
]


import asyncio
from dataclasses import dataclass, field
from typing import Any, List, Optional

import httpx
<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
from nbdev.showdoc import patch_to

from . import DomoGrant as dmgt
from . import DomoUser as dmdu
from ..client.auth import DomoAuth
from ..client.entities import DomoEntity
from ..client.exceptions import DomoError
from ..routes import role as role_routes
from . import DomoGrant as dmgt
from . import DomoUser as dmdu


@dataclass
class DomoRole(dmee.DomoEntity):
========

from ...client import exceptions as dmde
from ...client.auth import DomoAuth
from ...client.entities import DomoEntity, DomoManager
from ...client.exceptions import ClassError, DomoError
from ...routes import role as role_routes


class SetRoleGrants_MissingGrants(ClassError):
    def __init__(
        self, cls_instance, message: str = None, missing_grants: List[str] = None
    ):
        # from . import Role_Grant as dmgt

        # # validate if grants is a list of DomoGrant objects
        # if not isinstance(grants[0], dmgt.DomoGrant):
        #     message = f"grants must be a list of DomoGrant objects.  provided grants are {type(grants[0])}"
        #     super().__init__(message)

        # missing_grants = []

        # role_grants = [g.grant for g in role.grants]

        # for grant in grants:
        #     if grant.grant not in role_grants:
        #         missing_grants.append(grant.grant)

        if missing_grants:
            message = f"role {cls_instance.name} is missing the following grants: {missing_grants}"
        super().__init__(cls_instance=cls_instance, message=message)


@dataclass
class DomoRole(DomoEntity):
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======

from ...client import exceptions as dmde
from ...client.auth import DomoAuth
from ...entities.entities import DomoEntity, DomoManager
from ...client.exceptions import ClassError, DomoError
from ...routes import role as role_routes


class SetRoleGrants_MissingGrants(ClassError):
    def __init__(
        self, cls_instance, message: str = None, missing_grants: List[str] = None
    ):
        # from . import Role_Grant as dmgt

        # # validate if grants is a list of DomoGrant objects
        # if not isinstance(grants[0], dmgt.DomoGrant):
        #     message = f"grants must be a list of DomoGrant objects.  provided grants are {type(grants[0])}"
        #     super().__init__(message)

        # missing_grants = []

        # role_grants = [g.grant for g in role.grants]

        # for grant in grants:
        #     if grant.grant not in role_grants:
        #         missing_grants.append(grant.grant)

        if missing_grants:
            message = f"role {cls_instance.name} is missing the following grants: {missing_grants}"
        super().__init__(cls_instance=cls_instance, message=message)


@dataclass
class DomoRole(DomoEntity):
>>>>>>> main
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    is_system_role: bool = False
    is_default_role: bool = False

    grants: List[Any] = field(default_factory=list)  # Will be DomoGrant objects
    membership_ls: list = field(default_factory=list)

    @property
    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/roles/{self.id}?tab=grants"

    def __post_init__(self):
        self.is_system_role = True if int(self.id or 0) <= 5 else False

        if self.grants:
            self.grants = self._valid_grants(self.grants)

    def _valid_grants(self, grants) -> List[Any]:
        """Convert grant strings or objects to DomoGrant objects."""

        from . import Role_Grant as dmgt

        if not grants:
            return []

        if isinstance(grants[0], str):
            return [dmgt.DomoGrant(grant_str) for grant_str in grants]
        elif (
            hasattr(grants[0], "__class__")
            and grants[0].__class__.__name__ == "DomoGrant"
        ):
            return grants
        else:
            return []

    @classmethod
    def from_dict(
        cls, obj: dict, auth: DomoAuth = None, is_default_role: Optional[bool] = None
    ):
        return (
            cls(
                auth=auth,
                id=obj.get("id", ""),
                name=obj.get("name"),
                description=obj.get("description"),
                is_system_role=obj.get("is_system_role", False),
                is_default_role=is_default_role,
                grants=obj.get("grants", []),
                raw=obj,
            ),
        )

    @classmethod
    async def get_by_id(
        cls,
        role_id: str,
        auth: DomoAuth,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ):
        res = await role_routes.get_role_by_id(
            auth=auth,
            role_id=role_id,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        return cls.from_dict(obj=res.response, auth=auth)

    async def get_grants(
        self,
        auth: DomoAuth = None,
        role_id: Optional[str] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> List[Any]:  # Returns List[DomoGrant]
        from . import Role_Grant as dmgt

        res = await role_routes.get_role_grants(
            auth=auth,
            role_id=role_id or self.id,
            debug_api=debug_api,
            session=session,
        )

        self.grants = [dmgt.DomoGrant(obj) for obj in res.response]

        return self.grants

    async def set_grants(
        self,
        auth: DomoAuth,
        role_id: str = None,
        grants: list = None,
        is_replace: bool = True,
        session: Optional[httpx.AsyncClient] = None,
    ):
        from . import Role_Grant as dmgt

        all_grants = await self.get_grants(
            role_id=role_id or self.id,
            auth=auth,
            session=session,
        )

        all_grants_str = [g.grant for g in all_grants]

        if isinstance(grants[0], dmgt.DomoGrant):
            grants_str = [g.grant for g in grants]

        elif isinstance(grants[0], str):
            grants_str = grants

        missing_grants = [g for g in grants_str if g not in all_grants_str]

        if missing_grants:
            raise SetRoleGrants_MissingGrants(role=self, grants=grants)

        res = await role_routes.set_role_grants(
            auth=auth,
            role_id=role_id or self.id,
            grants=grants_str,
            is_replace=is_replace,
            session=session,
        )

        return res

    async def add_user(
        self,
        auth: DomoAuth,
        user_id: str = None,
        user: "DomoUser" = None,
        session: Optional[httpx.AsyncClient] = None,
    ):
        from .. import DomoUser as dmdu

        if user_id is None:
            if isinstance(user, dmdu.DomoUser):
                user_id = user.id
            else:
                raise AddUser_Error(user=user)

        res = await role_routes.add_user_to_role(
            auth=auth,
            role_id=self.id,
            user_id=user_id,
            session=session,
        )

        self.membership_ls.append(user_id)

        return res

    async def delete(
        self,
        auth: DomoAuth = None,
        role_id: str = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ):
        res = await role_routes.delete_role(
            auth=auth,
            role_id=role_id or self.id,
            debug_api=debug_api,
            session=session,
        )

        return res


class AddUser_Error(ClassError):
    def __init__(self, user):
        message = f"user must either be a DomoUser object or provide user_id. received user: {user}, {type(user)}"
        super().__init__(message)


class DeleteRole_Error(ClassError):
    def __init__(self, role: DomoRole = None, message: str = "failure to delete role"):
        super().__init__(message)


class SearchRole_NotFound(ClassError):
    def __init__(self, role_name: str = ""):
        message = f"role {role_name} not found"
        super().__init__(message)


class DomoRoles:
    def __init__(self, auth: DomoAuth):
        self.auth = auth

    @classmethod
    async def get_all(
        cls,
        auth: DomoAuth,
        session: Optional[httpx.AsyncClient] = None,
    ) -> List[DomoRole]:
        res = await role_routes.get_all_roles(auth=auth, session=session)

        return [DomoRole.from_dict(obj=obj, auth=auth) for obj in res.response]

    @classmethod
    async def search_by_name(
        cls,
        auth: DomoAuth,
        name_query: str,
        session: Optional[httpx.AsyncClient] = None,
    ) -> DomoRole:
        all_roles = await cls.get_all(auth=auth, session=session)

        role_obj = next((r for r in all_roles if r.name == name_query), None)

        if not role_obj:
            raise SearchRole_NotFound(role_name=name_query)

        return role_obj

    # def _from_str(cls, id, name, description=None, auth: DomoAuth = None):

    #     return cls(id=id,
    #             name=name,
    #             description=description,
    #             auth=auth
    #             )

    @classmethod
<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
    def from_dict(cls, obj: dict, auth=dmda.DomoAuth, is_default_role=None):
========
    def from_dict(cls, obj: dict, auth=DomoAuth, is_default_role=None):
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
    def from_dict(cls, obj: dict, auth=DomoAuth, is_default_role=None):
>>>>>>> main
        return cls(
            id=obj.get("id"),
            name=obj.get("name"),
            description=obj.get("description"),
            auth=auth,
            is_default_role=is_default_role,
            raw=obj,
        )

    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/roles/{self.id}?tab=grants"

    @classmethod
    async def get_by_id(
        cls,
        role_id: int,
        auth: DomoAuth,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        return_raw: bool = False,
    ):
        res = await role_routes.get_role_by_id(
            role_id=role_id,
            auth=auth,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            session=session,
            parent_class=cls.__name__,
        )

        if return_raw:
            return res.response

        return cls.from_dict(obj=res.response, auth=auth)
<<<<<<< HEAD


<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======


>>>>>>> main
async def get_grants(
    self: DomoRole,
    auth: DomoAuth = None,
    role_id: str = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
) -> List["DomoGrant"]:
    auth = auth or self.auth
    role_id = role_id or self.id

    from . import Role_Grant as dmgt

    res = await role_routes.get_role_grants(
        auth=auth,
        role_id=role_id,
        debug_api=debug_api,
        session=session,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    self.grants = [dmgt.DomoGrant(obj) for obj in res.response]

    return self.grants


class SetRoleGrants_MissingGrants(dmde.ClassError):
    def __init__(self, cls_instance, missing_grants: List[str]):
        super().__init__(
            cls_instance=cls_instance,
            message=f"failed to add grants: {', '.join(missing_grants)}",
        )


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def set_grants(
    self: DomoRole,
    grants: List["DomoGrant"],
    debug_api: bool = False,
    debug_num_stacks_to_drop: bool = 2,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    valid_grants = self._valid_grants(grants)

    res = await role_routes.set_role_grants(
        auth=self.auth,
        role_id=self.id,
        role_grant_ls=[domo_grant.id for domo_grant in valid_grants],
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=self.__class__.__name__,
    )

    if return_raw:
        return res

    # validate grants
    await asyncio.sleep(2)

    all_grants = await self.get_grants(
        auth=self.auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    missing_grants = [grant.id for grant in valid_grants if grant not in all_grants]

    if missing_grants:
        raise SetRoleGrants_MissingGrants(
            cls_instance=self,
            missing_grants=missing_grants,
        )

    return self.grants


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole, cls_method=True)
async def create(
    cls,
    auth: dmda.DomoAuth,
========
async def create(
    cls,
    auth: DomoAuth,
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
async def create(
    cls,
    auth: DomoAuth,
>>>>>>> main
    name: str,
    description,
    grants: List[Any],  # DomoGrants
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
    return_raw: bool = False,
):
    res = await role_routes.create_role(
        auth=auth,
        name=name,
        description=description,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=cls.__name__,
    )

    if return_raw:
        return res

    domo_role = cls.from_dict(obj=res.response, auth=auth)

    if grants:
        await domo_role.set_grants(grants=grants)

    return domo_role


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def get_membership(
    self,
    role_id=None,
    auth: DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    from .. import DomoUser as dmdu

    auth = auth or self.auth
    role_id = role_id or self.id

    res = await role_routes.get_role_membership(
        auth=auth,
        role_id=role_id,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res.response

    membership_ls = [
        dmdu.DomoUser._from_search_json(obj=obj, auth=auth) for obj in res.response
    ]

    self.membership_ls = membership_ls

    return membership_ls


class AddUser_Error(dmde.ClassError):
    def __init__(self, cls_instance, user_id, user_name=None):
        user_str = f"{user_id} - {user_name}" if user_name else user_id
        super().__init__(
            cls_instance=cls_instance,
            message=f"unable to add {user_str} to role {role_id}",
        )


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def add_user(
    self,
    user: "DomoUser",
    role_id: str = None,
    auth: DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 2,
):
    role_id = role_id or self.id
    auth = auth or self.auth

    await role_routes.role_membership_add_users(
        auth=auth,
        role_id=role_id,
        user_list=[user.id],
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    domo_members = await self.get_membership(
        auth=auth or self.auth,
        role_id=role_id or self.id,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )
    self.membership_ls = domo_members

    if user not in domo_members:
        raise AddUser_Error(
            cls_instance=self,
            user_id=user.id,
            user_name=user.display_name,
        )

    return domo_members


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def update(
    self: DomoRole,
    name=None,
    description: str = None,
    grants: List["DomoGrant"] = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
):
    name = name or self.name
    description = description or self.description

    res = await role_routes.update_role_metadata(
        role_id=self.id,
        role_name=name,
        role_description=description,
        auth=self.auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    self.name = name
    self.description = description

    if grants:
        await self.set_grants(grants)

    if return_raw:
        return res

    return self


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
class DeleteRole_Error(dmde.DomoError):
========
class DeleteRole_Error(DomoError):
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
class DeleteRole_Error(DomoError):
>>>>>>> main
    def __init__(self, cls_instance):
        super().__init__(
            cls_instance=cls_instance, message="role not deleted -- does it exist?"
        )


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def delete(
    self: DomoRole,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    return await role_routes.delete_role(
        role_id=self.id,
        auth=self.auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole, cls_method=True)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def delete_role(
    cls: DomoRole,
    role_id: int,
    auth: DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    res = await role_routes.get_roles(
        auth=auth,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        debug_api=debug_api,
    )

    domo_role = next((role for role in res.response if role.get("id") == role_id), None)

    if not domo_role:
        raise DeleteRole_Error(role_id=role_id, domo_instance=auth.domo_instance)

    return await role_routes.delete_role(
        role_id=role_id,
        auth=auth,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )


class SearchRole_NotFound(dmde.ClassError):
    def __init__(self, cls_instance, role_id, message="not found"):
        super().__init__(
            cls_instance=cls_instance,
            message=message,
            entity_id=role_id,
        )


@dataclass
<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
class DomoRoles(dmee.DomoManager):
========
class DomoRoles(DomoManager):
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
class DomoRoles(DomoManager):
>>>>>>> main
    roles: List[DomoRole] = field(default=None)

    default_role: DomoRole = field(default=None)

    async def get_default_role(
        self,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        return_raw: bool = False,
    ) -> DomoRole:
        res = await role_routes.get_default_role(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        self.default_role = await DomoRole.get_by_id(
            role_id=res.response,
            auth=self.auth,
            session=session,
            debug_api=debug_api,
        )

        return self.default_role

    async def get(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ):
        res = await role_routes.get_roles(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        await self.get_default_role()

        self.roles = [
            DomoRole.from_dict(
                obj=obj,
                auth=self.auth,
                is_default_role=obj["id"] == self.default_role.id,
            )
            for obj in res.response
        ]

        return self.roles

    async def search_by_name(
        self,
        role_name: str = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        debug_num_stacks_to_drop=2,
    ):
        domo_roles = await self.get(
            debug_api=debug_api,
            session=session,
            return_raw=return_raw,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return domo_roles

        domo_role = next(
            (role for role in domo_roles if role.name.lower() == role_name.lower()),
            None,
        )

        if not domo_role:
            raise SearchRole_NotFound(cls_instance=self, role_id=role_name)

        return domo_role


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRoles)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def create(
    self: DomoRoles,
    name: str,
    grants: List["DomoGrant"] = None,
    description: str = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    domo_role = await DomoRole.create(
        auth=auth,
        name=name,
        description=description,
        grants=grants,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
    )

    await self.get()
    return domo_role


async def upsert(
    self: DomoRoles,
    name: str,
    description: str = None,
<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
    grants: List[dmgt.DomoGrant] = None,
========
    grants: List["DomoGrant"] = None,
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
    grants: List["DomoGrant"] = None,
>>>>>>> main
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_prn: bool = False,
    debug_num_stacks_to_drop=2,
):
    domo_role = None
    try:
        domo_role = await self.search_by_name(
            role_name=name,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        if debug_prn:
            print(f"updating role {name}")

        await domo_role.update(
            description=description,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            session=session,
        )

        if grants:
            await domo_role.set_grants(
                grants=grants,
            )

    except SearchRole_NotFound:
        if debug_prn:
            print(f"Creating - {name}")

        domo_role = await DomoRole.create(
            name=name,
            description=description,
            auth=self.auth,
            grants=grants,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            session=session,
        )

    await self.get()

    return domo_role


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoRole.py
@patch_to(DomoRole)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/Role.py
=======
>>>>>>> main
async def set_as_default_role(
    self: DomoRole,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 2,
):
    return await role_routes.set_default_role(
        auth=self.auth,
        role_id=self.id,
        debug_api=debug_api,
        session=session,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )
