__all__ = [
    "DAC_NoTargetInstance",
    "DAC_NoTargetUser",
    "DAC_NoPassword",
    "DAC_NoUserName",
    "DAC_NoAccessTokenName",
    "DAC_NoAccessToken",
    "DAC_ValidAuth",
    "DomoAccount_Credential",
]


from dataclasses import dataclass, field
from typing import Optional

import httpx

from ...client import auth as dmda, exceptions as dmde
from ...client.auth import DomoAuth
from ...utils import convert as dmcv
from . import Account_Default as dmacb
from ..DomoAccessToken import DomoAccessToken as dmact
from ..DomoUser import DomoUser as dmdu, DomoUsers


class DAC_NoTargetInstance(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            message=f"no target_instance on class - {cls_instance.name}",
            cls_instance=cls_instance,
        )


class DAC_NoTargetUser(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            message=f"no target_user on class - {cls_instance.name}",
            cls_instance=cls_instance,
        )


class DAC_NoPassword(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            message=f"no password stored in account - {cls_instance.name}",
            cls_instance=cls_instance,
        )


class DAC_NoUserName(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            message=f"no username stored in account - {cls_instance.name}",
            cls_instance=cls_instance,
        )


class DAC_NoAccessTokenName(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            message="must pass access token name to retrieve",
            cls_instance=cls_instance,
        )


class DAC_NoAccessToken(dmde.ClassError):
    def __init__(self, cls_instance):
        super().__init__(
            message=f"no access_token stored in account - {cls_instance.name}",
            cls_instance=cls_instance,
        )


class DAC_ValidAuth(dmde.ClassError):
    def __init__(self, cls_instance, message=None):
        super().__init__(
            message=message
            or f"{cls_instance.name} no valid auth retrieved for domo_instance - {cls_instance.target_instance}",
            cls_instance=cls_instance,
        )


@dataclass
class DomoAccount_Credential(dmacb.DomoAccount_Default):
    """Account credential management class for Domo accounts.
    
    This class extends DomoAccount_Default to provide credential management
    capabilities including authentication testing, password management, and
    access token operations.
    
    Attributes:
        target_instance: Target Domo instance for credential operations
        is_valid_full_auth: Whether full authentication is valid
        is_valid_token_auth: Whether token authentication is valid
        target_auth: Active authentication object for target instance
        target_user: DomoUser object for the target user
        target_access_token: Access token for the account
    """
    target_instance: Optional[str] = None

    is_valid_full_auth: Optional[bool] = None
    is_valid_token_auth: Optional[bool] = None

    _token_auth: Optional[DomoAuth] = field(repr=False, default=None)
    _full_auth: Optional[DomoAuth] = field(repr=False, default=None)

    target_auth: Optional[DomoAuth] = field(default=None)
    target_user: Optional[dmdu] = field(default=None)
    target_access_token: Optional[dmact] = field(default=None)

    # Note: __post_init__ is inherited from DomoAccount_Default
    # which initializes the Access subentity

    @classmethod
    def _classfrom_dict(
        cls,
        obj: dict,
        is_admin_summary: bool = True,
        auth: Optional[DomoAuth] = None,
        **kwargs,
    ):
        """Create Account_Credential from dictionary representation.
        
        Args:
            obj: Dictionary containing account data
            is_admin_summary: Whether this is an admin summary view
            auth: Authentication object
            **kwargs: Additional keyword arguments including target_instance
            
        Returns:
            DomoAccount_Credential instance
        """
        return cls._defaultfrom_dict(
            obj=obj,
            is_admin_summary=is_admin_summary,
            auth=auth,
            target_instance=kwargs.get("target_instance"),
        )

    def set_password(self, password: str) -> bool:
        """Set the password in the account configuration.
        
        Args:
            password: New password to set
            
        Returns:
            True if successful
        """
        self.Config.password = password
        return True

    def set_username(self, username: str) -> bool:
        """Set the username in the account configuration.
        
        Args:
            username: New username to set
            
        Returns:
            True if successful
        """
        self.Config.username = username
        return True

    def set_access_token(self, access_token: str) -> bool:
        """Set the access token in the account configuration.
        
        Args:
            access_token: New access token to set
            
        Returns:
            True if successful
        """
        self.Config.domo_access_token = access_token
        return True

    async def test_full_auth(
        self, 
        debug_api: bool = False, 
        session: Optional[httpx.AsyncClient] = None
    ) -> bool:
        """Test full authentication (username/password) for the account.
        
        Generates a DomoFullAuth object and validates it against the target instance.
        
        Args:
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            
        Returns:
            True if authentication is valid, False otherwise
            
        Raises:
            DAC_NoUserName: If username is not configured
            DAC_NoPassword: If password is not configured
            DAC_NoTargetInstance: If target instance is not set
        """
        self.is_valid_full_auth = False

        if not self.Config.username:
            raise DAC_NoUserName(self)

        if not self.Config.password:
            raise DAC_NoPassword(self)

        if not self.target_instance:
            raise DAC_NoTargetInstance(self)

        self._full_auth = dmda.DomoFullAuth(
            domo_instance=self.target_instance,
            domo_username=self.Config.username,
            domo_password=self.Config.password,
        )

        try:
            await self._full_auth.print_is_token(debug_api=debug_api, session=session)
            self.is_valid_full_auth = True

        except dmda.AuthError as e:
            dmcv.print_md(f"🤯 test_full_auth for: ***{self.name}*** returned {e}")

            self.is_valid_full_auth = False

        return self.is_valid_full_auth

    async def test_token_auth(
        self, 
        debug_api: bool = False, 
        session: Optional[httpx.AsyncClient] = None
    ) -> bool:
        """Test token authentication for the account.
        
        Generates a DomoTokenAuth object and validates it against the target instance.
        
        Args:
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            
        Returns:
            True if authentication is valid, False otherwise
            
        Raises:
            DAC_NoAccessToken: If access token is not configured
            DAC_NoTargetInstance: If target instance is not set
        """

        self.is_valid_token_auth = False

        if not self.Config.domo_access_token:
            raise DAC_NoAccessToken(self)

        if not self.target_instance:
            raise DAC_NoTargetInstance(self)

        self._token_auth = dmda.DomoTokenAuth(
            domo_instance=self.target_instance,
            domo_access_token=self.Config.domo_access_token,
        )

        try:
            await self._token_auth.print_is_token(debug_api=debug_api, session=session)
            self.is_valid_token_auth = True
            self.target_auth = self._token_auth

        except dmda.AuthError as e:
            dmcv.print_md(f"🤯 test_token_auth for: ***{self.name}*** returned {e}")
            self.is_valid_token_auth = False

        return self.is_valid_token_auth

    def _set_target_auth(
        self,
        valid_backup_auth: Optional[DomoAuth] = None,
    ) -> DomoAuth:
        """Set target authentication using best available method.
        
        Prioritizes authentication methods in order: Token Auth > Full Auth > Backup Auth
        
        Args:
            valid_backup_auth: Validated backup authentication object to use as fallback
            
        Returns:
            The selected authentication object
            
        Raises:
            DAC_ValidAuth: If no valid authentication method is available
        """

        target_auth = None

        if self.is_valid_token_auth:
            target_auth = self._token_auth

        if self.is_valid_full_auth:
            target_auth = self._full_auth

        if not target_auth and (valid_backup_auth and valid_backup_auth.is_valid_token):
            target_auth = valid_backup_auth

        if not target_auth:
            raise DAC_ValidAuth(self)

        self.target_auth = target_auth

        return self.target_auth

    async def test_auths(
        self,
        backup_auth: Optional[DomoAuth] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> dict:
        """Test both token and full authentication methods.
        
        Attempts to validate both authentication methods and sets the best available
        as the target authentication.
        
        Args:
            backup_auth: Backup authentication to use if configured auths fail
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            
        Returns:
            Dictionary with authentication test results
        """
        ## test token auth
        try:
            await self.test_token_auth(debug_api=debug_api, session=session)

        except DomoError as e:
            print(f"testing token: {self.name}: {e}")

        ## test full auth
        try:
            await self.test_full_auth(debug_api=debug_api, session=session)

        except DomoError as e:
            print(f"testing full auth: {self.name}: {e}")

        ## generate target_auth
        try:
            self._set_target_auth(valid_backup_auth=backup_auth)

        except DAC_ValidAuth as e:
            print(f"{self.name}: unable to generate valid target_auth: {e}")

        return self.to_dict()

    def to_dict(self) -> dict:
        """Convert credential information to dictionary.
        
        Returns:
            Dictionary containing account ID, alias, instance, and auth validity status
        """
        return {
            "account_id": self.id,
            "alias": self.name,
            "target_instance": self.target_instance,
            "is_valid_full_auth": self.is_valid_full_auth,
            "is_valid_token_auth": self.is_valid_token_auth,
        }

    async def get_target_user(
        self,
        user_email: Optional[str] = None,
        target_auth: Optional[DomoAuth] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> dmdu:
        """Retrieve the target user for this account.
        
        Args:
            user_email: Email address of user (defaults to configured username)
            target_auth: Authentication object (defaults to self.target_auth)
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            
        Returns:
            DomoUser object for the target user
            
        Raises:
            DAC_NoUserName: If user email is not provided or configured
            DAC_ValidAuth: If target authentication is not available
            DAC_NoTargetUser: If user cannot be found
        """
        user_email = user_email or self.Config.username

        if not user_email:
            raise DAC_NoUserName(self)

        target_auth = target_auth or self.target_auth

        if not target_auth:
            raise DAC_ValidAuth(
                self,
                message="no target_auth, pass a valid backup_auth",
            )

        self.target_user = await DomoUsers.by_email(
            email_ls=[user_email],
            auth=target_auth,
            debug_api=debug_api,
            session=session,
        )

        if not self.target_user:
            raise DAC_NoTargetUser(self)

        return self.target_user

    async def update_target_user_password(
        self,
        new_password: str,
        user_email: Optional[str] = None,
        is_update_account: bool = True,
        target_auth: Optional[DomoAuth] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> "DomoAccount_Credential":
        """Update the password for the target user.
        
        Args:
            new_password: New password to set for the user
            user_email: Email address of user (defaults to configured username)
            is_update_account: Whether to update the account config with new password
            target_auth: Authentication object (defaults to self.target_auth)
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            
        Returns:
            Self for method chaining
            
        Raises:
            DAC_ValidAuth: If target authentication is not available
        """
        target_auth = target_auth or self.target_auth

        if not target_auth:
            raise DAC_ValidAuth(
                self,
                message="no target_auth, pass a valid backup_auth",
            )

        if not self.target_user:
            await self.get_target_user(
                debug_api=debug_api,
                session=session,
                user_email=user_email,
                target_auth=target_auth,
            )

        await self.target_user.reset_password(
            new_password=new_password,
            debug_api=debug_api,
            session=session,
        )

        self.set_password(new_password)

        if is_update_account:
            await self.update_config(debug_api=debug_api, session=session)

        return self

    async def get_target_access_token(
        self,
        token_name: Optional[str] = None,
        user_email: Optional[str] = None,
        target_auth: Optional[DomoAuth] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> Optional[dmact]:
        """Retrieve an access token for the target user.
        
        Args:
            token_name: Name of the access token (defaults to account name)
            user_email: Email address of user (defaults to configured username)
            target_auth: Authentication object (defaults to self.target_auth)
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            
        Returns:
            DomoAccessToken object if found, None otherwise
            
        Raises:
            DAC_ValidAuth: If target authentication is not available
            DAC_NoAccessTokenName: If token name is not provided or available
        """
        target_auth = target_auth or self.target_auth

        if not target_auth:
            raise DAC_ValidAuth(
                self,
                message="no target_auth, pass a valid backup_auth",
            )

        if not self.target_user:
            await self.get_target_user(
                debug_api=debug_api,
                session=session,
                user_email=user_email,
                target_auth=target_auth,
            )

        token_name = token_name or self.name

        if not token_name:
            raise DAC_NoAccessTokenName(self)

        domo_access_tokens = await self.target_user.get_access_tokens(
            session=session,
            debug_api=debug_api,
        )

        self.target_access_token = next(
            (
                dat
                for dat in domo_access_tokens
                if dat and (dat.name and dat.name.lower() == token_name.lower())
            ),
            None,
        )

        return self.target_access_token

    async def regenerate_target_access_token(
        self,
        token_name: Optional[str] = None,
        duration_in_days: int = 90,
        user_email: Optional[str] = None,
        is_update_account: bool = True,
        target_auth: Optional[DomoAuth] = None,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> "DomoAccount_Credential":
        """Regenerate or create an access token for the target user.
        
        If a token with the given name exists, it will be regenerated. Otherwise,
        a new token will be created.
        
        Args:
            token_name: Name of the access token (defaults to account name)
            duration_in_days: Token validity duration in days (default: 90)
            user_email: Email address of user (defaults to configured username)
            is_update_account: Whether to update the account config with new token
            target_auth: Authentication object (defaults to self.target_auth)
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            
        Returns:
            Self for method chaining
            
        Raises:
            DAC_ValidAuth: If target authentication is not available
            DAC_NoTargetUser: If target user cannot be retrieved
        """
        target_auth = target_auth or self.target_auth

        if not target_auth:
            raise DAC_ValidAuth(
                self,
                message="no target_auth, pass a valid backup_auth",
            )

        domo_access_token = await self.get_target_access_token(
            token_name=token_name,
            user_email=user_email,
            target_auth=target_auth,
            debug_api=debug_api,
            session=session,
        )  # handles retrieving target user

        if not self.target_user:
            raise DAC_NoTargetUser(self)

        if domo_access_token:
            await domo_access_token.regenerate(
                duration_in_days=duration_in_days, session=session, debug_api=debug_api
            )

        else:
            domo_access_token = await dmact.DomoAccessToken.generate(
                duration_in_days=duration_in_days,
                token_name=token_name,
                auth=target_auth,
                owner=self.target_user,
                debug_api=debug_api,
                session=session,
            )

            self.target_access_token = domo_access_token

        self.set_access_token(domo_access_token.token)

        if is_update_account:
            await self.update_config(debug_api=debug_api, session=session)

        return self
