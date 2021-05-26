import io
from code import get_image_height_in_pixels

import pytest
from PIL import Image


def create_image(height: int):
    image = Image.new("RGB", (75, height), color="red")
    image_byteio = io.BytesIO()
    image.save(image_byteio, "PNG")
    image_byteio.seek(0)
    image_bytes = image_byteio.read()
    return image_bytes


@pytest.mark.parametrize(
    "url, height,result",
    [
        ("http://test.com/image", 60, 60),
        ("http://test.com/image", 70, 70),
        ("no_content", 70, None),
    ],
)
def test_get_image_height_in_pixels(requests_mock, url, height, result):
    requests_mock.get(url, content=create_image(height))
    assert get_image_height_in_pixels(url) == result
