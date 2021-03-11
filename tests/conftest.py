import pytest
from PIL import Image


@pytest.fixture()
def fixture_create_image():
    image = Image.new('RGBA', size=(10, 10))
    return image


class MockObject:
    def __init__(self):
        self.size = 'SML'
