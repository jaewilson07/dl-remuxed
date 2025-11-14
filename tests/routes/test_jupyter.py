r"""
Test file generated from jupyter.ipynb
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
    dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_DOJO_INSTANCE"],
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )




async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    tests = [
        './admin/hello_world.ipynb',
        './admin/new_folder',
        'admin',
        ''
    ]

    for test in tests:
        print(f"{test} - {generate_update_jupyter_body__new_content_path(test)}")


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    generate_update_jupyter_body("hello world", "hi.md")


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    generate_update_jupyter_body(None, "admin/new_folder")


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    try:
        await create_jupyter_obj(
            content_path=f"admin-{dt.date.today()}/", auth=dj_auth, debug_api=True
        )


    except dmde.DomoError as e:
        print(e)
