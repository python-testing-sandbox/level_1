from code import split_camel_case_words

import pytest


@pytest.mark.parametrize(
    "camel_cased_word, result, exception",
    [
        ("CamelCase", ["camel", "case"], None),
        ("Camel_Case", ["camel_", "case"], None),
        ("Camel Case", ["camel ", "case"], None),
        ("nocamelcase", [], IndexError),
        ("no camel case", [], IndexError),
        ("cAmelCase", ["c", "amel", "case"], None),
    ],
)
def test_split_camel_case_words(camel_cased_word, result, exception):
    if not exception:
        assert split_camel_case_words(camel_cased_word) == result
    else:
        with pytest.raises(exception):
            assert split_camel_case_words(camel_cased_word) == result
