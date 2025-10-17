"""preferred response class for all API requests"""


__all__ = [
    "DomoBase",
    "DomoEntity",
    "DomoEntity_w_Lineage",
    "DomoFederatedEntity",
    "DomoPublishedEntity",
    "DomoManager",
    "DomoSubEntity",
    "Entity_Relation",
]

# | export


import abc
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Callable

import httpx

from . import DomoAuth as dmda
from ..utils.convert import convert_snake_to_pascal


class DomoEnum(Enum):

    @classmethod
    def get(cls, value):

        for member in cls:
            if member.name.lower() == value.lower():
                return member

        return cls.default

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.name.lower() == value.lower():
                return member

        return cls.default


@dataclass
class DomoBase(abc.ABC):
    pass


@dataclass
class DomoEntity(DomoBase):
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    raw: dict = field(repr=False)  # api representation of the class

    def __eq__(self, other):
        if isinstance(other, DomoEntity):
            return self.id == other.id

        return False

    def to_dict(self, override_fn: Callable = None) -> dict:
        """takes all attributes of the dataclass and returns them as a dictionary in pascalCase"""

        if override_fn:
            return override_fn(self)

        return {
            convert_snake_to_pascal(field.name): getattr(self, field.name)
            for field in fields(self)
        }

    @classmethod
    @abc.abstractmethod
    def _from_dict(cls):
        raise NotImplementedError("This method should be implemented by subclasses.")

    @classmethod
    @abc.abstractmethod
    async def get_by_id(cls, auth: dmda.DomoAuth, entity_id: str):
        """
        Fetches an entity by its ID.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abc.abstractmethod
    def display_url(self) -> str:
        """
        Returns the URL to display the entity in Domo.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoEntity_w_Lineage(DomoEntity):

    Lineage: Any = field(repr=False)

    def __post_init__(self):
        from ..classes import DomoLineage as dmdl

        self.Lineage = dmdl.DomoLineage._from_parent(auth=self.auth, parent=self)

    @classmethod
    @abc.abstractmethod
    async def _get_entity_by_id(cls, auth: dmda.DomoAuth, entity_id: str):
        """
        Fetches an entity by its ID.
        This method should be implemented by subclasses to fetch the specific entity type.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoFederatedEntity(DomoEntity_w_Lineage):

    @abc.abstractmethod
    async def get_federated_parent(
        self, parent_auth=None, parent_auth_retrieval_fn: Callable = None
    ):
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoPublishedEntity(DomoFederatedEntity):
    subscription: Any = field(repr=False)
    parent_publication: Any = field(repr=False)

    @abc.abstractmethod
    async def get_subscription(self):

        # self.subscription = ... ## should return one subscirption
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abc.abstractmethod
    async def get_parent_publication(
        self, parent_auth=None, parent_auth_retreival_fn=None
    ):

        # if not self.subscription:
        #     await get_subscription()

        # if not parent_auth:
        #     if not parent_auth_retreival_fn:
        #         raise ValueError("Either parent_auth or parent_auth_retreival_fn must be provided.")
        #     parent_auth = parent_auth_retreival_fn(self.subscription)

        # self.parent_publication = ... (parent_auth) ## should return the parent publication
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abc.abstractmethod
    async def get_parent_content_details(self, parent_auth=None):
        """the parent dataset, card or page..."""

        # if not self.parent_publication:
        #     self.get_parent_publication(parent_auth)

        raise NotImplementedError("This method should be implemented by subclasses.")

    async def get_federated_prent(self, parent_auth):
        raise NotImplementedError


@dataclass
class DomoManager(DomoBase):
    auth: dmda.DomoAuth = field(repr=False)

    @abc.abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")


@dataclass
class DomoSubEntity(DomoBase):
    auth: dmda.DomoAuth = field(repr=False)
    parent: Any
    parent_id: str
    # raw : dict = field(repr=False, default=None) # api representation of the class

    def __post_init__(self):
        if self.parent:
            self.auth = self.parent.auth
            self.parent_id = self.parent.id

    @classmethod
    def _from_parent(cls, parent: DomoEntity):
        return cls(auth=parent.auth, parent=parent, parent_id=parent.id)


@dataclass
class Entity_Relation:
    auth: dmda.DomoAuth = field(repr=False)
    entity: Any
    relation_type: str

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False

        return (
            self.entity.id == other.entity.id
            and self.relation_type == other.relation_type
        )

    @classmethod
    async def _from_user_id(
        cls,
        user_id,
        relation_type: str,
        auth: dmda.DomoAuth,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
    ):

        # if entity_type == "USER":
        from ..classes import DomoUser as dmdu

        domo_user = await dmdu.DomoUser.get_by_id(
            user_id=user_id,
            auth=auth,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        return cls(entity=domo_user, relation_type=relation_type, auth=auth)

    @classmethod
    async def _from_group_id(
        cls,
        group_id,
        relation_type,
        auth: dmda.DomoAuth,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
    ):

        from ..classes import DomoGroup as dmdg

        domo_group = await dmdg.DomoGroup.get_by_id(
            group_id=group_id,
            auth=auth,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        return cls(entity=domo_group, relation_type=relation_type, auth=auth)