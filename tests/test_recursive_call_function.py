import ast
import pytest

from code import has_recursive_calls


@pytest.mark.parametrize(
    "funcdef, result",
    [
        (ast.parse("def recursive(a): \n return recursive(a)").body[0], True),
        (ast.parse("def not_recursive(a): \n return a").body[0], False),
    ],
)
def test_recursive_calls(funcdef, result):
    print(funcdef.body[0])
    assert has_recursive_calls(funcdef) == result
