import pytest
import ast
import datetime

from code import (flat, is_python_class_name, parse_iso_datetime, chunks,
                  is_camel_case_word, if_logs_has_any_of_commands, is_path_in_exclude_list,
                  get_full_class_name, max_with_default, split_camel_case_words, extract_all_constants_from_ast,
                  has_recursive_calls, get_image_height_in_pixels)
from .conftest import MyTestClass


@pytest.mark.parametrize(
    'some_list, expected',
    [
        ([['People'], ['Name', 'Job']], ['People', 'Name', 'Job']),
        ([[], [1, 'a']], [1, 'a']),
    ],
)
def test_flat(some_list, expected):
    assert flat(some_list) == expected


@pytest.mark.parametrize(
    'some_name, expected',
    [
        ('User', True),
        ('name', False),
        ('userName', False)
    ],
)
def test_is_python_class_name(some_name, expected):
    assert is_python_class_name(some_name) == expected


@pytest.mark.parametrize(
    'iso_datetime, expected',
    [
        ('2008-09-03T20:56:35.450686Z', datetime.datetime(2008, 9, 3, 20, 56, 35, 450686)),
        ('name', None),
        ('2018-11-11', datetime.datetime(2018, 11, 11, 0, 0)),
        ('2010-09-03T20:56:35.45', None),
    ],
)
def test_parse_iso_datetime(iso_datetime, expected):
    assert parse_iso_datetime(iso_datetime) == expected


@pytest.mark.parametrize(
    'some_list, chunk_size, expected',
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 4, [[1, 2, 3, 4], [5, 6, 7, 8], [9]]),
        ([1, 2, 3, 4, 5], 3, [[1, 2, 3], [4, 5]]),
        ([], 3, []),
    ]

)
def test_chunks(some_list, chunk_size, expected):
    assert list(chunks(some_list, chunk_size)) == expected


@pytest.mark.parametrize(
    'log, some_commands, expected',
    [
        (['update photo', 'delete'], ['update', 'read', 'exit'], True),
        (['user post new recipes', 'user read url'], ['update', 'read', 'exit'], True),
        (['delete', 'send'], ['update'], False),
        ([], ['read'], False),
    ],
)
def test_if_logs_has_any_of_commands(log, some_commands, expected):
    assert if_logs_has_any_of_commands(log, some_commands) == expected


@pytest.mark.parametrize(
    'some_word, expected',
    [
        ('CamelCaps', True),
        ('camelcaps', False),
        ('CamelHumpedWord', True),
        ('Ca', False),
        ('cA', True),
        ('', False),
    ],
)
def test_is_camel_case_word(some_word, expected):
    assert is_camel_case_word(some_word) == expected


@pytest.mark.parametrize(
    'some_path, exclude, expected',
    [
        ('some_path', ['some', 'path'], True),
        ('some path', ['path'], True),
        ('some path', [''], True),
        ('some path', [], False),
        ('', [], False),
        ('', [''], True),
    ]
)
def test_is_path_in_exclude_list(some_path, exclude, expected):
    assert is_path_in_exclude_list(some_path, exclude) == expected


@pytest.mark.parametrize(
    'some_obj, expected',
    [
        (4.3, 'float'),
        ('text', 'str'),
        ([2], 'list'),
        (MyTestClass(), 'tests.conftest.MyTestClass'),
    ]
)
def test_get_full_class_name(some_obj, expected):
    assert get_full_class_name(some_obj) == expected


@pytest.mark.parametrize(
    'some_items, default, expected',
    [
        ([1, -2, 3], 1, 3),
        ('', None, 0),
        ([], 15, 15),
        ('AaBbCcXxYyZz', None, 'z'),
    ]
)
def test_max_with_default(some_items, default, expected):
    assert max_with_default(some_items, default) == expected


@pytest.mark.parametrize(
    'camel_cased_word, expected',
    [
        ('SomeCamelCasedWord', ['some', 'camel', 'cased', 'word']),
        (' CamelCasedWord', [' ', 'camel', 'cased', 'word']),
        ('CamelCasedsoMeWorD', ['camel', 'casedso', 'me', 'wor', 'd']),
    ]
)
def test_split_camel_case_words(camel_cased_word, expected):
    assert split_camel_case_words(camel_cased_word) == expected


@pytest.mark.parametrize(
    'ast_tree, expected',
    [
        ("fruits = ['mango', 'grapes']", {'mango', 'grapes'}),
        ("a = 'Bob'", {'Bob'}),
    ]

)
def test_extract_all_constants_from_ast(ast_tree, expected):
    assert {*extract_all_constants_from_ast(ast.parse(ast_tree))} == expected


@pytest.mark.parametrize(
    'some_funcdef, expected',
    [
        ('def func(n):\n\treturn func(n/2)', True),
        ('def func(n):\n\treturn n/2', False),
    ]
)
def test_has_recursive_calls(some_funcdef, expected):
    assert has_recursive_calls(ast.parse(some_funcdef).body[0]) == expected


@pytest.mark.parametrize(
    'some_url, expected',
    [
        ('url', None),
        ('http://climbhub.com/', 100),
    ],
)
def test_get_image_height_in_pixels(some_url, expected, create_image, requests_mock, mocker):
    requests_mock.get(some_url, content=b"request")
    mocker.patch('PIL.Image.open', return_value=create_image)
    assert get_image_height_in_pixels(some_url) == expected
