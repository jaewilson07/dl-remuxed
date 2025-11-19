"""Proof of concept: Replace manual properties with dynamic registration.

This demonstrates how to migrate from manually defined properties to
dynamically registered ones.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dataclasses import dataclass, field
from typing import Any

from domolibrary2.classes.DomoDataset.stream_configs._conformed import (
    CONFORMED_PROPERTIES,
    ConformedProperty,
)


# ============================================================================
# Current Implementation (Manual Properties)
# ============================================================================


@dataclass
class DomoStream_Manual:
    """Current approach: 12 manually defined properties."""

    data_provider_key: str = "snowflake"
    configuration: list = field(default_factory=list)

    def _get_conformed_value(self, name):
        return f"value_{name}"

    # All 12 properties manually defined
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

    @property
    def report_id(self):
        return self._get_conformed_value("report_id")

    @property
    def spreadsheet(self):
        return self._get_conformed_value("spreadsheet")

    @property
    def bucket(self):
        return self._get_conformed_value("bucket")

    @property
    def dataset_id(self):
        return self._get_conformed_value("dataset_id")

    @property
    def file_url(self):
        return self._get_conformed_value("file_url")

    @property
    def host(self):
        return self._get_conformed_value("host")

    @property
    def port(self):
        return self._get_conformed_value("port")


# ============================================================================
# Proposed Implementation (Dynamic Registration)
# ============================================================================


def register_conformed_properties(cls, properties_registry=CONFORMED_PROPERTIES):
    """Register conformed properties onto a class dynamically."""

    # Map registry names to property names
    property_map = {
        "query": "sql",  # query -> sql property
        "database": "database",
        "schema": "schema",
        "warehouse": "warehouse",
        "table": "table",
        "report_id": "report_id",
        "spreadsheet": "spreadsheet",
        "bucket": "bucket",
        "dataset_id": "dataset_id",
        "file_url": "file_url",
        "host": "host",
        "port": "port",
        # custom_query is internal, not exposed
    }

    for conf_name, conf_prop in properties_registry.items():
        if conf_name not in property_map:
            continue

        prop_name = property_map[conf_name]

        # Skip if already exists (allow manual override)
        if hasattr(cls, prop_name):
            continue

        # Create getter with closure over conf_name
        def make_getter(cn):
            def getter(self):
                # Special case for sql: try query first, then custom_query
                if cn == "query":
                    result = self._get_conformed_value("query")
                    if result:
                        return result
                    return self._get_conformed_value("custom_query")
                return self._get_conformed_value(cn)

            return getter

        # Create docstring
        providers_list = ", ".join(conf_prop.supported_providers[:3])
        if len(conf_prop.supported_providers) > 3:
            providers_list += f", ... ({len(conf_prop.supported_providers)} total)"

        doc = f"""Get {conf_prop.description or prop_name} (cross-platform).

        {conf_prop.description or 'Configuration parameter'}

        Supported providers: {providers_list}

        Returns:
            str | None: Value from configuration or None if not available

        Example:
            >>> stream = await DomoStream.get_by_id(auth, stream_id)
            >>> print(stream.{prop_name})
        """

        # Create property
        getter = make_getter(conf_name)
        getter.__doc__ = doc
        getter.__name__ = f"get_{prop_name}"

        prop = property(getter)
        setattr(cls, prop_name, prop)

    return cls


@dataclass
class DomoStream_Dynamic:
    """Proposed approach: Properties registered dynamically."""

    data_provider_key: str = "snowflake"
    configuration: list = field(default_factory=list)

    def _get_conformed_value(self, name):
        return f"value_{name}"


# Register properties dynamically
register_conformed_properties(DomoStream_Dynamic)


# ============================================================================
# Hybrid Approach (Best of Both Worlds)
# ============================================================================


@dataclass
class DomoStream_Hybrid:
    """Hybrid: Manual for key properties, dynamic for the rest."""

    data_provider_key: str = "snowflake"
    configuration: list = field(default_factory=list)

    def _get_conformed_value(self, name):
        return f"value_{name}"

    # Manually define TOP 3 most important properties with detailed docs
    @property
    def sql(self) -> str | None:
        """Get SQL query from stream configuration (cross-platform).

        This is the most commonly used property. Works across all SQL-based
        data providers including Snowflake, AWS Athena, and PostgreSQL.

        Automatically handles different parameter names:
        - Snowflake: uses 'query' parameter
        - Amazon Athena High Bandwidth: uses 'enteredCustomQuery'
        - Snowflake Internal Unload: uses 'customQuery'

        Returns:
            SQL query string, or None if stream doesn't use SQL

        Example:
            >>> stream = await DomoStream.get_by_id(auth, stream_id)
            >>> if stream.sql:
            ...     print(f"Query: {stream.sql}")
        """
        result = self._get_conformed_value("query")
        if result:
            return result
        return self._get_conformed_value("custom_query")

    @property
    def database(self) -> str | None:
        """Get database name (cross-platform).

        Works for Snowflake, AWS Athena, PostgreSQL, and other database connectors.
        """
        return self._get_conformed_value("database")

    @property
    def warehouse(self) -> str | None:
        """Get compute warehouse (Snowflake-specific).

        Only applicable for Snowflake connectors. Returns None for other providers.
        """
        return self._get_conformed_value("warehouse")


# Dynamically register remaining 9 properties
_remaining_props = {
    k: v
    for k, v in CONFORMED_PROPERTIES.items()
    if k not in ["query", "custom_query", "database", "warehouse"]
}
register_conformed_properties(DomoStream_Hybrid, _remaining_props)


# ============================================================================
# Comparison Tests
# ============================================================================


def test_all_approaches():
    """Compare manual, dynamic, and hybrid approaches."""
    print("=" * 80)
    print("Comparison: Manual vs Dynamic vs Hybrid Property Registration")
    print("=" * 80)

    # Manual approach
    manual = DomoStream_Manual()
    print("\n1. Manual Properties:")
    print(f"   SQL: {manual.sql}")
    print(f"   Database: {manual.database}")
    print(f"   Lines of code: ~60 (12 properties × 5 lines each)")

    # Dynamic approach
    dynamic = DomoStream_Dynamic()
    print("\n2. Dynamic Properties:")
    print(f"   SQL: {dynamic.sql}")
    print(f"   Database: {dynamic.database}")
    print(f"   Lines of code: ~5 (just _get_conformed_value)")

    # Hybrid approach
    hybrid = DomoStream_Hybrid()
    print("\n3. Hybrid Properties:")
    print(f"   SQL: {hybrid.sql}")
    print(f"   Database: {hybrid.database}")
    print(f"   Schema: {hybrid.schema}")  # Dynamically registered
    print(f"   Lines of code: ~25 (3 manual + dynamic registration)")

    # Verify all properties exist
    print("\n4. Property Verification:")
    expected_props = [
        "sql",
        "database",
        "warehouse",
        "schema",
        "table",
        "report_id",
        "spreadsheet",
        "bucket",
        "dataset_id",
        "file_url",
        "host",
        "port",
    ]

    for cls_name, cls in [
        ("Manual", DomoStream_Manual),
        ("Dynamic", DomoStream_Dynamic),
        ("Hybrid", DomoStream_Hybrid),
    ]:
        missing = [p for p in expected_props if not hasattr(cls, p)]
        if missing:
            print(f"   {cls_name}: MISSING {missing}")
        else:
            print(f"   {cls_name}: ✓ All {len(expected_props)} properties exist")

    # Check docstrings
    print("\n5. Docstring Comparison:")
    print(f"   Manual.sql: {len(DomoStream_Manual.sql.__doc__) if DomoStream_Manual.sql.__doc__ else 0} chars")
    print(f"   Dynamic.sql: {len(DomoStream_Dynamic.sql.__doc__) if DomoStream_Dynamic.sql.__doc__ else 0} chars")
    print(f"   Hybrid.sql: {len(DomoStream_Hybrid.sql.__doc__) if DomoStream_Hybrid.sql.__doc__ else 0} chars")

    # Performance comparison
    print("\n6. Performance (1000 property accesses):")
    import time

    def benchmark(stream, iterations=1000):
        start = time.time()
        for _ in range(iterations):
            _ = stream.sql
            _ = stream.database
            _ = stream.warehouse
        return (time.time() - start) * 1000  # Convert to ms

    manual_time = benchmark(manual)
    dynamic_time = benchmark(dynamic)
    hybrid_time = benchmark(hybrid)

    print(f"   Manual: {manual_time:.3f}ms")
    print(f"   Dynamic: {dynamic_time:.3f}ms")
    print(f"   Hybrid: {hybrid_time:.3f}ms")
    print(f"   Difference: {abs(manual_time - dynamic_time):.3f}ms (negligible)")


if __name__ == "__main__":
    test_all_approaches()

    print("\n" + "=" * 80)
    print("Conclusion")
    print("=" * 80)
    print("""
    Manual:  Best for explicit control, detailed docs
    Dynamic: Best for scalability, DRY principle
    Hybrid:  Best of both - recommended for production

    Recommendation: Use Hybrid approach
    - Manual properties for top 3-5 most used (sql, database, warehouse)
    - Dynamic registration for remaining properties
    - Easy to add new properties without code changes
    """)
