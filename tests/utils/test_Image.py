r"""
Test file generated from Image.ipynb
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
    img = None
    try:
        img = Image.from_image_file(image_path="../test/route_sample.png")

    except Exception as e:
        print(e)
    img


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    img.crop_square()


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    byte_arr = img.to_bytes()

    Image.from_bytestr(byte_arr)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    img2 = Image.from_image_file("../test/route_sample.png")
    img2


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    are_same_image(domo_default_img, img2)
