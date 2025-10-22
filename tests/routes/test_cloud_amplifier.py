"""
Test file generated from cloud_amplifier.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os
import domolibrary.client.DomoAuth as dmda

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ['DOMO_INSTANCE'],
    domo_access_token=os.environ['DOMO_ACCESS_TOKEN'],
)


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],                                                                                 
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    res = await get_integrations(
        auth = token_auth,
        # integration_engine = "SNOWFLAKE",
    )
    integrations = res.response
    print(f"Found {len(integrations)} accounts")

    integration_id = integrations[0]['id']

    (await get_integration_by_id(
        auth = token_auth,
        integration_id = integration_id,
    )).response


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await token_auth.who_am_i()

    assert token_auth.user_id

    (await get_integration_permissions(
        auth = token_auth,
        user_id = token_auth.user_id,
        integration_ids = [integration_id],
    )).response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    try:
        print(await get_integration_warehouses(
            auth = token_auth,
            integration_id = integration_id,
        )).response

    except dmde.DomoError as e:
        print(e)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    try:
        databases = (
            await get_databases(
                auth=token_auth,
                integration_id=integration_id,
            )
        ).response

        print(databases)

        schemas = (
            await get_schemas(
                auth=token_auth,
                integration_id=integration_id,
                database=databases[0]["databaseName"],
            )
        ).response

        pprint(schemas)

        tables = (
            await get_tables(
                auth=token_auth,
                integration_id=integration_id,
                database=databases[0]["databaseName"],
                schema=schemas[0]["schemaName"],
            )
        ).response

        pprint(tables)

    except dmde.DomoError as e:
        print(e)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    sample_dataset_id = "6b9b4112-6683-434f-b6b5-457946c2f2ca"

    try:
        collisions = await check_for_colliding_datasources(
            auth = token_auth,
            dataset_id = sample_dataset_id,
        )
    except Cloud_Amplifier_Error as e:
        print(e)
    print("Collision check complete")

    try:
        fed_meta = await get_federated_source_metadata(
            auth = token_auth,
            dataset_id = sample_dataset_id,
        )
    except Cloud_Amplifier_Error as e:
        print(e)
    print("Federated metadata retrieved")


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    class Cloud_Amplifier_Warehouse_Activity(DomoEnum):
        QUERY = "query" # Read
        INDEX = "index" # Write
        DATAFLOW = "dataflow" # Transform
