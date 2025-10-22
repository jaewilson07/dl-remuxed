"""
Test file generated from 50_DomoUser.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.routes.user as user_routes
import domolibrary2.classes.DomoUser as dmdu
from domolibrary2.routes.user import UserProperty_Type, UserProperty, User_CRUD_Error

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

TEST_USER_ID_1 = int(os.environ.get("USER_ID_1", 0))


async def test_cell_0(token_auth=token_auth) -> str:
    """Helper function to get the user ID of the authenticated user."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth.user_id


async def test_cell_1(token_auth=token_auth) -> dmdu.DomoUser:
    """Test case from cell 1"""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    user_id = token_auth.user_id

    domo_user = await dmdu.DomoUser.get_by_id(
        user_id=user_id, auth=token_auth, return_raw=False
    )
    return domo_user


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    if not token_auth.user_id:
        await token_auth.who_am_i()

    user_id = token_auth.user_id

    domo_user = await dmdu.DomoUser.get_by_id(
        user_id=user_id, auth=token_auth, return_raw=False
    )

    img = await domo_user.download_avatar(
        folder_path="./EXPORTS/classes/DomoUser",
        img_name="cls_sample.png",
        return_raw=False,
        debug_api=False,
    )

    return img


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""

    domo_user = await dmdu.DomoUser.get_by_id(user_id=TEST_USER_ID_1, auth=token_auth)

    print(domo_user.display_url)

    property_ls = [
        UserProperty(UserProperty_Type.display_name, "test 3"),
        UserProperty(UserProperty_Type.email_address, "test33@test.com"),
        UserProperty(UserProperty_Type.role_id, 5),
    ]

    try:
        await domo_user.update_properties(property_ls=property_ls, debug_api=False)
    except User_CRUD_Error as e:
        print(e)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""

    domo_user = None
    try:
        domo_user = await dmdu.DomoUser.create(
            auth=token_auth,
            email_address="test4@test.com",
            display_name="tony the tiger",
            role_id=3,
            debug_api=False,
        )

        print(domo_user)

    except dmdu.User_CRUD_Error as e:
        print(e)

    try:
        if domo_user:
            await domo_user.delete()

    except dmdu.User_CRUD_Error as e:
        print(e)


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    assert await token_auth.who_am_i()

    domo_user = await dmdu.DomoUser.get_by_id(
        user_id=token_auth.user_id, auth=token_auth
    )

    tokens = await domo_user.get_access_tokens(return_raw=False, debug_api=True)

    print({"Tokens": len(tokens), "user_id": domo_user.id})


async def main(token_auth=token_auth):
    fn_ls = [
        test_cell_0,
        test_cell_1,
        test_cell_2,
        test_cell_3,
        test_cell_4,
        test_cell_7,
    ]
    for fn in fn_ls:
        await fn(token_auth=token_auth)


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        main(token_auth=token_auth),
    )


# async def test_cell_6(token_auth=token_auth):
#     """Test case from cell 6"""
#     user_id = 1216550715

#     domo_user = await DomoUser.get_by_id(user_id=user_id, auth=auth)

#     try:
#         avatar = Image.from_image_file("images/128618865.png")

#         await domo_user.upload_avatar(avatar=avatar, return_raw=False)

#     except Exception as e:
#         print(e)


# async def test_cell_8(token_auth=token_auth):
#     """Test case from cell 8"""
#     domo_users = DomoUsers(auth=auth)

#     await domo_users.get(debug_api=False, return_raw=False)

#     domo_users = [
#         domo_user
#         for domo_user in domo_users.users
#         if "test" in domo_user.email_address.lower()
#     ]
#     domo_users


# async def test_cell_9(token_auth=token_auth):
#     """Test case from cell 9"""
#     domo_users = DomoUsers(auth=auth)

#     await domo_users.search_by_email(
#         email="jae@datacrew.space",
#         only_allow_one=True,
#         return_raw=False,
#         debug_api=False,
#         suppress_no_results_error=False,
#     )


# async def test_cell_10(token_auth=token_auth):
#     """Test case from cell 10"""
#     await DomoUsers.by_id(
#         auth=auth,
#         user_ids=[domo_user.id],
#         only_allow_one=False,
#         return_raw=False,
#     )


# async def test_cell_11(token_auth=token_auth):
#     """Test case from cell 11"""
#     try:
#         await DomoUsers.virtual_user_by_subscriber_instance(
#             auth=auth,
#             subscriber_instance_ls=[os.environ["DOMO_INSTANCE"], "test"],
#             # return_raw=True,
#             debug_api=False,
#         )
#     except GetUser_Error as e:
#         print(e)


# async def test_cell_12(token_auth=token_auth):
#     """Test case from cell 12"""
#     try:
#         await DomoUsers.create_user(
#             auth=auth,
#             display_name="test_and_delete",
#             email_address="test26@test.com",
#             role_id=5,
#         )
#     except User_CrudError as e:
#         print(e)


# async def test_cell_13(token_auth=token_auth):
#     """Test case from cell 13"""
#     domo_users = DomoUsers(auth=auth)

#     await domo_users.upsert(
#         email_address="test4@test.com",
#         display_name=f"test - updated via dl {dt.date.today()}",
#         role_id=3,
#     )
