"""Snowflake-specific account configurations."""

from dataclasses import dataclass, field
from typing import Any

from ._base import DomoAccount_Config
from ..config import register_account_config

__all__ = [
    "DomoAccount_Config_Snowflake",
    "DomoAccount_Config_SnowflakeUnload_V2",
    "DomoAccount_Config_SnowflakeUnloadAdvancedPartition",
    "DomoAccount_Config_SnowflakeWriteback",
    "DomoAccount_Config_SnowflakeUnload",
    "DomoAccount_Config_SnowflakeFederated",
    "DomoAccount_Config_SnowflakeInternalUnload",
    "DomoAccount_Config_SnowflakeKeyPairAuthentication",
    "DomoAccount_Config_SnowflakeKeyPairWriteback",
    "DomoAccount_Config_SnowflakeKeyPairUnload_V2",
    "DomoAccount_Config_SnowflakeKeyPairInternalManagedUnload",
]


@register_account_config("snowflake")
@dataclass
class DomoAccount_Config_Snowflake(DomoAccount_Config):
    """this connector is not enabled by default contact your CSM / AE"""

    data_provider_type: str = "snowflake"
    is_oauth: bool = False

    account: str = None
    username: str = None
    password: str = field(repr=False, default=None)
    role: str = None

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "account",
            "username",
            "password",
            "role",
        ]
    )


@register_account_config("snowflake-unload-v2")
@dataclass
class DomoAccount_Config_SnowflakeUnload_V2(DomoAccount_Config):
    """this connector is not enabled by default contact your CSM / AE"""

    data_provider_type: str = "snowflake-unload-v2"
    is_oauth: bool = False

    account: str = None
    username: str = None
    password: str = field(repr=False, default=None)

    access_key: str = None
    secret_key: str = field(repr=False, default=None)
    region: str = None
    bucket: str = None

    role: str = None

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "account",
            "username",
            "password",
            "access_key",
            "secret_key",
            "bucket",
            "region",
            "role",
        ]
    )


@register_account_config("snowflake-internal-unload-advanced-partition")
@dataclass
class DomoAccount_Config_SnowflakeUnloadAdvancedPartition(DomoAccount_Config):
    data_provider_type: str = "snowflake-internal-unload-advanced-partition"
    is_oauth: bool = False

    password: str = field(repr=False, default=None)
    account: str = None
    username: str = None
    role: str = None

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "password",
            "role",
            "account",
            "username",
        ]
    )


@register_account_config("snowflake-writeback")
@dataclass
class DomoAccount_Config_SnowflakeWriteback(DomoAccount_Config):
    data_provider_type: str = "snowflake-writeback"
    is_oauth: bool = False

    domo_client_secret: str = field(repr=False, default=None)
    domo_client_id: str = None
    account: str = None
    password: str = field(repr=False, default=None)
    username: str = None
    role: str = None

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "domo_client_secret",
            "password",
            "domo_client_id",
            "account",
            "username",
            "role",
        ]
    )

    # @classmethod
    # def from_dict(cls, obj: dict, parent: Any = None, **kwargs):
    #     return cls(
    #         domo_client_secret=obj["domoClientSecret"],
    #         domo_client_id=obj["domoClientId"],
    #         account=obj["account"],
    #         username=obj["username"],
    #         password=obj["password"],
    #         raw=obj,
    #         parent=parent,
    #     )


@register_account_config("snowflake-unload")
@dataclass
class DomoAccount_Config_SnowflakeUnload(DomoAccount_Config):
    data_provider_type: str = "snowflake-unload"
    is_oauth: bool = False

    secret_key: str = field(repr=False, default=None)
    access_key: str = None
    account: str = None
    password: str = field(repr=False, default=None)
    username: str = None
    bucket: str = None

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "bucket",
            "password",
            "secret_key",
            "access_key",
            "account",
            "username",
        ]
    )


@register_account_config("snowflake-federated")
@dataclass
class DomoAccount_Config_SnowflakeFederated(DomoAccount_Config):
    data_provider_type: str = "snowflake-federated"
    is_oauth: bool = False
    password: str = field(repr=False, default=None)

    host: str = None
    warehouse: str = None
    username: str = None
    port: str = None
    role: str = None

    _field_map: dict = field(
        default_factory=lambda: {
            "user": "username",
        },
        repr=False,
        init=False,
    )

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "password",
            "port",
            "host",
            "warehouse",
            "username",  # Will be mapped to "user" in to_dict
            "role",
        ]
    )


@register_account_config("snowflake-internal-unload")
@dataclass
class DomoAccount_Config_SnowflakeInternalUnload(DomoAccount_Config):
    is_oauth: bool = False
    data_provider_type: str = "snowflake-internal-unload"

    password: str = field(repr=False, default=None)
    account: str = None
    username: str = None
    role: str = None

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "password",
            "role",
            "account",
            "username",
        ]
    )


@register_account_config("snowflakekeypairauthentication")
@dataclass
class DomoAccount_Config_SnowflakeKeyPairAuthentication(DomoAccount_Config):
    data_provider_type: str = "snowflakekeypairauthentication"
    is_oauth: bool = False

    private_key: str = field(repr=False, default=None)
    account: str = field(repr=False, default=None)
    passphrase: str = field(repr=False, default=None)
    username: str = None
    role: str = None

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "private_key",
            "role",
            "account",
            "username",
            "passphrase",
        ]
    )

    _field_map: dict = field(
        default_factory=lambda: {
            "passPhrase": "passphrase",
        },
        repr=False,
        init=False,
    )


@register_account_config("snowflake-key-pair-writeback")
@dataclass
class DomoAccount_Config_SnowflakeKeyPairWriteback(DomoAccount_Config):
    """Snowflake Key Pair Authentication for Writeback"""

    data_provider_type: str = "snowflake-key-pair-writeback"
    is_oauth: bool = False

    private_key: str = field(repr=False, default=None)
    account: str = None
    passphrase: str = field(repr=False, default=None)
    username: str = None
    role: str = None

    _field_map: dict = field(
        default_factory=lambda: {
            "passPhrase": "passphrase",
        },
    )
    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "private_key",
            "role",
            "account",
            "username",
            "passphrase",
        ]
    )


@register_account_config("snowflake-key-pair-unload-v2")
@dataclass
class DomoAccount_Config_SnowflakeKeyPairUnload_V2(DomoAccount_Config):
    """Snowflake Key Pair Authentication for Unload V2"""

    data_provider_type: str = "snowflake-key-pair-unload-v2"
    is_oauth: bool = False

    private_key: str = field(repr=False, default=None)
    account: str = None
    passphrase: str = field(repr=False, default=None)
    username: str = None
    role: str = None

    access_key: str = None
    secret_key: str = field(repr=False, default=None)
    bucket: str = None
    region: str = None
    encryption_type: str = None

    _field_map: dict = field(
        default_factory=lambda: {
            "passPhrase": "passphrase",
        },
    )

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "private_key",
            "role",
            "account",
            "username",
            "passphrase",
            "access_key",
            "secret_key",
            "bucket",
            "region",
            "encryption_type",
        ]
    )


@register_account_config("snowflake-keypair-internal-managed-unload")
@dataclass
class DomoAccount_Config_SnowflakeKeyPairInternalManagedUnload(DomoAccount_Config):
    """Snowflake Key Pair Internal Managed Unload"""

    data_provider_type: str = "snowflake-keypair-internal-managed-unload"
    is_oauth: bool = False

    private_key: str = field(repr=False, default=None)
    account: str = None
    passphrase: str = field(repr=False, default=None)
    username: str = None
    role: str = None

    _field_map: dict = field(
        default_factory=lambda: {
            "passPhrase": "passphrase",
        },
    )
