from code import flat

import pytest


@pytest.mark.parametrize(
    "some_list, list_result, exception",
    [
        ([[1, 'a'], [3]], [1, 'a', 3], None),
        ([[1, {2}], [3,[4]]], [1, {2}, 3,[4]], None),
        ([1, 2, 3], [], TypeError),
    ],
)
def test_flat(some_list, list_result, exception):
    if not exception:
        assert flat(some_list) == list_result
    else:
        with pytest.raises(exception):
            assert flat(some_list) == list_result
