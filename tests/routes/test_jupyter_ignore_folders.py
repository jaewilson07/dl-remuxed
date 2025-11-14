"""Test ignore_folders parameter in Jupyter content routes."""

import os
from dotenv import load_dotenv
import domolibrary2.auth as dmda

load_dotenv()


def test_path_filtering_logic():
    """Test that path filtering correctly matches segments."""
    # Test data
    test_paths = [
        {"name": "stdout", "path": "recent_executions/file.ipynb/2025-07-17/stdout"},
        {"name": "test.py", "path": "domolibrary/test.py"},
        {"name": "main.ipynb", "path": "notebooks/main.ipynb"},
        {"name": "config.py", "path": "domolibrary/config/config.py"},
        {"name": "temp.txt", "path": "temp/temp.txt"},
    ]

    ignore_folders = ["domolibrary", "temp"]

    # Filter paths
    filtered = [
        f
        for f in test_paths
        if not any(ign in f["path"].split("/") for ign in ignore_folders)
    ]

    # Verify results
    assert len(filtered) == 2, f"Expected 2 paths, got {len(filtered)}"
    assert filtered[0]["name"] == "stdout"
    assert filtered[1]["name"] == "main.ipynb"

    print("✓ Path filtering logic works correctly")
    print(f"  Original: {len(test_paths)} paths")
    print(f"  Filtered: {len(filtered)} paths")
    print(f"  Removed: {[p['name'] for p in test_paths if p not in filtered]}")


async def test_get_content_with_ignore_folders():
    """Test get_content with ignore_folders parameter."""
    # Note: This requires actual Jupyter auth - for integration testing
    jupyter_token = os.environ.get("JUPYTER_TOKEN")
    if not jupyter_token:
        print("⚠ Skipping integration test - no JUPYTER_TOKEN in env")
        return

    auth = dmda.DomoJupyterAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        jupyter_token=jupyter_token,
    )

    from domolibrary2.routes.jupyter import content as jupyter_routes

    # Test with ignore_folders
    res = await jupyter_routes.get_content(
        auth=auth,
        ignore_folders=["domolibrary", ".ipynb_checkpoints"],
        return_raw=True,
    )

    print(f"✓ get_content accepts ignore_folders parameter")
    print(f"  Retrieved {len(res.response)} items")

    # Verify no ignored folders in results
    for item in res.response:
        path_segments = item.get("path", "").split("/")
        assert "domolibrary" not in path_segments
        assert ".ipynb_checkpoints" not in path_segments

    print("✓ No ignored folders in results")


if __name__ == "__main__":
    import asyncio

    # Run unit test
    test_path_filtering_logic()

    # Run integration test if credentials available
    asyncio.run(test_get_content_with_ignore_folders())
