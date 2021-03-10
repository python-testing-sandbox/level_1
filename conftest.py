import pytest
from PIL import Image


class FakeClass:
    pass


def fake_func(a):
    return a + 5


a = '''
def recursive_fake_func(a):
    if a == 0:
        return

    return recursive_fake_func(a - 1)
'''


def get_size():
    return 50


@pytest.fixture
def test_image_factory():
    def create_test_image(a):
        image = Image.new('RGBA', size=(get_size(), get_size()), color=(155, 0, 0))
        return image

    return create_test_image
