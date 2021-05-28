from code import is_camel_case_word

import pytest


@pytest.mark.parametrize(
    "word, result",
    [
        ("CamelCase", True),
        ("Camel_Case", True),
        ("Camel Case", True),
        ("nocamelcase", False),
        ("no camel case", False),
    ],
)
def test_is_camel_case_word(word, result):
    assert is_camel_case_word(word) == result
