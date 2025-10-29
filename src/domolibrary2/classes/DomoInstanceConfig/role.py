__all__ = [
    "DomoRole",
    "SetRoleGrants_MissingGrants",
    "AddUser_Error",
    "DeleteRole_Error",
    "SearchRole_NotFound",
    "DomoRoles",
]


from dataclasses import dataclass, field
from typing import Any, Optional, List

import httpx

from ...client.auth import DomoAuth
from ...client.exceptions import ClassError
from ...entities.entities import DomoEntity, DomoManager
from ...entities.relationships import DomoRelationshipController
from ...routes import role as role_routes


class SetRoleGrants_MissingGrants(ClassError):
    def __init__(
        self, cls_instance, message: str = None, missing_grants: list[str] = None
    ):
        if missing_grants:
            message = f"role {cls_instance.name} is missing the following grants: {missing_grants}"
        super().__init__(cls_instance=cls_instance, message=message)


class AddUser_Error(ClassError):
    def __init__(self, cls_instance, user):
        message = f"user must either be a DomoUser object or provide user_id. received user: {user}, {type(user)}"
        super().__init__(cls_instance=cls_instance, message=message)


class DeleteRole_Error(ClassError):
    def __init__(self, cls_instance=None, message: str = "failure to delete role"):
        super().__init__(cls_instance=cls_instance, message=message)


class SearchRole_NotFound(ClassError):
    def __init__(self, cls_instance, role_name: str = ""):
        message = f"role {role_name} not found"
        super().__init__(cls_instance=cls_instance, message=message)


@dataclass
class DomoRole(
    DomoRelationshipController,
    DomoEntity,
):
    id: str
    name: str = field(default=None)
    description: Optional[str] = field(default=None)
    is_system_role: bool = None
    is_default_role: bool = None

    grants: list[Any] = field(default_factory=list)  # Will be DomoGrant objects
    membership: list = field(default_factory=list)

    # def __post_init__(self):
    #     super().__post_init__()

    @property
    def entity_type(self):
        return "ROLE"

    @property
    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/roles/{self.id}?tab=grants"

    def __post_init__(self):
        self.is_system_role = True if int(self.id or 0) <= 5 else False

        if self.grants:
            self.grants = self._valid_grants(self.grants)

    def _valid_grants(self, grants) -> list[Any]:
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
        cls, auth: DomoAuth, obj: dict, is_default_role: Optional[bool] = None
    ):
        return cls(
            auth=auth,
            id=obj.get("id", ""),
            name=obj.get("name"),
            description=obj.get("description"),
            is_system_role=obj.get("is_system_role", False),
            is_default_role=is_default_role,
            grants=obj.get("grants", []),
            raw=obj,
            Relations=None,
        )

    @classmethod
    async def get_entity_by_id(cls, entity_id, auth, **kwargs):
        return await cls.get_by_id(
            auth=auth,
            role_id=entity_id,
            **kwargs,
        )

    async def get(self):
        raise NotImplementedError("Subclasses must implement get method.")

    async def add_relationship(self):
        raise NotImplementedError("Subclasses must implement add_relationship method.")

    @classmethod
    async def get_by_id(
        cls,
        auth: DomoAuth,
        role_id: str,
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

    async def update(
        self,
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
        role_id: str = None,
        grants: list = None,
        is_replace: bool = True,
        session: Optional[httpx.AsyncClient] = None,
    ):
        from . import Role_Grant as dmgt

        all_grants = await self.get_grants(
            role_id=role_id or self.id,
            auth=self.auth,
            session=session,
        )

        all_grants_str = [g.grant for g in all_grants]

        if isinstance(grants[0], dmgt.DomoGrant):
            grants_str = [g.grant for g in grants]

        elif isinstance(grants[0], str):
            grants_str = grants

        missing_grants = [g for g in grants_str if g not in all_grants_str]

        if missing_grants:
            raise SetRoleGrants_MissingGrants(
                cls_instance=self, missing_grants=missing_grants
            )

        res = await role_routes.set_role_grants(
            auth=self.auth,
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
        user: Any = None,  # DomoUser
        session: Optional[httpx.AsyncClient] = None,
    ):
        from .. import DomoUser as dmdu

        if user_id is None:
            if isinstance(user, dmdu.DomoUser):
                user_id = user.id
            else:
                raise ValueError("must either provide a user_id or user : DomoUser")

        res = await role_routes.role_membership_add_users(
            auth=auth,
            role_id=self.id,
            user_ids=[user_id],
            session=session,
        )

        self.membership.append(user_id)

        return res

    async def set_as_default_role(
        self,
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

    @classmethod
    async def create(
        cls,
        auth: DomoAuth,
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

        self.membership = [
            dmdu.DomoUser.from_dict(obj=obj, auth=auth) for obj in res.response
        ]
        return self.membership

    async def delete(
        self,
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


@dataclass
class DomoRoles(DomoManager):
    default_role: DomoRole = None
    roles: List[DomoRole] = field(default=None)

    async def get(
        self,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ) -> List[DomoRole]:
        res = await role_routes.get_roles(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            parent_cls=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        self.roles = [
            DomoRole.from_dict(obj=obj, auth=self.auth) for obj in res.response
        ]
        return self.roles

    async def by_name(
        self,
        search_name: str,
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        is_suppress_error: bool = False,
        debug_num_stacks_to_drop: int = 3,
    ) -> DomoRole:
        await self.get(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop - 1,
        )

        match_role = next(
            (r for r in self.roles if search_name.lower() in r.name.lower()), None
        )

        if not match_role and not is_suppress_error:
            raise SearchRole_NotFound(cls_instance=self, role_name=search_name)

        return match_role

    async def upsert(
        self,
        name: str,
        description: str = None,
        grants: List["DomoGrant"] = None,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_prn: bool = False,
        debug_num_stacks_to_drop=2,
    ):
        domo_role = None
        try:
            domo_role = await self.by_name(
                search_name=name,
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

    async def get_default_role(
        self, debug_api=False, session=None, debug_num_stacks_to_drop=2
    ):
        # First get the default role ID
        res = await role_routes.get_default_role(
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        # res.response is the role ID, now get the full role details
        default_role_id = res.response

        # Get the full role object by ID
        self.default_role = await DomoRole.get_by_id(
            auth=self.auth,
            role_id=default_role_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        return self.default_role
