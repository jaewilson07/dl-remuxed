"""Example: Dynamic property registration using different approaches.

This demonstrates three approaches to dynamically register conformed properties:
1. Function-based registration (after class definition)
2. Class decorator (at class definition time)
3. Metaclass (most powerful, controls class creation)
"""

from dataclasses import dataclass, field
from typing import Any

from domolibrary2.classes.DomoDataset.stream_configs._conformed import (
    CONFORMED_PROPERTIES,
)


# ============================================================================
# Approach 1: Function-Based Registration (Simple, Explicit)
# ============================================================================


def register_conformed_properties_v1(cls, properties_registry=CONFORMED_PROPERTIES):
    """Register all conformed properties as @property methods.

    Call this after class definition:
        class DomoStream:
            ...

        register_conformed_properties_v1(DomoStream)
    """
    property_map = {
        "query": ("sql", "SQL query"),
        "database": ("database", "database name"),
        "schema": ("schema", "schema name"),
        "warehouse": ("warehouse", "compute warehouse"),
        "table": ("table", "table name"),
        "report_id": ("report_id", "report/survey ID"),
        "spreadsheet": ("spreadsheet", "spreadsheet ID"),
        "bucket": ("bucket", "S3 bucket"),
        "dataset_id": ("dataset_id", "dataset ID"),
        "file_url": ("file_url", "file URL"),
        "host": ("host", "host address"),
        "port": ("port", "port number"),
    }

    for conf_name, conf_prop in properties_registry.items():
        if conf_name not in property_map:
            continue

        prop_name, desc = property_map[conf_name]

        # Skip if already exists
        if hasattr(cls, prop_name):
            continue

        # Create getter function with closure
        def make_getter(cn):
            def getter(self):
                return self._get_conformed_value(cn)

            return getter

        # Create property
        prop = property(
            make_getter(conf_name),
            doc=f"Get {desc} (cross-platform). Providers: {len(conf_prop.supported_providers)}",
        )

        setattr(cls, prop_name, prop)

    return cls


# ============================================================================
# Approach 2: Class Decorator (Pythonic, Declarative)
# ============================================================================


def with_conformed_properties(properties_registry=CONFORMED_PROPERTIES):
    """Class decorator to automatically add conformed properties.

    Usage:
        @with_conformed_properties()
        class DomoStream:
            def _get_conformed_value(self, name):
                ...
    """

    def decorator(cls):
        return register_conformed_properties_v1(cls, properties_registry)

    return decorator


# ============================================================================
# Approach 3: Metaclass (Most Powerful, Full Control)
# ============================================================================


class ConformedPropertyMeta(type):
    """Metaclass that automatically registers conformed properties.

    Usage:
        class DomoStream(metaclass=ConformedPropertyMeta):
            _conformed_properties = CONFORMED_PROPERTIES
            ...
    """

    def __new__(mcs, name, bases, namespace, **kwargs):
        # Create the class first
        cls = super().__new__(mcs, name, bases, namespace)

        # Check if class wants conformed properties
        properties_registry = namespace.get("_conformed_properties")
        if properties_registry:
            register_conformed_properties_v1(cls, properties_registry)

        return cls


# ============================================================================
# Approach 4: Lazy Property (Runtime Registration)
# ============================================================================


class LazyConformedProperty:
    """Descriptor that creates properties on first access.

    Usage:
        class DomoStream:
            sql = LazyConformedProperty("query")
            database = LazyConformedProperty("database")
    """

    def __init__(self, conf_name: str):
        self.conf_name = conf_name
        self.attr_name = f"_cached_{conf_name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Check cache
        if not hasattr(obj, self.attr_name):
            # Get value and cache it
            value = obj._get_conformed_value(self.conf_name)
            setattr(obj, self.attr_name, value)

        return getattr(obj, self.attr_name)

    def __set_name__(self, owner, name):
        """Called when the descriptor is assigned to a class attribute."""
        self.name = name


# ============================================================================
# Example Usage
# ============================================================================


def example_function_based():
    """Example: Function-based registration."""

    @dataclass
    class ExampleStream:
        data_provider_key: str = "snowflake"
        configuration: list = field(default_factory=list)

        def _get_conformed_value(self, name):
            return f"value_{name}"

    # Register properties after class definition
    register_conformed_properties_v1(ExampleStream)

    # Now properties are available
    stream = ExampleStream()
    print(f"SQL: {stream.sql}")
    print(f"Database: {stream.database}")


def example_decorator_based():
    """Example: Decorator-based registration."""

    @with_conformed_properties()
    @dataclass
    class ExampleStream:
        data_provider_key: str = "snowflake"

        def _get_conformed_value(self, name):
            return f"value_{name}"

    stream = ExampleStream()
    print(f"SQL: {stream.sql}")


def example_metaclass_based():
    """Example: Metaclass-based registration."""

    @dataclass
    class ExampleStream(metaclass=ConformedPropertyMeta):
        _conformed_properties = CONFORMED_PROPERTIES
        data_provider_key: str = "snowflake"

        def _get_conformed_value(self, name):
            return f"value_{name}"

    stream = ExampleStream()
    print(f"SQL: {stream.sql}")


def example_lazy_property():
    """Example: Lazy property descriptor."""

    @dataclass
    class ExampleStream:
        data_provider_key: str = "snowflake"

        # Explicitly define properties with descriptors
        sql = LazyConformedProperty("query")
        database = LazyConformedProperty("database")

        def _get_conformed_value(self, name):
            print(f"Computing value for {name}")
            return f"value_{name}"

    stream = ExampleStream()
    print(stream.sql)  # Prints "Computing..." on first access
    print(stream.sql)  # Uses cached value


if __name__ == "__main__":
    print("=" * 80)
    print("Dynamic Property Registration Examples")
    print("=" * 80)

    print("\n1. Function-based:")
    example_function_based()

    print("\n2. Decorator-based:")
    example_decorator_based()

    print("\n3. Metaclass-based:")
    example_metaclass_based()

    print("\n4. Lazy property:")
    example_lazy_property()
