r"""
Test file generated from appdb.ipynb
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


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    datastores = (await get_datastores(auth=auth)).response
    datastores[0:2]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    (await get_datastore_by_id(auth=auth, datastore_id=DATASTORE_ID)).response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    (await get_collections_from_datastore(auth=auth, datastore_id=DATASTORE_ID)).response


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    collections = (await get_collections(auth=auth)).response
    collections[0:2]


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    (
        await get_collection_by_id(auth=auth, collection_id=COLLECTION_ID, debug_api=False)
    ).response


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    documents = (
        await get_documents_from_collection(
            auth=auth, collection_id=COLLECTION_ID, debug_api=False
        )
    ).response
    documents


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    await modify_collection_permissions(
        collection_id="b71d2341-8fe4-41af-b55b-163de11a906d",
        user_id="1893952720",
        permission=Collection_Permission_Enum.READ_CONTENT,
        auth=auth,
    )


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


    (
        await get_collection_document_by_id(
            auth=auth, collection_id=COLLECTION_ID, document_id=documents[0]["id"]
        )
    ).response["content"]
