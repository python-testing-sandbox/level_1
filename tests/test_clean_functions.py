import ast
import datetime
import pytest
from contextlib import nullcontext as does_not_raise

from code import (
    chunks, flat, is_python_class_name, max_with_default, is_path_in_exclude_list, split_camel_case_words,
    is_camel_case_word, if_logs_has_any_of_commands, has_recursive_calls, extract_all_constants_from_ast,
    parse_iso_datetime, get_image_height_in_pixels, get_full_class_name)
from tests.conftest import MockObject


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
        ([[1, 2, {}], ['a', 'b', {}]], [1, 2, {}, 'a', 'b', {}]),
        ([], []),
        ([[], []], []),
    ],
)
def test_flat(some_list, expected):
    assert flat(some_list) == expected


@pytest.mark.parametrize(
    'name, expected, expectation',
    [
        ('Classname', True, does_not_raise()),
        ('ClassName', False, does_not_raise()),
        ('classname', False, does_not_raise()),
        ('className', False, does_not_raise()),
        ('', None, pytest.raises(IndexError)),
    ],
)
def test_is_python_class_name(name, expected, expectation):
    with expectation:
        assert is_python_class_name(name) == expected


@pytest.mark.parametrize(
    'items, default, expected',
    [
        ([[1, 2], [3, 4], [5]], None, [5]),
        ([[1, 2], [3, 4], [5]], 1, [5]),
        ([3, 4, 5], 1, 5),
        ('', 1, 1),
        ('', None, 0),
    ],
)
def test_max_with_default(items, default, expected):
    assert max_with_default(items, default) == expected


def test_max_with_default_with_exception():
    with pytest.raises(TypeError):
        assert max_with_default([[1, 2], '3, 4', (5, 'b')], 1) is None


@pytest.mark.parametrize(
    'path, exclude, expected',
    [
        ('abc def', ['a', 'b', 'c', 'z'], True),
        ('abc def', ['z'], False),
        ('', [], False),
    ],
)
def test_is_path_in_exclude_list(path, exclude, expected):
    assert is_path_in_exclude_list(path, exclude) == expected


@pytest.mark.parametrize(
    'camel_cased_word, expected, expectation',
    [
        ('camelCasedWord', ['camel', 'cased', 'word'], does_not_raise()),
        ('CamelCasedWord', ['camel', 'cased', 'word'], does_not_raise()),
        ('CamelCasedWorD', ['camel', 'cased', 'wor', 'd'], does_not_raise()),
        ('', None, pytest.raises(IndexError)),
        ('camelcaseword', None, pytest.raises(IndexError)),
    ],
)
def test_split_camel_case_words(camel_cased_word, expected, expectation):
    with expectation:
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
        ('def func():\n return None', False),
        ('def func():\n return func()', True),
    ],
)
def test_has_recursive_calls(funcdef, expected):
    assert has_recursive_calls(ast.parse(funcdef).body[0]) == expected


@pytest.mark.parametrize(
    'ast_tree, expected',
    [
        ('a = "string"', ['string']),
        ('def func():\n return 5', []),
    ],
)
def test_extract_all_constants_from_ast(ast_tree, expected):
    assert extract_all_constants_from_ast(ast.parse(ast_tree).body[0]) == expected


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
        ('http://test.com', 10),
    ],
)
def test_get_image_height_in_pixels(requests_mock, mocker, url, expected, fixture_create_image):
    requests_mock.get(url, content=b'abcdef')
    mocker.patch(
        'PIL.Image.open',
        return_value=fixture_create_image,
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
