"""
Test file generated from DomoError.ipynb
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
    import domolibrary.routes.user as user_route
    import domolibrary.classes.DomoUser as dmdu

    import domolibrary.client.DomoAuth as dmda
    import os


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    try:
        raise DomoError(
            entity_id="ds_123",
            function_name="create_dataset",
            # parent_class = "Foo",
            status=403,
            message="invalid path",
        )
    except DomoError as e:
        print(e)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )
    async def test_fn(user_id):
        res = await user_route.get_all_users(auth = auth,
                                             parent_class = 'test',
                                             debug_num_stacks_to_drop=2)
        res.response = 'hello world'

        raise RouteError(res = res, entity_id = user_id, function_name = 'abc')

    try:
        await test_fn(user_id = None)
    except RouteError as e:
        print(e)
