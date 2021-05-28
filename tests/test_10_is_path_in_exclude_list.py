from code import is_path_in_exclude_list

import pytest


@pytest.mark.parametrize(
    "path, exclude, result",
    [
        (
            "/first", 
            ["/first", "/second", "/third"], 
            True
        ),
        (
            "/second/something1",
            ["/first", "/second/something1", "/third/something1/something2"],
            True,
        ),
        (
            "/fourth",
            ["/first", "/second/something1", "/third/something1/something2"],
            False,
        ),
        (
            "/third", 
            ["/first", "/second", "/third/something1/something2"], 
            False,
        ),
    ],
)
def test_is_path_in_exclude_list(path, exclude, result):
    assert is_path_in_exclude_list(path, exclude) == result
