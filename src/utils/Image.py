__all__ = [
    "isBase64",
    "handle_string_to_bytes_and_decode",
    "handle_string_to_bytes_and_encode",
    "are_same_image",
    "Image",
]

import base64
import io
import os

from typing import Union

import numpy as np
import PIL
from PIL.Image import Image


def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False


def handle_string_to_bytes_and_decode(data: Union[str, bytes]):

    if isinstance(data, str):
        data = bytes(data)

    if isBase64(data):
        data = base64.b64decode(data)

    return data


def handle_string_to_bytes_and_encode(data: Union[str, bytes]):

    if isinstance(data, str):
        data = bytes(data)

    if not isBase64(data):
        data = base64.b64encode(data)

    return data


# Monkey-patch methods directly onto PIL.Image.Image class
def _image_to_bytes(self) -> bytes:
    byte_arr = io.BytesIO()

    if not hasattr(self, "area"):
        self.area = self

    self.area.save(byte_arr, format=self.format)

    self.data = byte_arr.getvalue()

    return self.data


def _image_crop_square(self):

    width, height = self.size  # Get dimensions

    new_edge = min(width, height)

    left = (width - new_edge) / 2
    top = (height - new_edge) / 2
    right = (width + new_edge) / 2
    bottom = (height + new_edge) / 2

    # Crop the center of the image
    self.area = self.crop((left, top, right, bottom))

    self.to_bytes()

    return self.area


def _image_from_image_file(cls, image_path: str) -> Image:
    if not os.path.exists(image_path):
        raise FileNotFoundError(image_path)

    with open(image_path, "rb") as file:
        data = file.read()

    data = handle_string_to_bytes_and_decode(data)

    im = PIL.Image.open(io.BytesIO(data))

    return im


def _image_from_bytestr(cls, data: Union[str, bytes]) -> Image:

    data = handle_string_to_bytes_and_decode(data)

    im = PIL.Image.open(io.BytesIO(data))

    return im


# Apply monkey patches
Image.to_bytes = _image_to_bytes
Image.crop_square = _image_crop_square
Image.from_image_file = classmethod(_image_from_image_file)
Image.from_bytestr = classmethod(_image_from_bytestr)


def are_same_image(image1, image2):
    try:
        img_chop = PIL.ImageChops.difference(image1, image2)

        print(np.sum(np.array(img_chop.getdata())))

        if np.sum(np.array(img_chop.getdata())) == 0:
            return True
        return False

    except ValueError as e:
        print(e)
        return False