from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, List

import httpx

from ...client import exceptions as dmde
from ...entities.entities import DomoSubEntity
from ...entities.relationships import (
    DomoRelationship,
    DomoRelationshipController,
    RelationshipType,
)
from ...routes import group as group_routes
from ...utils import chunk_execution as dmce

__all__ = [
    "UpdateMembership",
    "Membership_Entity",
    "DomoMembership",
    "DomoMembership_Group",
]


class UpdateMembership(dmde.ClassError):
    def __init__(self, cls_instance, member_name=None, entity_id=None):
        super().__init__(
            entity_id=entity_id,
            cls_instance=cls_instance,
            message=f"unable to alter membership {member_name if member_name else ''}",
        )


@dataclass
class Membership_Entity(DomoRelationship):
    """Represents a membership relationship between entities."""

    @property
    def relation_type(self) -> RelationshipType:
        """Backward compatibility property."""
        return self.relationship_type

    def to_dict(self):
        from .. import (
            DomoGroup as dmdg,
            DomoUser as dmdu,
        )

        if isinstance(self.entity, dmdu.DomoUser):
            return {"type": "USER", "id": str(self.entity.id)}

        if isinstance(self.entity, dmdg.DomoGroup):
            return {"type": "GROUP", "id": int(self.entity.id)}

        raise UpdateMembership(cls_instance=self, entity_id=self.entity.id)

    def update(self):
        """Update membership metadata or properties."""
        # Implementation for updating membership properties
        pass


@dataclass
class DomoMembership(DomoRelationshipController, DomoSubEntity):
    """
    Unified membership management using the relationship system.

    This class provides a consistent interface for managing membership relationships
    across all Domo objects including groups, roles, and organizations.
    """

    # Legacy compatibility
    owners: List[str] = field(default_factory=lambda: [])
    members: List[str] = field(default_factory=lambda: [])

    # Relationship management
    _add_member_ls: List[Membership_Entity] = field(default_factory=lambda: [])
    _remove_member_ls: List[Membership_Entity] = field(default_factory=lambda: [])
    _add_owner_ls: List[Membership_Entity] = field(default_factory=lambda: [])
    _remove_owner_ls: List[Membership_Entity] = field(default_factory=lambda: [])

    async def get(self) -> List[Membership_Entity]:
        """Get all membership relationships for this object."""
        raise NotImplementedError("DomoMembership.get not implemented")

    async def add_relationship(
        self,
        relative_id: str,
        relationship_type: RelationshipType,
    ) -> Membership_Entity:
        """Create a new membership relationship."""
        raise NotImplementedError("DomoMembership.add_relationship not implemented")

    @abstractmethod
    async def get_owners(self) -> List[Membership_Entity]:
        """Get all owner relationships."""
        pass

    @abstractmethod
    async def get_members(self) -> List[Membership_Entity]:
        """Get all member relationships."""
        pass

    @abstractmethod
    async def update(self):
        """Update membership relationships."""
        pass

    def _add_to_list(self, member, list_to_update, relation_type):
        if not isinstance(member, Membership_Entity):
            # Convert entity to Membership_Entity with new structure
            member_entity = Membership_Entity(
                entity=member, relationship_type=RelationshipType(relation_type)
            )
        else:
            member_entity = member

        if member_entity not in list_to_update:
            list_to_update.append(member_entity)

    def _add_member(self, member):
        return self._add_to_list(member, self._add_member_ls, relation_type="MEMBER")

    def _remove_member(self, member, is_keep_system_group=True):
        """Remove member - does not remove system groups"""
        from .. import DomoGroup as dmg

        # Check if we should keep system groups
        if (
            is_keep_system_group
            and isinstance(member, dmg.DomoGroup)
            and member.type == "system"
        ):
            return

        return self._add_to_list(member, self._remove_member_ls, relation_type="MEMBER")

    def _add_owner(self, member):
        return self._add_to_list(member, self._add_owner_ls, relation_type="OWNER")

    def _remove_owner(self, member, is_keep_system_group=True):
        """Remove owner - does not remove system groups"""
        from .. import DomoGroup as dmg

        # Check if we should keep system groups
        if (
            is_keep_system_group
            and isinstance(member, dmg.DomoGroup)
            and member.type == "system"
        ):
            return

        return self._add_to_list(member, self._remove_owner_ls, relation_type="OWNER")

    def _reset_obj(self):
        self._add_member_ls = []
        self._remove_member_ls = []

        self._add_owner_ls = []
        self._remove_owner_ls = []

    async def _extract_domo_groups_from_list(
        self, entity_ls, session: httpx.AsyncClient
    ):
        from .. import DomoGroup as dmg

        return await dmce.gather_with_concurrency(
            *[
                dmg.DomoGroup.get_by_id(
                    group_id=obj.get("groupId") or obj.get("id"),
                    auth=self.auth,
                    session=session,
                )
                for obj in entity_ls
                if obj.get("type") == "GROUP" or obj.get("groupId")
            ],
            n=60,
        )

    async def _extract_domo_users_from_list(
        self, entity_ls, session: httpx.AsyncClient = None
    ):
        from .. import DomoUser as dmu

        return await dmce.gather_with_concurrency(
            *[
                dmu.DomoUser.get_by_id(
                    user_id=obj.get("userId") or obj.get("id"),
                    session=session,
                    auth=self.auth,
                )
                for obj in entity_ls
                if obj.get("type") == "USER" or obj.get("userId")
            ],
            n=10,
        )

    async def _extract_domo_entities_from_list(
        self, entity_ls, relation_type, session: httpx.AsyncClient = None
    ):
        session = session or httpx.AsyncClient()

        domo_groups = await self._extract_domo_groups_from_list(
            entity_ls, session=session
        )
        domo_users = await self._extract_domo_users_from_list(
            entity_ls, session=session
        )

        # Create Membership_Entity instances using the new structure
        membership_entities = []
        for entity in domo_groups + domo_users:
            membership_entity = Membership_Entity(
                entity=entity, relationship_type=RelationshipType(relation_type)
            )
            membership_entities.append(membership_entity)

        return membership_entities

    @staticmethod
    def _list_to_dict(entity_ls):
        return [parent.to_dict() for parent in entity_ls]


@dataclass
class DomoMembership_Group(DomoMembership):
    """
    Group membership management using unified relationship system.

    This class provides backward compatibility while using the new
    unified relationship framework internally.
    """

    async def get(self) -> List[Membership_Entity]:
        """Get all membership relationships for this group."""
        owners = await self.get_owners()
        members = await self.get_members()
        return owners + members

    async def add_relationship(
        self,
        relative_id: str,
        relationship_type: RelationshipType,
    ) -> Membership_Entity:
        """Create a new membership relationship for this group."""
        # Implementation would create the relationship and add to appropriate list
        raise NotImplementedError(
            "DomoMembership_Group.add_relationship not implemented"
        )

    async def get_owners(
        self,
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        res = await group_routes.get_group_owners(
            group_id=self.parent_id,
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )
        if return_raw:
            return res

        owners = await self._extract_domo_entities_from_list(
            res.response, relation_type="OWNER", session=session
        )
        self.owners = owners

        if self.parent:
            self.parent.owner_id_ls = [owner.entity.id for owner in self.owners]
            self.parent.owner_ls = [owner.entity for owner in self.owners]

        return self.owners

    async def update(
        self,
        update_payload: dict = None,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        res = await group_routes.update_group_membership(
            auth=self.auth,
            update_payload=update_payload,
            group_id=self.parent_id,
            add_member_arr=self._list_to_dict(self._add_member_ls),
            remove_member_arr=self._list_to_dict(self._remove_member_ls),
            add_owner_arr=self._list_to_dict(self._add_owner_ls),
            remove_owner_arr=self._list_to_dict(self._remove_owner_ls),
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        self._reset_obj()

        return res

    async def get_members(
        self,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ):
        res = await group_routes.get_group_membership(
            group_id=self.parent_id,
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        members = await self._extract_domo_entities_from_list(
            res.response, relation_type="MEMBER", session=session
        )
        self.members = members

        if self.parent:
            self.parent.members_id_ls = [member.entity.id for member in self.members]
            self.parent.members_ls = [member.entity for member in self.members]

        return self.members

    async def add_members(
        self: DomoMembership_Group,
        add_user_ls: List[Any],
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        self._reset_obj()

        for domo_user in add_user_ls:
            self._add_member(domo_user)

        res = await self.update(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        if return_raw:
            return res

        return await self.get_members(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

    async def remove_members(
        self: DomoMembership_Group,
        remove_user_ls: List[Any],
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        self._reset_obj()

        for domo_user in remove_user_ls:
            self._remove_member(domo_user)

        res = await self.update(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        if return_raw:
            return res

        return await self.get_members(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

    async def set_members(
        self: DomoMembership_Group,
        user_ls: List[Any],
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        self._reset_obj()

        # Convert users to Membership_Entity instances
        user_entities = []
        for user in user_ls:
            member_entity = Membership_Entity(
                relative_id=str(user.id),
                relative_class=type(user),
                relationship_type=RelationshipType("MEMBER"),
                parent_entity=self.parent,
                entity=user,
            )
            user_entities.append(member_entity)

        user_ls = user_entities

        memberships = await self.get_members(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        for domo_user in user_ls:
            self._add_member(domo_user)

        for me in memberships:
            if me not in user_ls:
                self._remove_member(me)

        res = await self.update(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )
        if return_raw:
            return res

        return await self.get_members(
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            session=session,
        )

    async def add_owners(
        self: DomoMembership_Group,
        add_owner_ls: List[Any],
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        self._reset_obj()

        for domo_user in add_owner_ls:
            self._add_owner(domo_user)

        res = await self.update(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return await self.get_owners(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

    async def remove_owners(
        self: DomoMembership_Group,
        remove_owner_ls: List[Any],
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop: int = 2,
    ):
        self._reset_obj()

        for domo_user in remove_owner_ls:
            self._remove_owner(domo_user)

        res = await self.update(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        if return_raw:
            return res

        return await self.get_owners(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

    async def set_owners(
        self: DomoMembership_Group,
        owner_ls: List[Any],
        return_raw: bool = False,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        session: httpx.AsyncClient = None,
    ):
        from .. import DomoGroup as dmdg

        self._reset_obj()

        # Convert owners to Membership_Entity instances
        owner_entities = []
        for owner in owner_ls:
            owner_entity = Membership_Entity(
                relative_id=str(owner.id),
                relative_class=type(owner),
                relationship_type=RelationshipType("OWNER"),
                parent_entity=self.parent,
                entity=owner,
            )
            owner_entities.append(owner_entity)

        owner_ls = owner_entities

        membership = await self.get_owners()

        for domo_entity in owner_ls:
            self._add_owner(domo_entity)

        for oe in membership:
            # open accounts must have themselves as an owner
            if (
                self.parent
                and self.parent.type == "open"
                and self.parent.id == oe.entity.id
                and isinstance(oe.entity, dmdg.DomoGroup)
            ):
                self._add_owner(oe)
                continue

            if isinstance(oe.entity, dmdg.DomoGroup) and oe.entity.is_system:
                self._add_owner(oe)
                continue

            if oe.entity not in owner_ls:
                self._remove_owner(oe)

        res = await self.update(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

        if return_raw:
            return res

        return await self.get_owners(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

    async def add_owner_manage_all_groups_role(
        self: DomoMembership_Group,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        from .. import DomoGroup as dmg

        domo_groups = dmg.DomoGroups(auth=self.auth)

        grant_group = await domo_groups.search_by_name(
            group_name="Grant: Manage all groups",
            is_hide_system_groups=False,
            session=session,
            debug_api=debug_api,
        )

        await self.add_owners(
            add_owner_ls=[grant_group], session=session, debug_api=debug_api
        )

        return await self.get_owners(session=session)
