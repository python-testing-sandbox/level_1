import pytest
from PIL import Image


class FakeClass:
    pass


def get_size():
    return 50


@pytest.fixture
def test_image_factory():
    def create_test_image(a):
        image = Image.new('RGBA', size=(get_size(), get_size()), color=(155, 0, 0))
        return image

    return create_test_image
