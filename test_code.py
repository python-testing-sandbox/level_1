import ast
import datetime

import pytest
import requests
from PIL import Image

import code
from conftest import FakeClass, get_size


@pytest.mark.parametrize(
    'name, expected',
    [('MyClass', False), ('Myclass', True), ('myclass', False), ('mYclass', False)]
)
def test_is_python_class_name(name, expected):
    assert code.is_python_class_name(name) == expected


@pytest.mark.parametrize(
    'args, expected',
    [
        (([], None), 0),
        (([],), 0),
        (([], 5), 5),
        (([-1], None), -1),
        (([1, 3, -1, 100], 5), 100),
        (((1, 3, -1, 101), 5), 101),
        (((1, 3, -1, 101),), 101),
    ]
)
def test_max_with_default(args, expected):
    assert code.max_with_default(*args) == expected


@pytest.mark.parametrize(
    'args, expected, ',
    [(((1, 3, -1, '101'),), None)]
)
def test_max_with_default_with_exception(args, expected):
    with pytest.raises(TypeError):
        assert code.max_with_default(*args) == expected


@pytest.mark.parametrize(
    'path, exclude, expected',
    [
        ('mypath', [], False),
        ('mypath', ['my', 'path'], True),
        ('mypath', ['mypath', 'anypath'], True),
        ('', [''], True),
        ('', [], False),
    ]
)
def test_is_path_in_exclude_list(path, exclude, expected):
    assert code.is_path_in_exclude_list(path, exclude) == expected


@pytest.mark.parametrize(
    'some_list, expected',
    [
        ([[1, 2, 3], [4, 5, 6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 'b', 3], [{}, 5, 6], ['a', 8, 9]], [1, 'b', 3, {}, 5, 6, 'a', 8, 9]),
        ([[], []], []),
        ([], []),
        ([[]], []),
    ]
)
def test_flat(some_list, expected):
    assert code.flat(some_list) == expected


@pytest.mark.parametrize(
    'iso_datetime, expected',
    [
        ('2018-05-25T12:16:14Z', datetime.datetime(2018, 5, 25, 12, 16, 14)),
        ('2018-02-25T18:16:15', datetime.datetime(2018, 2, 25, 18, 16, 15)),
        ('2018:02-25T18:16:15', None),
    ]
)
def test_parse_iso_datetime(iso_datetime, expected):
    assert code.parse_iso_datetime(iso_datetime) == expected


@pytest.mark.parametrize(
    'log, commands, expected',
    [
        ([], [], False),
        (['command'], ['command'], True),
        (['command'], ['pip'], False),
        (['pip command'], ['pip'], True),
        (['nice pip command'], ['pip'], True),
        (['command'], [], False),
        ([], ['command'], False),
    ]
)
def test_if_logs_has_any_of_commands(log, commands, expected):
    assert code.if_logs_has_any_of_commands(log, commands) == expected


@pytest.mark.parametrize(
    'word, expected',
    [
        ('small', False),
        ('Bs', False),
        ('BiG', True),
        ('cAmel', True),
        ('small', False),
        ('BIG', False),
        ('', False),
    ]
)
def test_is_camel_case_word(word, expected):
    assert code.is_camel_case_word(word) == expected


@pytest.mark.parametrize(
    'obj, expected',
    [
        ('sting', 'str'),
        (1, 'int'),
        ([2], 'list'),
        ((1, 2, 3), 'tuple'),
        (FakeClass(), 'conftest.FakeClass'),
    ]
)
def test_get_full_class_name(obj, expected):
    assert code.get_full_class_name(obj) == expected


@pytest.mark.parametrize(
    'some_list, chunk_size, expected',
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([], 2, []),
    ]
)
def test_chunks(some_list, chunk_size, expected):
    gen = code.chunks(some_list, chunk_size)

    assert list(gen) == expected


@pytest.mark.parametrize(
    'camel_cased_word, expected',
    [
        ('BigGood', ['big', 'good']),
        ('Big', ['big']),
        ('bIg', ['b', 'ig']),
    ]
)
def test_split_camel_case_words(camel_cased_word, expected):
    assert code.split_camel_case_words(camel_cased_word) == expected


@pytest.mark.parametrize(
    'camel_cased_word, expected, ',
    [('small', []), ('', [])]
)
def test_split_camel_case_words_with_exception(camel_cased_word, expected):
    with pytest.raises(IndexError):
        assert code.split_camel_case_words(camel_cased_word) == expected


@pytest.mark.parametrize(
    'url, expected',
    [
        ('https://yandex.ru/', get_size()),
        ('yandex.ru/', None),
    ]
)
def test_get_image_height_in_pixels(url, expected, monkeypatch, test_image_factory):
    monkeypatch.setattr(requests, 'get', b'some binary chars')
    monkeypatch.setattr(Image, 'open', test_image_factory)
    assert code.get_image_height_in_pixels(url) == expected


@pytest.mark.parametrize(
    'module, expected',
    [
        ('a = "literal"\nb = 5', {'literal'}),
        ('b = 5', set()),
        ('a = "literal"\nb = "new literal"', {'literal', 'new literal'}),
    ]
)
def test_extract_all_constants_from_ast(module, expected):
    assert {*code.extract_all_constants_from_ast(ast.parse(module))} == expected


@pytest.mark.parametrize(
    'module, expected',
    [
        ('def not_recursive(a, b, c):\n    return a + b + c', False),
        ('def recursive(a, b, c):\n    return recursive(a, b, c)', True),
    ]
)
def test_has_recursive_calls(module, expected):
    assert code.has_recursive_calls(ast.parse(module).body[0]) == expected
