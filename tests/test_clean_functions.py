import ast
import datetime
import pytest

from code import (
    chunks, flat, is_python_class_name, max_with_default, is_path_in_exclude_list, split_camel_case_words,
    is_camel_case_word, if_logs_has_any_of_commands, has_recursive_calls, extract_all_constants_from_ast,
    parse_iso_datetime, get_image_height_in_pixels, get_full_class_name)
from tests.conftest import MockImage, MockObject


@pytest.mark.parametrize(
    'some_list, chunk_size, expected',
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        (['a', 'b', 'c', 'd'], 3, [['a', 'b', 'c'], ['d']]),
        ([], 1, []),
    ],
)
def test_chunks(some_list, chunk_size, expected):
    generator = chunks(some_list, chunk_size)
    assert list(generator) == expected


@pytest.mark.parametrize(
    'some_list, expected',
    [
        ([[1, 2], [3, 4], [5]], [1, 2, 3, 4, 5]),
        ([['a', 'b', 'c'], ['d']], ['a', 'b', 'c', 'd']),
        ([], []),
    ],
)
def test_flat(some_list, expected):
    assert flat(some_list) == expected


@pytest.mark.parametrize(
    'name, expected',
    [
        ('Classname', True),
        ('ClassName', False),
    ],
)
def test_is_python_class_name(name, expected):
    assert is_python_class_name(name) == expected


def test_is_python_class_name_with_exception():
    with pytest.raises(IndexError):
        assert is_python_class_name('')


@pytest.mark.parametrize(
    'items, default, expected',
    [
        ([[1, 2], [3, 4], [5]], None, [5]),
        ([[1, 2], [3, 4], [5]], 1, [5]),
        ('', 1, 1),
        ('', None, 0)
    ],
)
def test_max_with_default(items, default, expected):
    assert max_with_default(items, default) == expected


@pytest.mark.parametrize(
    'path, exclude, expected',
    [
        ('abc def', ['a', 'b', 'c', 'z'], True),
        ('abc def', ['z'], False),
        ('', [], False)
    ],
)
def test_is_path_in_exclude_list(path, exclude, expected):
    assert is_path_in_exclude_list(path, exclude) == expected


@pytest.mark.parametrize(
    'camel_cased_word, expected',
    [
        ('camelCasedWord', ['camel', 'cased', 'word']),
        ('CamelCasedWord', ['camel', 'cased', 'word']),
        ('CamelCasedWorD', ['camel', 'cased', 'wor', 'd']),
    ],
)
def test_split_camel_case_words(camel_cased_word, expected):
    assert split_camel_case_words(camel_cased_word) == expected


@pytest.mark.parametrize(
    'uppercase_letters_amount, expected',
    [
        ('camelCasedWord', True),
        ('camelCased', True),
        ('camelcasedword', False),
        ('', False),
    ],
)
def test_is_camel_case_word(uppercase_letters_amount, expected):
    assert is_camel_case_word(uppercase_letters_amount) == expected


@pytest.mark.parametrize(
    'log, commands, expected',
    [
        (['request to api', 'response from api'], ['request', 'exit'], True),
        (['first request to api', 'first response from api'], ['request', 'exit'], True),
        (['request', 'response'], ['request', 'exit'], True),
        (['request', 'response'], ['exit'], False),
        ([], ['exit'], False),
    ],
)
def test_if_logs_has_any_of_commands(log, commands, expected):
    assert if_logs_has_any_of_commands(log, commands) == expected


@pytest.mark.parametrize(
    'funcdef, expected',
    [
        (ast.parse('''def func():\n return None''').body[0], False),
        (ast.parse('''def func():\n return func()''').body[0], True),
    ],
)
def test_has_recursive_calls(funcdef, expected):
    assert has_recursive_calls(funcdef) == expected


@pytest.mark.parametrize(
    'ast_tree, expected',
    [
        (ast.Str('string'), ['string']),
        (ast.FunctionDef, []),
    ],
)
def test_extract_all_constants_from_ast(ast_tree, expected):
    assert extract_all_constants_from_ast(ast_tree) == expected


@pytest.mark.parametrize(
    'iso_datetime, expected',
    [
        ('2019-12-04Z', datetime.datetime(2019, 12, 4, 0, 0)),
        ('2019-12-04', datetime.datetime(2019, 12, 4, 0, 0)),
        ('2019-12-04W', None),
    ],
)
def test_parse_iso_datetime(iso_datetime, expected):
    assert parse_iso_datetime(iso_datetime) == expected


@pytest.mark.parametrize(
    'url, expected',
    [
        ('url', None),
        ('http://test.com', 'M'),
    ],
)
def test_get_image_height_in_pixels(requests_mock, mocker, url, expected):
    requests_mock.get('http://test.com', content=b"abcdef")
    mocker.patch(
        'PIL.Image.open',
        return_value=MockImage(),
    )
    assert get_image_height_in_pixels(url) == expected


@pytest.mark.parametrize(
    'obj, expected',
    [
        (MockObject(), 'tests.conftest.MockObject'),
        ([], 'list'),
    ],
)
def test_get_full_class_name(obj, expected):
    assert get_full_class_name(obj) == expected
