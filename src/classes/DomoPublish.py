from __future__ import annotations

import datetime as dt
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Union, TYPE_CHECKING

import httpx
import pandas as pd

from . import DomoLineage as dmdl
from ..client import auth as dmda
from ..client import entities as dmen
from ..client import exceptions as dmde
from ..client.DomoEntity import DomoEntity_w_Lineage, DomoEnum
from ..routes import publish as publish_routes
from ..utils import chunk_execution as dmce
from ..client.entities import DomoEntity_w_Lineage, DomoEnum

if TYPE_CHECKING:
    from . import DomoCard, DomoDataset, DomoPage

__all__ = [
    "DomoPublication_Content_Enum",
    "DomoPublication_Content",
    "DomoPublication_UnexpectedContentType",
    "DomoPublication",
    "DomoSubscription_NoParentAuth",
    "DomoSubscription_NoParent",
    "DomoSubscription",
    "DomoEverywhere",
]


class DomoPublication_Content_Enum(DomoEnum):
    from . import DomoAppStudio as dmas
    from . import DomoCard as dmac
    from . import DomoDataset as dmdc
    from . import DomoPage as dmpg

    CARD = dmac.DomoCard
    DATASET = dmdc.DomoDataset
    DATA_APP = dmas.DomoAppStudio
    PAGE = dmpg.DomoPage


@dataclass
class DomoPublication_Content:
    auth: dmda.DomoAuth

    content_id: str
    entity_type: str
    entity_id: str
    entity_domain: str
    is_v2: bool
    is_direct_content: bool

    created_dt: dt.datetime
    updated_dt: dt.datetime = None

    subscriber_content_id: str = None
    subscriber_insance: str = None

    entity: Any = field(repr=False, default=None)
    parent: Any = field(repr=False, default=None)

    """the publication content is the content from the publisher instance that is being distributed to subscribers"""

    @classmethod
    def from_dict(cls, obj: dict, auth: dmda.DomoAuth, parent: Any = None):
        entity_type = obj.get("content").get("type")
        return cls(
            auth=auth,
            content_id=obj["id"],
            entity_id=obj.get("content").get("domoObjectId"),
            entity_domain=obj.get("content").get("domain"),
            is_v2=obj.get("isV2"),
            created_dt=(
                dt.datetime.fromtimestamp(obj["created"] / 1000)
                if obj["created"]
                else None
            ),
            updated_dt=(
                dt.datetime.fromtimestamp(obj.get("content").get("updated") / 1000)
                if obj.get("content").get("updated")
                else None
            ),
            is_direct_content=obj.get("useDirectContent"),
            parent=parent,
            entity_type=entity_type,
            entity=DomoPublication_Content_Enum[entity_type].value,
        )

    async def get_entity(
        self, debug_api: bool = False, session: httpx.AsyncClient = None
    ):
        """get the entity from the publication content"""
        if not self.entity:
            self.entity = DomoPublication_Content_Enum[self.entity_type].value

        self.entity = await self.entity._get_entity_by_id(
            auth=self.auth,
            entity_id=self.entity_id,
            debug_api=debug_api,
            session=session,
        )

        return self.entity

    def to_api_json(self):
        return {
            "domain": self.entity_domain,
            "domoObjectId": self.entity_id,
            "customerId": self.entity_domain,
            "type": self.entity_type,
        }


class DomoPublication_UnexpectedContentType(dmde.ClassError):
    def __init__(self, cls_instance, content_type):
        super().__init__(
            cls_instance=cls_instance,
            message=f"DomoPublication_Instantiation: Unexpected content type {content_type}",
        )


@dataclass
class DomoPublication(DomoEntity_w_Lineage):
    name: str
    description: str
    is_v2: bool
    created_dt: dt.datetime

    updated_dt: dt.datetime = None

    subscriptions: List[DomoSubscription] = None

    content: List[DomoPublication_Content] = None

    # content_page_id_ls: List[str] = default = None
    # content_dataset_id_ls: List[str] = field(default_factory=list)
    # content_data_app_id_ls: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.Lineage = dmdl.DomoLineage_Publication.from_parent(
            parent=self, auth=self.auth
        )

    def _generate_subscriptions(self, subscription_authorizations_ls, auth):
        self.subscriptions = [
            DomoSubscription.from_dict(obj=sub, auth=auth, parent_publication=self)
            for sub in subscription_authorizations_ls
        ]

    def _generate_content(self, children_ls):
        self.content = [
            DomoPublication_Content.from_dict(child, auth=self.auth, parent=self)
            for child in children_ls
        ]

        return self.content

    @classmethod
    def from_dict(cls, obj, auth: dmda.DomoAuth):
        domo_pub = cls(
            id=obj["id"],
            name=obj["name"],
            description=obj["description"],
            created_dt=(
                dt.datetime.fromtimestamp(obj["created"] / 1000)
                if obj["created"]
                else None
            ),
            updated_dt=(
                dt.datetime.fromtimestamp(obj.get("content").get("updated") / 1000)
                if obj.get("content").get("updated")
                else None
            ),
            is_v2=obj["isV2"],
            auth=auth,
            raw=obj,
            Lineage=None,
        )

        if (
            obj.get("subscriptionAuthorizations")
            and len(obj.get("subscriptionAuthorizations")) > 0
        ):
            domo_pub._generate_subscriptions(
                subscription_authorizations_ls=obj["subscriptionAuthorizations"],
                auth=auth,
            )

        if obj.get("children") and len(obj.get("children")) > 0:
            domo_pub._generate_content(obj["children"])

        return domo_pub

    @classmethod
    async def get_by_id(
        cls,
        publication_id,
        auth: dmda.DomoAuth,
        return_raw: bool = False,
        timeout=10,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        res = await publish_routes.get_publication_by_id(
            auth=auth,
            publication_id=publication_id,
            timeout=timeout,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            session=session,
            parent_class=cls.__name__,
        )

        if return_raw:
            return res

        return cls.from_dict(obj=res.response, auth=auth)

    @classmethod
    async def _get_entity_by_id(cls, entity_id, **kwargs):
        return await cls.get_by_id(publication_id=entity_id, **kwargs)

    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/domo-everywhere/publications/details?id={self.id}"

    async def get_content_details(
        self,
        subscriber_domain: str,  # must include .domo.com
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        if not subscriber_domain.lower().endswith(".domo.com"):
            subscriber_domain = f"{subscriber_domain}.domo.com"

        res = await publish_routes.get_subscriber_content_details(
            auth=self.auth,
            publication_id=self.id,
            subscriber_instance=subscriber_domain,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
        )

        return res

    async def get_publication_entity_by_subscriber_entity(
        self,
        subscriber_domain: str,
        subscriber: "Union[DomoCard, DomoDataset, DomoPage]",
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
        is_suppress_errors: bool = False,
    ) -> "Union[DomoCard, DomoDataset, DomoPage, None]":

        res = await self.get_content_details(
            subscriber_domain=subscriber_domain,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        obj = next(
            (row for row in res.response if row["subscriberObjectId"] == subscriber.id),
            None,
        )

        if not obj:
            if not is_suppress_errors:
                pass
                # raise dmde.DomoError(
                #         =self,
                #         message=f"get_publication_entity_by_subscriber_entity: No matching publication content found for subscriber id {subscriber.id} in publication id {self.id}",
                #     )
            return None

        return await subscriber._get_entity_by_id(
            entity_id=obj["publisherObjectId"], auth=self.auth
        )

    @classmethod
    async def create_publication(
        cls,
        auth: "dmda.DomoAuth",
        name: str,
        content_ls: List["DomoPublication_Content"],
        subscription_ls: List["DomoSubscription"],
        unique_id: str = None,
        description: str = None,
        debug_api: bool = False,
    ):

        if not isinstance(subscription_ls, list):
            subscription_ls = [subscription_ls]

        domain_ls = []
        content_json_ls = []
        for sub in subscription_ls:
            domain_ls.append(sub.subscriber_domain)
        for content_item in content_ls:
            content_json_ls.append(content_item.to_api_json())

        unique_id = unique_id or str(uuid.uuid4())

        body = publish_routes.generate_publish_body(
            url=f"{auth.domo_instance}.domo.com",
            sub_domain_ls=domain_ls,
            content_ls=content_json_ls,
            name=name,
            unique_id=unique_id,
            description=description or "",
            is_new=True,
        )

        res = await publish_routes.create_publish_job(
            auth=auth, body=body, debug_api=debug_api
        )

        return cls.from_dict(obj=res.response, auth=auth)

    async def get_content_details(
        self,
        subscriber_domain: str = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):

        res = await publish_routes.get_publication_by_id(
            auth=self.auth,
            publication_id=self.id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
        )

        # Extract subscription details
        if subscriber_domain:
            subscription_auth = next(
                (
                    sub
                    for sub in res.response.get("subscriptionAuthorizations", [])
                    if sub.get("subscriberDomain") == subscriber_domain
                ),
                None,
            )
            if subscription_auth:
                res.response = subscription_auth
            else:
                res.response = []

        return res

    async def revoke_subscription_auth(
        self,
        auth: "dmda.DomoAuth" = None,
        subscription_id: str = None,
        subscription: "DomoSubscription" = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):

        # Note: This function may not have a direct route implementation
        # It would need to be implemented based on the available API endpoints
        auth = auth or self.auth
        subscription_id = subscription_id or subscription.id

        # This is a placeholder implementation - would need actual API route
        raise NotImplementedError("revoke_subscription_auth route not yet implemented")

    async def update_publication(
        self,
        auth: "dmda.DomoAuth" = None,
        content_ls: List["DomoPublication_Content"] = None,
        description: str = None,
        name: str = None,
        subscription_ls: List["DomoSubscription"] = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):

        auth = auth or self.auth

        # Use the actual available route
        if not isinstance(subscription_ls, list) and subscription_ls:
            subscription_ls = [subscription_ls]

        domain_ls = []
        content_json_ls = []

        if subscription_ls:
            for sub in subscription_ls:
                domain_ls.append(sub.subscriber_domain)

        if content_ls:
            for content_item in content_ls:
                content_json_ls.append(content_item.to_api_json())

        body = publish_routes.generate_publish_body(
            url=f"{auth.domo_instance}.domo.com",
            sub_domain_ls=domain_ls,
            content_ls=content_json_ls,
            name=name or self.name,
            unique_id=self.id,
            description=description or self.description,
            is_new=False,
        )

        res = await publish_routes.update_publish_job(
            auth=auth, publication_id=self.id, body=body
        )

        return res


class DomoSubscription_NoParentAuth(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            cls_instance=cls_instance,
            entity_id="subscription_id",
            message="must pass parent_auth or parent_auth_retrieval_fn which returns an instance of auth given self",
        )


class DomoSubscription_NoParent(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            cls_instance=cls_instance,
            entity_id="subscription_id",
            message="unable to retrieve parent publication",
        )


@dataclass
class DomoSubscription(dmen.DomoEntity):
    """the subscriber represents a location a publication is sent to"""

    id: str
    publication_id: str
    subscriber_domain: str
    publisher_domain: str
    parent_publication: DomoPublication = field(repr=False, default=None)
    created_dt: Optional[dt.datetime] = None

    @classmethod
    def from_dict(cls, obj, auth: dmda.DomoAuth, parent_publication: Any = None):
        return cls(
            auth=auth,
            id=obj.get("id") or obj.get("subscriptionId"),
            publication_id=obj["publicationId"],
            subscriber_domain=obj.get("domain") or obj.get("subscriberDomain"),
            publisher_domain=obj.get("publisherDomain"),
            created_dt=(
                (dt.datetime.fromtimestamp(obj.get("created") / 1000))
                if obj.get("created")
                else None
            ),
            raw=obj,
            parent_publication=parent_publication,
        )

    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/domo-everywhere/subscriptions"

    @classmethod
    async def get_by_id(
        cls,
        auth: dmda.DomoAuth,
        subscription_id: str,
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        res = await publish_routes.get_subscription_by_id(
            auth=auth,
            subscription_id=subscription_id,
            debug_api=debug_api,
            session=session,
            parent_class=cls.__name__,
        )

        if return_raw:
            return res

        return cls.from_dict(obj=res.response, auth=auth)

    async def get_parent_publication(
        self,
        parent_auth: dmda.DomoAuth = None,
        parent_auth_retrieval_fn: Callable = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        if not parent_auth and parent_auth_retrieval_fn:
            parent_auth = parent_auth_retrieval_fn(self)

        if not parent_auth:
            raise DomoSubscription_NoParentAuth(self)

        self.parent_publication = await DomoPublication.get_by_id(
            publication_id=self.publication_id,
            auth=parent_auth,
            debug_api=debug_api,
            session=session,
        )

        return self.parent_publication

    async def get_content_details(
        self,
        parent_auth: dmda.DomoAuth = None,
        parent_auth_retrieval_fn: Callable = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        if not self.parent_publication:
            await self.get_parent_publication(
                parent_auth=parent_auth,
                parent_auth_retrieval_fn=parent_auth_retrieval_fn,
                debug_api=debug_api,
                session=session,
            )

        if not self.parent_publication:
            raise DomoSubscription_NoParent(self)

        publication_content = self.parent_publication.content

        res = await publish_routes.get_subscriber_content_details(
            auth=self.parent_publication.auth,
            publication_id=self.publication_id,
            subscriber_instance=self.subscriber_domain,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
        )

        for content in publication_content:
            subscriber_obj = next(
                (
                    subscriber_obj
                    for subscriber_obj in res.response
                    if subscriber_obj["publisherObjectId"] == content.entity_id
                    and subscriber_obj["contentType"] == content.entity_type
                ),
                None,
            )
            if subscriber_obj is not None:
                content.subscriber_content_id = subscriber_obj["subscriberObjectId"]
                content.subscriber_insance = subscriber_obj["subscriberDomain"]

        self.content = publication_content

        return self.content


@dataclass
class DomoEverywhere:
    auth: dmda.DomoAuth = field(repr=False)

    publications: List[DomoPublication] = field(default=None)

    subscriptions: List[DomoSubscription] = field(default=None)

    invitations: List[dict] = field(default=None)

    async def get_publications(
        self,
        search_term: str = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        debug_num_stacks_to_drop=2,
    ):
        res = await publish_routes.search_publications(
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            search_term=search_term,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        self.publications = await dmce.gather_with_concurrency(
            n=60,
            *[
                DomoPublication.get_by_id(publication_id=obj.get("id"), auth=self.auth)
                for obj in res.response
            ],
        )
        return self.publications

    async def search_publications(
        self,
        search_term: str = None,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        return_raw: bool = False,
        debug_num_stacks_to_drop=2,
    ):
        res = await self.get_publications(
            search_term=search_term,
            session=session,
            debug_api=debug_api,
            return_raw=return_raw,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        return res

    async def get_subscriptions(
        self,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        debug_api: bool = False,
    ):
        """get instances subscription summaries"""

        self.subscriptions = []

        res = await publish_routes.get_subscription_summaries(
            auth=self.auth, session=session, debug_api=debug_api
        )

        if return_raw:
            return res

        for sub in res.response:
            domo_sub = DomoSubscription.from_dict(sub, auth=self.auth)

            if sub in self.subscriptions:
                continue
            self.subscriptions.append(domo_sub)

        return self.subscriptions

    async def get_subscription_invitations(
        self, debug_api: bool = False, session: httpx.AsyncClient = None
    ):
        res = await publish_routes.get_subscription_invitations(
            auth=auth,
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
        )

        self.invitations = res.response

        return res

    async def accept_invite_by_id(
        self,
        subscription_id: str,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        res = await publish_routes.accept_invite_by_id(
            auth=self.auth,
            subscription_id=subscription_id,
            debug_api=debug_api,
            session=session,
        )

        if res.status == 200:
            return res.response
        else:
            return None
