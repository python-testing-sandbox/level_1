import datetime
import pytest
import ast

from code import (chunks, flat, has_recursive_calls, parse_iso_datetime, get_image_height_in_pixels,
                  if_logs_has_any_of_commands, extract_all_constants_from_ast, is_camel_case_word,
                  split_camel_case_words, is_path_in_exclude_list, get_full_class_name, max_with_default,
                  is_python_class_name)
from conftest import SomeClass


@pytest.mark.parametrize(
    'somelist, chunk_size, expected',
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([], 3, []),
        (['a', 'b'], 3, [['a', 'b']]),
    ]
)
def test_chunk_iteration(somelist, chunk_size, expected):
    some_chunks = chunks(somelist, chunk_size)
    assert list(some_chunks) == expected


@pytest.mark.parametrize(
    'some_list, expected',
    [
        ([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'j']], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j']),
        ([], []),
        ([{1: 'a', 2: 'b'}, {3: 'q', 4: 'w'}], [1, 2, 3, 4]),
    ]
)
def test_flat(some_list, expected):
    assert flat(some_list) == expected


@pytest.mark.parametrize(
    'expression, expected',
    [
        ('5/3+8', False),
        ('def foo(): return foo()', True),

    ]
)
def test_has_recursive_calls(expression, expected):
    funcdef = ast.parse(expression).body[0]
    assert has_recursive_calls(funcdef) == expected


@pytest.mark.parametrize(
    'some_datetime, expected',
    [
        ('2021-05-24T10:34:25.518993Z', datetime.datetime(2021, 5, 24, 10, 34, 25, 518993)),
        ('2021.05.28', None),
        ('', None),
        ('2021-05-24T10:34:25.518993', datetime.datetime(2021, 5, 24, 10, 34, 25, 518993)),

    ]
)
def test_parse_iso_datetime(some_datetime, expected):
    assert parse_iso_datetime(some_datetime) == expected


@pytest.mark.parametrize(
    'log, commands, expected',
    [
        (['move forward'], ['move'], True),
        (['variable set on'], ['set'], True),
        (['put'], ['put'], True),
        (['some text'], ['erase'], False),
    ]
)
def test_if_logs_has_any_of_commands(log, commands, expected):
    assert if_logs_has_any_of_commands(log, commands) == expected


@pytest.mark.parametrize(
    'expression, expected',
    [
        ('def foo(): return foo()', []),
        ('def foo(): return "text"', ['text']),
    ]
)
def test_extract_all_constants_from_ast(expression, expected):
    tree = ast.parse(expression).body[0]
    assert extract_all_constants_from_ast(tree) == expected


@pytest.mark.parametrize(
    'some_word, expected',
    [
        ('SuperClass', True),
        ('nonameclass', False),
        ('email_address', False),
        ('EmailVerification', True),
        ('oldEmail', True),
    ]
)
def test_is_camel_case_word(some_word, expected):
    assert is_camel_case_word(some_word) == expected


@pytest.mark.parametrize(
    'camel_cased_word, expected',
    [
        ('SuperMegaClass', ['super', 'mega', 'class']),
        ('userName', ['user', 'name']),
        ('Sometext', ['sometext']),
    ]
)
def test_split_camel_case_words(camel_cased_word, expected):
    assert split_camel_case_words(camel_cased_word) == expected


@pytest.mark.parametrize(
    'path, exclude, expected',
    [
        ('user/project/template', ['project', 'projects'], True),
        ('lib/bin/', ['project', 'projects'], False),
        ('C:\\User\\Documents', ['User'], True),
        ('D:\\Game\\Civilization', ['Program', 'User'], False),
    ]
)
def test_is_path_in_exclude_list(path, exclude, expected):
    assert is_path_in_exclude_list(path, exclude) == expected


@pytest.mark.parametrize(
    'items, default, expected',
    [
        ([], 1, 1),
        ([1, 2], None, 2),
    ]
)
def test_max_with_default(items, default, expected):
    assert max_with_default(items, default) == expected


@pytest.mark.parametrize(
    'classname, expected',
    [
        ('List', True),
        ('car', False),
    ]
)
def test_is_python_class_name(classname, expected):
    assert is_python_class_name(classname) == expected


@pytest.mark.parametrize(
    'image_url, expected',
    [
        ('some.url', None),
        ('https://fake.url', 100),
    ]
)
def test_get_image_height_in_pixels(requests_mock, mocker, get_fixture_image_object, image_url, expected):
    requests_mock.get(image_url, content=b'fakeurl')
    mocker.patch('PIL.Image.open', return_value=get_fixture_image_object)
    assert get_image_height_in_pixels(image_url) == expected


@pytest.mark.parametrize(
    'obj, expected',
    [
        ('Hello World', 'str'),
        (SomeClass(), 'conftest.SomeClass')
    ]
)
def test_get_full_class_name(obj, expected):
    assert get_full_class_name(obj) == expected
