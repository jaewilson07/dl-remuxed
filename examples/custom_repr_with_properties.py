"""Custom __repr__ implementations for DomoStream with conformed properties.

This demonstrates different approaches to include conformed properties in
the string representation of DomoStream objects.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dataclasses import dataclass, field
from typing import Any

from domolibrary2.classes.DomoDataset.stream_configs._conformed import (
    CONFORMED_PROPERTIES,
)


# ============================================================================
# Approach 1: Simple Custom __repr__ (Manual List)
# ============================================================================


@dataclass
class DomoStream_Simple:
    """Simple approach: Manually list properties in __repr__."""

    id: str
    data_provider_key: str = "snowflake"
    data_provider_name: str = "Snowflake"
    parent: Any = field(repr=False, default=None)

    def _get_conformed_value(self, name):
        """Mock for testing."""
        values = {
            "query": "SELECT * FROM table",
            "database": "SA_PRD",
            "warehouse": "COMPUTE_WH",
        }
        return values.get(name)

    @property
    def sql(self):
        return self._get_conformed_value("query")

    @property
    def database(self):
        return self._get_conformed_value("database")

    @property
    def warehouse(self):
        return self._get_conformed_value("warehouse")

    def __repr__(self) -> str:
        """Custom repr with conformed properties."""
        # Start with basic info
        parts = [f"DomoStream(id='{self.id}'"]

        # Add provider info
        if self.data_provider_name:
            parts.append(f"provider='{self.data_provider_name}'")

        # Add conformed properties (manually listed)
        if self.sql:
            sql_preview = self.sql[:50] + "..." if len(self.sql) > 50 else self.sql
            parts.append(f"sql='{sql_preview}'")

        if self.database:
            parts.append(f"database='{self.database}'")

        if self.warehouse:
            parts.append(f"warehouse='{self.warehouse}'")

        return ", ".join(parts) + ")"


# ============================================================================
# Approach 2: Dynamic Discovery (Auto-detect Properties)
# ============================================================================


@dataclass
class DomoStream_Dynamic:
    """Dynamic approach: Automatically discover and include all conformed properties."""

    id: str
    data_provider_key: str = "snowflake"
    data_provider_name: str = "Snowflake"
    parent: Any = field(repr=False, default=None)

    def _get_conformed_value(self, name):
        """Mock for testing."""
        values = {
            "query": "SELECT * FROM table WHERE id = 123",
            "database": "SA_PRD",
            "warehouse": "COMPUTE_WH",
            "schema": "PUBLIC",
        }
        return values.get(name)

    @property
    def sql(self):
        return self._get_conformed_value("query")

    @property
    def database(self):
        return self._get_conformed_value("database")

    @property
    def warehouse(self):
        return self._get_conformed_value("warehouse")

    @property
    def schema(self):
        return self._get_conformed_value("schema")

    def __repr__(self) -> str:
        """Dynamic repr that discovers all properties."""
        parts = [f"DomoStream(id='{self.id}'"]

        # Add provider
        if self.data_provider_name:
            parts.append(f"provider='{self.data_provider_name}'")

        # Discover all properties dynamically
        conformed_props = []
        for attr_name in dir(self):
            # Skip private/magic attributes
            if attr_name.startswith("_"):
                continue

            # Check if it's a property
            attr = getattr(type(self), attr_name, None)
            if not isinstance(attr, property):
                continue

            # Get the value
            try:
                value = getattr(self, attr_name)
                if value is not None:
                    # Truncate long values
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:50] + "..."
                    conformed_props.append((attr_name, value))
            except Exception:
                continue

        # Add properties in a sensible order
        priority = ["sql", "database", "warehouse", "schema"]
        for prop_name in priority:
            for name, value in conformed_props:
                if name == prop_name:
                    parts.append(f"{name}='{value}'")
                    break

        # Add remaining properties
        for name, value in conformed_props:
            if name not in priority:
                parts.append(f"{name}='{value}'")

        return ", ".join(parts) + ")"


# ============================================================================
# Approach 3: Configurable (Control What to Show)
# ============================================================================


@dataclass
class DomoStream_Configurable:
    """Configurable: Specify which properties to include in repr."""

    id: str
    data_provider_key: str = "snowflake"
    data_provider_name: str = "Snowflake"
    parent: Any = field(repr=False, default=None)

    # Configure which properties to show in repr
    _repr_properties: list[str] = field(
        default_factory=lambda: ["sql", "database", "warehouse", "schema"],
        repr=False,
        init=False,
    )

    def _get_conformed_value(self, name):
        """Mock for testing."""
        values = {
            "query": "SELECT * FROM table",
            "database": "SA_PRD",
            "warehouse": "COMPUTE_WH",
            "schema": "PUBLIC",
            "table": "customers",
        }
        return values.get(name)

    @property
    def sql(self):
        return self._get_conformed_value("query")

    @property
    def database(self):
        return self._get_conformed_value("database")

    @property
    def warehouse(self):
        return self._get_conformed_value("warehouse")

    @property
    def schema(self):
        return self._get_conformed_value("schema")

    @property
    def table(self):
        return self._get_conformed_value("table")

    def __repr__(self) -> str:
        """Repr with configurable property list."""
        parts = [f"DomoStream(id='{self.id}'"]

        # Add provider
        if self.data_provider_name:
            parts.append(f"provider='{self.data_provider_name}'")

        # Add configured properties
        for prop_name in self._repr_properties:
            if hasattr(self, prop_name):
                value = getattr(self, prop_name, None)
                if value is not None:
                    # Truncate long strings
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:50] + "..."
                    parts.append(f"{prop_name}='{value}'")

        return ", ".join(parts) + ")"


# ============================================================================
# Approach 4: Registry-Based (Use CONFORMED_PROPERTIES)
# ============================================================================


@dataclass
class DomoStream_Registry:
    """Registry-based: Use CONFORMED_PROPERTIES to discover what to show."""

    id: str
    data_provider_key: str = "snowflake"
    data_provider_name: str = "Snowflake"
    parent: Any = field(repr=False, default=None)

    def _get_conformed_value(self, name):
        """Mock for testing."""
        values = {
            "query": "SELECT * FROM table",
            "database": "SA_PRD",
            "warehouse": "COMPUTE_WH",
            "report_id": None,  # Not applicable for this provider
        }
        return values.get(name)

    @property
    def sql(self):
        return self._get_conformed_value("query")

    @property
    def database(self):
        return self._get_conformed_value("database")

    @property
    def warehouse(self):
        return self._get_conformed_value("warehouse")

    @property
    def report_id(self):
        return self._get_conformed_value("report_id")

    def __repr__(self) -> str:
        """Repr using CONFORMED_PROPERTIES registry."""
        parts = [f"DomoStream(id='{self.id}'"]

        # Add provider
        if self.data_provider_name:
            parts.append(f"provider='{self.data_provider_name}'")

        # Property name mapping (registry name -> property name)
        property_map = {
            "query": "sql",
            "database": "database",
            "warehouse": "warehouse",
            "report_id": "report_id",
        }

        # Check which properties are relevant for this provider
        relevant_props = []
        for conf_name, conf_prop in CONFORMED_PROPERTIES.items():
            # Check if this provider supports this property
            if self.data_provider_key in conf_prop.supported_providers:
                prop_name = property_map.get(conf_name)
                if prop_name and hasattr(self, prop_name):
                    value = getattr(self, prop_name, None)
                    if value is not None:
                        relevant_props.append((prop_name, value))

        # Add properties in priority order
        priority = ["sql", "database", "warehouse", "schema"]
        for prop_name in priority:
            for name, value in relevant_props:
                if name == prop_name:
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:50] + "..."
                    parts.append(f"{name}='{value}'")
                    break

        return ", ".join(parts) + ")"


# ============================================================================
# Demonstration
# ============================================================================


def demo_all_approaches():
    """Demonstrate all __repr__ approaches."""
    print("=" * 80)
    print("Custom __repr__ with Conformed Properties")
    print("=" * 80)

    print("\n1. Simple Approach (Manual List):")
    stream1 = DomoStream_Simple(id="stream-123")
    print(f"   {stream1}")
    print(f"   Length: {len(repr(stream1))} chars")

    print("\n2. Dynamic Discovery (Auto-detect):")
    stream2 = DomoStream_Dynamic(id="stream-456")
    print(f"   {stream2}")
    print(f"   Length: {len(repr(stream2))} chars")

    print("\n3. Configurable (Control What to Show):")
    stream3 = DomoStream_Configurable(id="stream-789")
    print(f"   {stream3}")
    print(f"   Length: {len(repr(stream3))} chars")

    # Test with different configuration
    stream3._repr_properties = ["sql", "database"]  # Only show these two
    print(f"   Custom config: {stream3}")

    print("\n4. Registry-Based (Use CONFORMED_PROPERTIES):")
    stream4 = DomoStream_Registry(id="stream-abc")
    print(f"   {stream4}")
    print(f"   Length: {len(repr(stream4))} chars")

    print("\n" + "=" * 80)
    print("Comparison")
    print("=" * 80)
    print(
        f"""
    Simple:        Clear, explicit, easy to understand
    Dynamic:       Automatic, discovers all properties
    Configurable:  Flexible, user can control output
    Registry:      Smart, only shows relevant properties

    Recommendation: Registry-based for DomoStream
    - Shows only properties relevant to provider type
    - Uses existing CONFORMED_PROPERTIES registry
    - Automatic and intelligent
    """
    )


if __name__ == "__main__":
    demo_all_approaches()
