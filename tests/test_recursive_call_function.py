from code import has_recursive_calls

import pytest
from read_test_file import read_test_file


@pytest.mark.parametrize(
    "funcdef, result",
    [
        (read_test_file("has_recursive.py").body[0], True),
        (read_test_file("no_recursive.py").body[0], False),
    ],
)
def test_recursive_calls(funcdef, result):
    assert has_recursive_calls(funcdef) == result
