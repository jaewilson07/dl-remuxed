"""a class based approach for interacting with Domo Datasets"""

__all__ = [
    "DomoDataset_Default",
    "FederatedDomoDataset",
    "DomoPublishDataset",
    "DomoDataset",
]


from dataclasses import dataclass
from typing import Callable, Optional

import httpx

from ...client.auth import DomoAuth
from ...entities.entities_federated import DomoFederatedEntity, DomoPublishedEntity
from .dataset_default import DomoDataset_Default
from ...utils import chunk_execution as dmce


@dataclass
class FederatedDomoDataset(DomoDataset_Default, DomoFederatedEntity):
    """Federated dataset seen in a parent instance; points to a child instance's native dataset."""

    async def get_federated_parent(
        self,
        parent_auth:  None,
        parent_auth_retrieval_fn: Optional[Callable] = None,
    ):
        from ...classes.publish import DomoEverywhere 
        domo_everywhere = DomoEverywhere(
            auth=self.auth,
        )

        await domo_everywhere.get_subscriptions()

        await dmce.gather_with_concurrency(*[sub.get_parent_publication(parent_auth_retrieval_fn=parent_auth_retrieval_fn) for sub in domo_everywhere.subscriptions], n= 20)


        all = await dmce.gather_with_concurrency(*[
            sub.parent_publication.get_publication_entity_by_subscriber_entity(
                subscriber_domain=sub.subscriber_domain,
                subscriber=self,
            )
            for sub in domo_everywhere.subscriptions
        ], n=20)
        
        self.parent_entity = next((entity for entity in all if entity is not None), None)
        if not self.parent_entity:
            # raise KeyError(
            #         cls_instance=self,
            #         message=f"get_federated_parent: No matching parent entity found for subscriber id {self.id}",
            #     )
            raise NotImplementedError("To Do")
        
        
        return self.parent_entity
    

    @classmethod
    async def get_by_id(
        cls,
        dataset_id: str,
        auth: DomoAuth,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
        is_use_default_dataset_class: bool = False,
        parent_class: str = None,
    ):
        """retrieves federated dataset metadata"""
        # Use parent implementation to avoid code duplication
        return await super().get_by_id(
            dataset_id=dataset_id,
            auth=auth,
            debug_api=debug_api,
            return_raw=return_raw,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            is_use_default_dataset_class=is_use_default_dataset_class,
            parent_class=parent_class or cls.__name__,
        )


@dataclass
class DomoPublishDataset(FederatedDomoDataset, DomoPublishedEntity):
    async def get_subscription(self):
        return await super().get_subscription()

    async def get_parent_publication(self):
        return await super().get_parent_publication()


@dataclass
class DomoDataset(DomoDataset_Default):
    @classmethod
    def from_dict(
        cls,
        obj: dict,
        # is_admin_summary: bool = True,
        auth: DomoAuth = None,
        is_use_default_dataset_class: bool = False,
        new_cls=None,
        **kwargs,
    ) -> "DomoDataset":
        """converts dataset API response into a dataset class object"""

        is_federated = cls._is_federated_dataset_obj(obj)

        new_cls = DomoDataset

        if is_federated and not is_use_default_dataset_class:
            new_cls = FederatedDomoDataset

        # TO DO -- how do we know if it's published?

        return super().from_dict(
            auth=auth,
            obj=obj,
            is_use_default_dataset_class=is_use_default_dataset_class,
            new_cls=new_cls,
            **kwargs,
        )
