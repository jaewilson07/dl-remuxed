__all__ = [
    "InstanceSwitcher_Mapping",
    "InstanceSwitcher",
    "InstanceSwitcher_GET_Error",
    "InstanceSwitcher_CRUD_Error",
]


import asyncio
from dataclasses import dataclass, field
from typing import List, Optional

import httpx

from ...client.auth import DomoAuth
from ...routes.instance_config import instance_switcher as instance_switcher_routes
from ...routes.instance_config.instance_switcher import (
    InstanceSwitcher_CRUD_Error,
    InstanceSwitcher_GET_Error,
)


@dataclass
class InstanceSwitcher_Mapping:
    """Represents a single instance switcher mapping configuration.

    Maps a user attribute to a target Domo instance that users can switch to.

    Attributes:
        user_attribute: The user attribute key used for mapping
        target_instance: The Domo instance domain (without .domo.com)
    """

    user_attribute: str
    target_instance: str  # instance user is granted access to / can switch to

    def __post_init__(self):
        """Remove .domo.com suffix from target_instance if present."""
        self.target_instance = self.target_instance.replace(".domo.com", "")

    def __eq__(self, other) -> bool:
        """Check equality based on user_attribute and target_instance.

        Args:
            other: Object to compare with

        Returns:
            bool: True if both have the same user_attribute and target_instance
        """
        if type(self) != type(other):
            return False
        else:
            return (
                self.target_instance == other.target_instance
                and self.user_attribute == other.user_attribute
            )

    def __lt__(self, other) -> bool:
        """Compare mappings for sorting.

        Args:
            other: Mapping to compare with

        Returns:
            bool: True if this mapping is less than other
        """
        return (
            self.target_instance < other.target_instance
            and self.user_attribute < other.user_attribute
        )

    @classmethod
    def from_dict(cls, obj: dict) -> "InstanceSwitcher_Mapping":
        """Create a mapping from API response dictionary.

        Args:
            obj: Dictionary with userAttribute and instance keys

        Returns:
            DomoInstanceConfig_InstanceSwitcher_Mapping: New mapping instance
        """
        return cls(
            user_attribute=obj["userAttribute"],
            target_instance=obj["instance"],
        )

    @classmethod
    def from_obj(cls, obj: dict) -> "InstanceSwitcher_Mapping":
        """Legacy method - calls from_dict for compatibility.

        Args:
            obj: Dictionary with userAttribute and instance keys

        Returns:
            DomoInstanceConfig_InstanceSwitcher_Mapping: New mapping instance
        """
        return cls.from_dict(obj)

    def to_dict(self) -> dict:
        """Convert mapping to API request format.

        Returns:
            dict: Dictionary with userAttribute and instance (including .domo.com)
        """
        return {
            "userAttribute": self.user_attribute,
            "instance": self.target_instance + ".domo.com",
        }


@dataclass
class InstanceSwitcher:
    """Manages instance switcher configuration for a Domo instance.

    This class handles the configuration of instance switching mappings, which allow
    users with specific attributes to switch between different Domo instances.

    Attributes:
        auth: Authentication object for API requests
        domo_instance_switcher_mapping: List of instance switcher mappings
    """

    auth: DomoAuth = field(repr=False)
    domo_instance_switcher_mapping: List[InstanceSwitcher_Mapping] = field(
        default_factory=list
    )

    def _add_mapping_to_ls(
        self,
        domo_instance_switcher_mapping: InstanceSwitcher_Mapping,
    ) -> List[InstanceSwitcher_Mapping]:
        """Add a mapping to the list with deduplication.

        Args:
            domo_instance_switcher_mapping: Mapping to add

        Returns:
            List[DomoInstanceConfig_InstanceSwitcher_Mapping]: Updated mapping list
        """

        if domo_instance_switcher_mapping not in self.domo_instance_switcher_mapping:
            self.domo_instance_switcher_mapping.append(domo_instance_switcher_mapping)
        return self.domo_instance_switcher_mapping

    async def get_mapping(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        debug_num_stacks_to_drop: int = 2,
        timeout: int = 20,
    ) -> List[InstanceSwitcher_Mapping]:
        """Retrieve current instance switcher mappings.

        Args:
            debug_api: Enable API debugging
            return_raw: Return raw response without processing
            session: HTTP client session
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            timeout: Request timeout in seconds

        Returns:
            List of instance switcher mappings or raw response if return_raw=True
        """
        res = await instance_switcher_routes.get_instance_switcher_mapping(
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            timeout=timeout,
        )

        if return_raw:
            return res

        for obj in res.response:
            self._add_mapping_to_ls(InstanceSwitcher_Mapping.from_obj(obj=obj))

        return self.domo_instance_switcher_mapping

    async def set_mapping(
        self,
        mapping_ls: Optional[
            List[InstanceSwitcher_Mapping]
        ] = None,  # will default to self.domo_instance_switcher_mapping
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        return_raw: bool = False,
        debug_num_stacks_to_drop: int = 2,
        timeout: int = 60,
        wait: int = 5,
    ) -> List[InstanceSwitcher_Mapping]:
        """Overwrite existing mappings with new mapping list.

        Args:
            mapping_ls: List of mappings to set (defaults to self.domo_instance_switcher_mapping)
            session: HTTP client session
            debug_api: Enable API debugging
            return_raw: Return raw response without processing
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            timeout: Request timeout in seconds
            wait: Seconds to wait before retrieving updated mappings

        Returns:
            Updated list of instance switcher mappings or raw response if return_raw=True
        """

        # structure payload appropriately
        mapping_ls = mapping_ls or self.domo_instance_switcher_mapping

        mapping_payloads = [domo_mapping.to_dict() for domo_mapping in mapping_ls]

        # update routing mappings
        res = await instance_switcher_routes.set_instance_switcher_mapping(
            auth=self.auth,
            mapping_payloads=mapping_payloads,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            timeout=timeout,
        )

        if return_raw:  # returns api response
            return res

        await asyncio.sleep(wait)

        return await self.get_mapping(
            session=session, debug_api=debug_api
        )  # returns updated list of classes

    async def add_mapping(
        self,
        mapping_to_add_ls: List[InstanceSwitcher_Mapping],
        session: Optional[httpx.AsyncClient] = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        timeout: int = 20,
        wait: int = 5,
    ) -> List[InstanceSwitcher_Mapping]:
        """Add new mappings to existing configuration.

        Args:
            mapping_to_add_ls: List of mappings to add
            session: HTTP client session
            debug_api: Enable API debugging
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            timeout: Request timeout in seconds
            wait: Seconds to wait before retrieving updated mappings

        Returns:
            Updated list of instance switcher mappings
        """

        # get existing mapping
        await self.get_mapping(
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            timeout=timeout,
        )

        for domo_mapping in mapping_to_add_ls:
            self._add_mapping_to_ls(domo_mapping)

        # update routing mappings
        return await self.set_mapping(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            timeout=timeout,
            wait=wait,
        )
