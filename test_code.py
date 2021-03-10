from contextlib import nullcontext as does_not_raise
import datetime

import pytest
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
    'args, expected, expectation',
    [
        (([], None), 0, does_not_raise()),
        (([],), 0, does_not_raise()),
        (([], 5), 5, does_not_raise()),
        (([-1], None), -1, does_not_raise()),
        (([1, 3, -1, 100], 5), 100, does_not_raise()),
        (((1, 3, -1, 101), 5), 101, does_not_raise()),
        (((1, 3, -1, 101),), 101, does_not_raise()),
        (((1, 3, -1, '101'),), None, pytest.raises(TypeError)),
    ]
)
def test_max_with_default(args, expected, expectation):
    with expectation:
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
    'some_list, chunk_size, expected, expectation',
    [
        ([1, 2, 3, 4, 5], 2, ([1, 2], [3, 4], [5]), pytest.raises(StopIteration)),
        ([], 2, (), pytest.raises(StopIteration)),
    ]
)
def test_chunks(some_list, chunk_size, expected, expectation):
    gen = code.chunks(some_list, chunk_size)
    expected_iterator = iter(expected)

    with expectation:
        assert next(gen) == next(expected_iterator)
        assert next(gen) == next(expected_iterator)
        assert next(gen) == next(expected_iterator)
        assert next(gen) == next(expected_iterator)


@pytest.mark.parametrize(
    'camel_cased_word, expected, expectation',
    [
        ('small', [], pytest.raises(IndexError)),
        ('BigGood', ['big', 'good'], does_not_raise()),
        ('Big', ['big'], does_not_raise()),
        ('bIg', ['b', 'ig'], does_not_raise()),
        ('', [], pytest.raises(IndexError)),
    ]
)
def test_split_camel_case_words(camel_cased_word, expected, expectation):
    with expectation:
        assert code.split_camel_case_words(camel_cased_word) == expected


@pytest.mark.parametrize(
    'url, expected',
    [
        ('https://yandex.ru/', get_size()),
        ('yandex.ru/', None),
    ]
)
def test_get_image_height_in_pixels(url, expected, monkeypatch, test_image_factory):
    monkeypatch.setattr(Image, 'open', test_image_factory)
    assert code.get_image_height_in_pixels(url) == expected


# @pytest.mark.parametrize(
#     'funcdef, expected',
#     [
#         (fake_func, False),
#         (datetime, True),
#     ]
# )
# def test_has_recursive_calls():
#     assert code.has_recursive_calls(ast.parse(''))


# def test_extract_all_constants_from_ast():
#     assert code.extract_all_constants_from_ast(ast.parse('fake_func')) == 1
