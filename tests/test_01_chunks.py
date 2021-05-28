from code import chunks

import pytest


@pytest.mark.parametrize(
    "some_list, chunk_size, chunk_result, exception",
    [
        ([1, 2, 3], 3, [[1, 2, 3]], None),
        ([1, 2, 3], 2, [[1, 2], [3]], None),
        ([], 2, [], None),
        ([1, 2, 3], 0, [], ValueError),
    ],
)
def test_chunks(some_list, chunk_size, chunk_result, exception):
    if not exception:
        assert list(chunks(some_list, chunk_size)) == chunk_result
    else:
        with pytest.raises(exception):
            assert list(chunks(some_list, chunk_size)) == chunk_result
