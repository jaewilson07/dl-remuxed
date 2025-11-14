r"""
Test file generated from filesets.ipynb
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
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
        domo_instance=os.environ["DOMO_INSTANCE"],
    )

    await auth.who_am_i()




async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    await auth.print_is_token()


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    get_args(EmbedData_Type)

    img_path = "../test/route_sample.png"
    try:
        assert os.path.exists(img_path), f"Image file {img_path} does not exist."

        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                encoded_string = str(base64.b64encode(f.read()))

            print(await embed_image(
                auth=auth,
                debug_api=True,
                debug_num_stacks_to_drop=1,
                image_data=encoded_string,
                media_type="image/png",
                data_type="base64",
                model="domo.domo_ai",

            ))
    except (AssertionError , dmde.DomoError ) as e:
        print(e)
