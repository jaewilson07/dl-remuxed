"""
Test file for DomoDataset_Schema
Following the DomoUser.py test pattern
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoDataset.Schema as schema
from domolibrary2.classes.DomoDataset.Schema import (
    DomoDataset_Schema,
    DomoDataset_Schema_Column,
    DatasetSchema_Types,
    DatasetSchema_InvalidSchema,
    CRUD_Dataset_Error,
)

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

# Test dataset ID - should be set in .env file
TEST_DATASET_ID_1 = os.environ.get("DATASET_ID_1")


async def test_cell_0(token_auth=token_auth) -> str:
    """Helper function to verify authentication."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth.user_id


async def test_cell_1(token_auth=token_auth):
    """Test Schema creation and get method."""
    # Create a mock parent object for testing
    class MockParent:
        def __init__(self, auth, dataset_id):
            self.auth = auth
            self.id = dataset_id
            self.name = "Test Dataset"

    parent = MockParent(token_auth, TEST_DATASET_ID_1)
    
    # Create schema instance
    dataset_schema = DomoDataset_Schema(
        auth=token_auth,
        parent=parent,
        parent_id=TEST_DATASET_ID_1,
    )

    # Get schema from API
    columns = await dataset_schema.get(debug_api=False, return_raw=False)
    
    assert columns is not None
    assert len(columns) > 0
    assert isinstance(columns[0], DomoDataset_Schema_Column)
    
    print(f"Schema has {len(columns)} columns")
    return dataset_schema


async def test_cell_2(token_auth=token_auth):
    """Test Schema to_dict method."""
    # Create a mock parent
    class MockParent:
        def __init__(self, auth, dataset_id):
            self.auth = auth
            self.id = dataset_id
            self.name = "Test Dataset"

    parent = MockParent(token_auth, TEST_DATASET_ID_1)
    
    # Create schema with test columns
    dataset_schema = DomoDataset_Schema(
        auth=token_auth,
        parent=parent,
        parent_id=TEST_DATASET_ID_1,
        columns=[
            DomoDataset_Schema_Column(
                name="test_col_1",
                id="1",
                type=DatasetSchema_Types.STRING,
                order=0,
                visible=True,
            ),
            DomoDataset_Schema_Column(
                name="test_col_2",
                id="2",
                type=DatasetSchema_Types.DOUBLE,
                order=1,
                visible=True,
            ),
        ],
    )

    schema_dict = dataset_schema.to_dict()
    
    assert "columns" in schema_dict
    assert len(schema_dict["columns"]) == 2
    assert schema_dict["columns"][0]["name"] == "test_col_1"
    
    print(f"Schema dict: {schema_dict}")
    return schema_dict


async def test_cell_3(token_auth=token_auth):
    """Test DomoDataset_Schema_Column from_dict method."""
    test_obj = {
        "name": "test_column",
        "id": "123",
        "type": "STRING",
        "visible": True,
        "upsertKey": False,
        "order": 0,
        "tags": ["tag1", "tag2"],
    }

    column = DomoDataset_Schema_Column.from_dict(test_obj)
    
    assert column.name == "test_column"
    assert column.id == "123"
    assert column.type == "STRING"
    assert column.visible is True
    assert column.upsert_key is False
    assert len(column.tags) == 2
    
    print(f"Column created: {column.name} ({column.type})")
    return column


async def test_cell_4(token_auth=token_auth):
    """Test add_col and remove_col methods."""
    # Create a mock parent
    class MockParent:
        def __init__(self, auth, dataset_id):
            self.auth = auth
            self.id = dataset_id
            self.name = "Test Dataset"

    parent = MockParent(token_auth, TEST_DATASET_ID_1)
    
    dataset_schema = DomoDataset_Schema(
        auth=token_auth,
        parent=parent,
        parent_id=TEST_DATASET_ID_1,
    )

    # Test add_col
    new_col = DomoDataset_Schema_Column(
        name="new_column",
        id="999",
        type=DatasetSchema_Types.STRING,
    )
    
    dataset_schema.add_col(new_col, debug_prn=True)
    assert len(dataset_schema.columns) == 1
    assert dataset_schema.columns[0].name == "new_column"
    
    # Test remove_col
    dataset_schema.remove_col(new_col)
    assert len(dataset_schema.columns) == 0
    
    print("✓ add_col and remove_col work correctly")
    return dataset_schema


async def main(token_auth=token_auth):
    """Run all test functions."""
    fn_ls = [
        test_cell_0,
        test_cell_1,
        test_cell_2,
        test_cell_3,
        test_cell_4,
    ]
    
    for fn in fn_ls:
        print(f"\n{'='*60}")
        print(f"Running: {fn.__name__}")
        print(f"{'='*60}")
        try:
            result = await fn(token_auth=token_auth)
            print(f"✓ {fn.__name__} passed")
        except Exception as e:
            print(f"✗ {fn.__name__} failed: {e}")
            raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(main(token_auth=token_auth))
