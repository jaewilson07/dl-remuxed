r"""
Test file generated from convert.ipynb
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
    print_md("hello ***world***")


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    convert_string_to_datetime("2023-06-22T19:34:02.290Z")


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    {

        "getUserData": convert_programming_text_to_title_case("getUserData"),
        "calculateTotalSum": convert_programming_text_to_title_case("calculate_total_sum"),
        "_privateMethod": convert_programming_text_to_title_case("_private_method"),
    }


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    convert_str = "test_snake_case"

    convert_snake_to_pascal(convert_str)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    [
        convert_str_to_snake_case(name, is_only_alphanumeric=True, is_pascal= True)
        for name in [
            "loginEnabled",
        ]
    ]


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    [
        convert_str_to_snake_case(name, is_only_alphanumeric=True)
        for name in [
            "Toolkit: Schema Management",
            "Toolkit: DataSet S3 Backup",
            "Sony Collaboration Publisher Executor",
            "Toolkit: User Automation",
            "Toolkit: DataSet Tag Automation",
        ]
    ]


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    test_valid_email("jae@onyxreporting.com")


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    try:
        test_valid_email("jae myong@onyxreporting.com")
    except InvalidEmail as e:
        print(e)


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    df = pd.DataFrame([{"col_a": "a", "col_b": "b", "col_c": "c"}])

    df_ls = [df, df, df]

    concat_list_dataframe(df_ls)
