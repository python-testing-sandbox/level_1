import pytest
from PIL import Image


@pytest.fixture
def get_fixture_image_object():
    im = Image.new('1', (100, 100))
    return im


class SomeClass:
    pass
