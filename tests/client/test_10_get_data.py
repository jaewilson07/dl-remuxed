"""
Test file generated from 10_get_data.ipynb
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
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    async def test_route_fn(auth = auth ):
        url = f"https://{ auth.domo_instance}.domo.com/api/content/v2/users"

        return await get_data(
            url=url,
            method="GET",
            auth=auth,
            debug_api=False,
            debug_traceback=False,
            num_stacks_to_drop=1,
        )

    res = await test_route_fn(auth = auth)
    res
    pprint({"traceback_details": res.traceback_details.__dict__})

    pd.DataFrame(res.response[0:5])


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    class Foo:
        async def test_route_fn(self, auth: dmda.DomoAuth):
            url = f"https://{ auth.domo_instance}.domo.com/api/content/v2/users"

            res = await get_data(
                url=url,
                method="GET",
                auth=auth,
                debug_api=False,
                debug_traceback=False,
                num_stacks_to_drop=1,
                parent_class=self.__class__.__name__,
            )
            return res


    test_foo = Foo()
    res = await test_foo.test_route_fn(auth=auth)


    pprint({"traceback_details": res.traceback_details.__dict__})


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await auth.who_am_i()

    pixels = 300
    debug_api = False

    url = f"https://{auth.domo_instance}.domo.com/api/content/v1/avatar/USER/{auth.user_id}?size={pixels}"

    res = await get_data_stream(
        url=url,
        method="GET",
        auth=auth,
        debug_api=False,
        headers={"accept": "image/png;charset=utf-8"},
        num_stacks_to_drop=0,
    )

    folder_path = "../test"

    dmfi.upsert_folder(folder_path)

    local_filename = f"{folder_path}/{auth.user_id}.png"

    with open(local_filename, "wb") as f:
        f.write(res.response)

    res


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    try:
        raise RouteFunction_ResponseTypeError("hello world")

    except RouteFunction_ResponseTypeError as e:
        print(e)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    @route_function
    async def test_fn(
        parent_class=None, debug_num_stacks_to_drop=1, debug_api=True, session=None
    ):
        return rgd.ResponseGetData(status=200, response=100, is_success=True)


    await test_fn()
