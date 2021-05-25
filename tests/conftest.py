import pytest
from PIL import Image


SIZE_IMAGE = 100


class MyTestClass:
    pass


@pytest.fixture()
def create_image():
    image = Image.new('RGBA', size=(SIZE_IMAGE, SIZE_IMAGE))
    return image
