"""Account module providing Domo account management functionality.

This module contains classes for managing Domo accounts, credentials, configurations,
and OAuth settings.

Classes:
    DomoAccount: Main account class
    DomoAccount_Default: Base account functionality
    DomoAccount_Credential: Account credential management
    DomoAccount_OAuth: OAuth account configurations
    AccountConfig: Account configuration classes
    DomoAccounts: Collection class for managing multiple accounts

Example:
    Basic account usage:

        >>> from domolibrary2.classes.Account import DomoAccount
        >>> account = DomoAccount.from_dict(account_data)

    Working with account collections:

        >>> from domolibrary2.classes.Account import DomoAccounts
        >>> accounts = await DomoAccounts(auth=auth).get()
"""

__all__ = [
    "DomoAccount",
    "DomoAccount_Default",
    "DomoAccount_Credential",
    "DomoAccount_OAuth",
    "AccountConfig",
    "DomoAccount_Config",
    "DomoAccounts",
    "DomoAccounts_NoAccount",
    "UpsertAccount_MatchCriteria",
]

# Import main classes
from .Account import DomoAccount, DomoAccounts, DomoAccounts_NoAccount
from .Account_Default import DomoAccount_Default, UpsertAccount_MatchCriteria
from .Account_Credential import DomoAccount_Credential
from .Account_OAuth import DomoAccount_OAuth
from .Config import AccountConfig, DomoAccount_Config
