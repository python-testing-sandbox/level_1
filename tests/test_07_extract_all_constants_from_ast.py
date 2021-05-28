from code import extract_all_constants_from_ast

import pytest

from tests.test_files.read_test_file import read_test_file


@pytest.mark.parametrize(
    "ast_tree, result",
    [
        (
            read_test_file("constans.py"),
            ["Hello", "World"],
        ),
    ],
)
def test_extract_all_constants_from_ast(ast_tree, result):
    assert set(extract_all_constants_from_ast(ast_tree)) == set(result)
