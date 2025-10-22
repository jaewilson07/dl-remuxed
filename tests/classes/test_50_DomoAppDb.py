"""
Test file generated from 50_DomoAppDb.ipynb
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
    DATASTORE_ID = '5e871f13-69d4-4012-8710-b61f654bb2b9'
    COLLECTION_ID = 'd2b23a60-b1d3-4577-ac85-32ecc619708a'
    DOCUMENT_ID = '37948887-8ba3-4465-a749-c09518930229'

    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    await AppDbDocument.get_by_id(
        auth = auth,
        collection_id= COLLECTION_ID,
        document_id= DOCUMENT_ID,
        identity_columns= ['id'],
        return_raw= False
    )


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_doc = await AppDbDocument.get_by_id(
        auth = auth,
        collection_id= COLLECTION_ID,
        document_id= DOCUMENT_ID,
        identity_columns= ['id']
    )

    content = {'update': 'update_via_content',  'id' : 12387 , "update_dt" : str(dt.date.today())}

    (await domo_doc.update_document(debug_api=False, content = content)).response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    domo_doc.content.update({ 'update': 'update via obj', 'update_dt' : dt.date.today()})

    (await domo_doc.update_document(debug_api=False)).response


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    domo_collection = await AppDbCollection.get_by_id(auth = auth, 
                              collection_id= COLLECTION_ID,
                              debug_api= False
                              )

    await domo_collection.share_collection()


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    filters = {"content.id": "abc"}


    domo_collection = await AppDbCollection.get_by_id(
        auth=auth, collection_id=COLLECTION_ID, return_raw=False
    )

    await domo_collection.query_documents(
        # filters = filters
    )

    [domo_doc.to_dict() for domo_doc in domo_collection.domo_documents]


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    await AppDbDocument.get_by_id(auth=auth,
                                     debug_api= False,
                                     collection_id = COLLECTION_ID,
                                     document_id = DOCUMENT_ID
                                     )


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    await AppDbDocument.upsert(
        auth = auth,
        collection_id = COLLECTION_ID,
        identity_columns = ['id'],
        content = {'update': 'testing_upsert', 'update_dt': '2024-06-28', 'id': 12387},
        debug_api = False
    )


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    @dataclass
    class TestDoc(AppDbDocument):
        id : int = None
        update :str = None
        update_dt : dt.date = None
        _identity_columns : List[str] = field(default_factory = ['id'])

        def __post_init__(self):
            self._identity_columns = ['id']


    await TestDoc.get_by_id(collection_id= COLLECTION_ID,
                            document_id= DOCUMENT_ID,
                            auth = auth)

    await TestDoc.upsert(
        auth = auth,
        collection_id = COLLECTION_ID,
        identity_columns = ['id'],
        content={'update': 'upsert_via_class', 'id': 123, 'update_dt': '2024-06-28'}
    )


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    domo_collections = await AppDbCollections.get_collections(auth = auth)
    domo_collections[0:5]
