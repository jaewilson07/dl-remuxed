r"""
Test file generated from 95_DomoAuth.ipynb
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
    try:
        # print((await full_auth.who_am_i()))
        await full_auth.elevate_otp(debug_api=False, one_time_password=840573)

    except dmde.DomoError as e:
        print(e)


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    try:
        domo_auth = DomoTokenAuth(
            domo_instance=os.environ["DOMO_INSTANCE"], domo_access_token="fake password"
        )

        # await domo_auth.who_am_i(debug_api = True)
        await domo_auth.print_is_token(debug_api=False)


    except InvalidCredentialsError as e:
        print(e)
