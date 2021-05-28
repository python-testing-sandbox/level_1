from code import max_with_default

import pytest


@pytest.mark.parametrize(
    "items, default, result",
    [([1, 2, 3], 4, 3), ([], 5, 5), ([1, 2, 3], None, 3)],
)
def test_max_with_default(items, default, result):
    assert max_with_default(items, default) == result
