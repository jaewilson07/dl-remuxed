"""
DomoInstanceConfig Toggle Management

This module provides a unified interface for managing instance-level feature toggles
in Domo, including social user invites, user invite notifications, weekly digest,
and left navigation settings.
"""

__all__ = ["Toggle_InstantiationError", "DomoToggle"]

from dataclasses import dataclass, field
from typing import Optional

import httpx

from ...client.auth import DomoAuth
from ...client.exceptions import ClassError, RouteError
from ...routes.auth import InvalidAuthTypeError
from ...routes.instance_config import toggle as toggle_routes


class Toggle_InstantiationError(ClassError):  # noqa: N801
    """Exception raised when toggle instantiation fails."""

    def __init__(self, auth: DomoAuth, message: str, cls=None):
        super().__init__(
            domo_instance=auth.domo_instance,
            message=message,
            cls=cls or self.__class__,
        )


@dataclass
class DomoToggle:
    """Manages instance-level feature toggles in Domo.

    This class provides methods to get and toggle various instance settings including:
    - Social user invitation capability
    - User invite email notifications
    - Weekly digest emails
    - Left navigation UI

    Note: Unlike most Domo entities, toggles represent singleton configuration per instance
    and do not have an 'id' field.

    Attributes:
        auth: Authentication object for API requests
        is_invite_social_users_enabled: Whether social users can be invited
        is_user_invite_notifications_enabled: Whether invite notification emails are sent
        is_weekly_digest_enabled: Whether weekly digest emails are sent
        is_left_nav_enabled: Whether left navigation is enabled
        customer_id: Customer ID (cached after first retrieval)
        raw: Raw API response data
    """

    auth: DomoAuth = field(repr=False)
    is_invite_social_users_enabled: Optional[bool] = None
    is_user_invite_notifications_enabled: Optional[bool] = None
    is_weekly_digest_enabled: Optional[bool] = None
    is_left_nav_enabled: Optional[bool] = None
    customer_id: Optional[str] = field(default=None, repr=False)
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def display_url(self) -> str:
        """Return the URL to the instance settings page in Domo."""
        return f"https://{self.auth.domo_instance}.domo.com/admin/company/settings"

    async def _get_customer_id(self) -> str:
        """Retrieve customer ID from bootstrap API.

        Returns:
            Customer ID string

        Raises:
            Toggle_InstantiationError: If FullAuth is required but not provided
        """
        if self.customer_id:
            return self.customer_id

        # Avoid circular import by importing here
        from .bootstrap import DomoBootstrap

        try:
            bs = DomoBootstrap(auth=self.auth)
            self.customer_id = await bs.get_customer_id()
            if self.customer_id:
                return self.customer_id
            else:
                raise Toggle_InstantiationError(
                    auth=self.auth,
                    message="Customer ID not found",
                )

        except InvalidAuthTypeError as e:
            raise Toggle_InstantiationError(
                auth=self.auth,
                message=f"{e.__class__.__name__} -- bootstrap API requires FullAuth to retrieve customer_id",
            ) from e

    # ============================================================================
    # Social User Invites
    # ============================================================================

    async def get_is_invite_social_users_enabled(
        self,
        customer_id: Optional[str] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Check if social user invitations are enabled.

        Args:
            customer_id: Optional customer ID (will be retrieved if not provided)
            debug_api: Enable debug output
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            True if social user invites are enabled, False otherwise

        Raises:
            Toggle_InstantiationError: If customer_id retrieval fails
        """
        if not customer_id:
            customer_id = await self._get_customer_id()

        res = await toggle_routes.get_is_invite_social_users_enabled(
            auth=self.auth,
            customer_id=customer_id,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        self.is_invite_social_users_enabled = res.response["is_enabled"]
        return (
            self.is_invite_social_users_enabled
            if self.is_invite_social_users_enabled
            else False
        )

    async def toggle_is_invite_social_users_enabled(
        self,
        is_enabled: bool,
        customer_id: Optional[str] = None,
        debug_api: bool = False,
        debug_prn: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Enable or disable social user invitation capability.

        Args:
            is_enabled: True to enable, False to disable
            customer_id: Optional customer ID (will be retrieved if not provided)
            debug_api: Enable debug output
            debug_prn: Print debug messages
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            Current state after toggle (True if enabled, False otherwise)

        Raises:
            Toggle_InstantiationError: If customer_id retrieval fails
        """
        if not customer_id:
            customer_id = await self._get_customer_id()

        # Check current state
        current_state = await self.get_is_invite_social_users_enabled(
            customer_id=customer_id,
            session=session,
            debug_api=debug_api,
        )

        if current_state == is_enabled:
            if debug_prn:
                print(
                    f"No action required - social user invites already {'enabled' if is_enabled else 'disabled'}"
                )
            return current_state

        res = await toggle_routes.toggle_is_invite_social_users_enabled(
            auth=self.auth,
            customer_id=customer_id,
            is_enabled=is_enabled,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        # Refresh state
        return await self.get_is_invite_social_users_enabled(
            customer_id=customer_id,
            session=session,
            debug_api=debug_api,
        )

    # ============================================================================
    # User Invite Notifications
    # ============================================================================

    async def get_is_user_invite_notifications_enabled(
        self,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Check if user invite notification emails are enabled.

        Args:
            debug_api: Enable debug output
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            True if invite notifications are enabled, False otherwise
        """
        res = await toggle_routes.get_is_user_invite_notifications_enabled(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        self.is_user_invite_notifications_enabled = res.response["is_enabled"]
        return (
            self.is_user_invite_notifications_enabled
            if self.is_user_invite_notifications_enabled
            else False
        )

    async def toggle_is_user_invite_notifications_enabled(
        self,
        is_enabled: bool,
        debug_api: bool = False,
        debug_prn: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Enable or disable user invite notification emails.

        Args:
            is_enabled: True to enable, False to disable
            debug_api: Enable debug output
            debug_prn: Print debug messages
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            Current state after toggle (True if enabled, False otherwise)
        """
        # Check current state
        current_state = await self.get_is_user_invite_notifications_enabled(
            session=session,
            debug_api=debug_api,
        )

        if current_state == is_enabled:
            if debug_prn:
                print(
                    f"No action required - user invite notifications already {'enabled' if is_enabled else 'disabled'}"
                )
            return current_state

        res = await toggle_routes.toggle_is_user_invite_enabled(
            auth=self.auth,
            is_enabled=is_enabled,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        # Route function refreshes state automatically
        self.is_user_invite_notifications_enabled = res.response["is_enabled"]
        return (
            self.is_user_invite_notifications_enabled
            if self.is_user_invite_notifications_enabled
            else False
        )

    # ============================================================================
    # Weekly Digest
    # ============================================================================

    async def get_is_weekly_digest_enabled(
        self,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Check if weekly digest emails are enabled.

        Args:
            debug_api: Enable debug output
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            True if weekly digest is enabled, False otherwise
        """
        res = await toggle_routes.get_is_weekly_digest_enabled(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        self.is_weekly_digest_enabled = res.response["is_enabled"]
        return self.is_weekly_digest_enabled if self.is_weekly_digest_enabled else False

    async def toggle_is_weekly_digest_enabled(
        self,
        is_enabled: bool,
        debug_api: bool = False,
        debug_prn: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Enable or disable weekly digest emails.

        Args:
            is_enabled: True to enable, False to disable
            debug_api: Enable debug output
            debug_prn: Print debug messages
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            Current state after toggle (True if enabled, False otherwise)
        """
        # Check current state
        current_state = await self.get_is_weekly_digest_enabled(
            session=session,
            debug_api=debug_api,
        )

        if current_state == is_enabled:
            if debug_prn:
                print(
                    f"No action required - weekly digest already {'enabled' if is_enabled else 'disabled'}"
                )
            return current_state

        res = await toggle_routes.toggle_is_weekly_digest_enabled(
            auth=self.auth,
            is_enabled=is_enabled,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        # Route function refreshes state automatically
        self.is_weekly_digest_enabled = res.response["is_enabled"]
        return self.is_weekly_digest_enabled if self.is_weekly_digest_enabled else False

    # ============================================================================
    # Left Navigation
    # ============================================================================

    async def get_is_left_nav_enabled(
        self,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Check if left navigation UI is enabled.

        Args:
            debug_api: Enable debug output
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            True if left navigation is enabled, False otherwise
        """
        res = await toggle_routes.get_is_left_nav_enabled(
            auth=self.auth,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        self.is_left_nav_enabled = res.response["is_enabled"]
        return self.is_left_nav_enabled if self.is_left_nav_enabled else False

    async def toggle_is_left_nav_enabled(
        self,
        is_enabled: bool = True,
        debug_api: bool = False,
        debug_prn: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
    ) -> bool:
        """Enable or disable left navigation UI.

        Args:
            is_enabled: True to enable, False to disable
            debug_api: Enable debug output
            debug_prn: Print debug messages
            session: Optional httpx session
            return_raw: Return raw response without processing

        Returns:
            Current state after toggle (True if enabled, False otherwise)
        """
        # Check current state
        current_state = await self.get_is_left_nav_enabled(
            session=session,
            debug_api=debug_api,
        )

        if current_state == is_enabled:
            if debug_prn:
                print(
                    f"No action required - left navigation already {'enabled' if is_enabled else 'disabled'}"
                )
            return current_state

        res = await toggle_routes.toggle_is_left_nav_enabled(
            auth=self.auth,
            is_use_left_nav=is_enabled,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        # Refresh state
        return await self.get_is_left_nav_enabled(
            session=session,
            debug_api=debug_api,
        )

    # ============================================================================
    # Bulk Operations
    # ============================================================================

    async def get_all(
        self,
        customer_id: Optional[str] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> dict:
        """Retrieve all toggle states.

        Args:
            customer_id: Optional customer ID (required for social user invites)
            debug_api: Enable debug output
            session: Optional httpx session

        Returns:
            Dictionary with all toggle states
        """
        if not customer_id:
            try:
                customer_id = await self._get_customer_id()
            except Toggle_InstantiationError:
                # If customer_id retrieval fails, skip social user invites
                customer_id = None

        results = {}

        # Social user invites (requires customer_id)
        if customer_id:
            try:
                results[
                    "is_invite_social_users_enabled"
                ] = await self.get_is_invite_social_users_enabled(
                    customer_id=customer_id,
                    session=session,
                    debug_api=debug_api,
                )
            except (RouteError, Toggle_InstantiationError) as e:
                results["is_invite_social_users_enabled"] = f"Error: {str(e)}"

        # User invite notifications
        try:
            results[
                "is_user_invite_notifications_enabled"
            ] = await self.get_is_user_invite_notifications_enabled(
                session=session,
                debug_api=debug_api,
            )
        except RouteError as e:
            results["is_user_invite_notifications_enabled"] = f"Error: {str(e)}"

        # Weekly digest
        try:
            results[
                "is_weekly_digest_enabled"
            ] = await self.get_is_weekly_digest_enabled(
                session=session,
                debug_api=debug_api,
            )
        except RouteError as e:
            results["is_weekly_digest_enabled"] = f"Error: {str(e)}"

        # Left navigation
        try:
            results["is_left_nav_enabled"] = await self.get_is_left_nav_enabled(
                session=session,
                debug_api=debug_api,
            )
        except RouteError as e:
            results["is_left_nav_enabled"] = f"Error: {str(e)}"

        return results

    @classmethod
    def from_dict(cls, auth: DomoAuth, obj: dict) -> "DomoToggle":
        """Create a DomoToggle instance from a dictionary representation.

        Args:
            auth: Authentication object for API requests
            obj: Dictionary containing toggle data

        Returns:
            DomoToggle instance
        """
        return cls(
            auth=auth,
            is_invite_social_users_enabled=obj.get("is_invite_social_users_enabled"),
            is_user_invite_notifications_enabled=obj.get(
                "is_user_invite_notifications_enabled"
            ),
            is_weekly_digest_enabled=obj.get("is_weekly_digest_enabled"),
            is_left_nav_enabled=obj.get("is_left_nav_enabled"),
            customer_id=obj.get("customer_id"),
            raw=obj,
        )
