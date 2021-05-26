import pytest
import ast

from code import chunks, flat, has_recursive_calls, parse_iso_datetime, get_image_height_in_pixels
from code import if_logs_has_any_of_commands, extract_all_constants_from_ast, is_camel_case_word
from code import split_camel_case_words, is_path_in_exclude_list, get_full_class_name, max_with_default
from code import is_python_class_name


def test_chunk_iteration():
    some_list = [1, 2, 3, 4, 5]
    chunk_size = 1
    some_chunks = chunks(some_list, chunk_size)
    with pytest.raises(StopIteration):
        while True:
            next(some_chunks)


def test_flat():
    some_list = ['hello' 'world']
    some_flat = flat(some_list)
    assert type(some_flat) == list


def test_has_recursive_calls():
    expression = '5/3+8'
    funcdef = ast.parse(expression)
    calls = has_recursive_calls(funcdef)
    assert calls == False


def test_parse_iso_datetime():
    iso_datetime = '2021-05-24T10:34:25.518993Z'
    assert parse_iso_datetime(iso_datetime).year == 2021
    iso_datetime = '2021'
    assert parse_iso_datetime(iso_datetime) is None


@pytest.mark.parametrize(
    'image_url, expected',
    [
        ('some.url', None),
        ('https://via.placeholder.com/140x100', 100),
    ]
)
def test_get_image_height_in_pixels(image_url, expected):
    assert get_image_height_in_pixels(image_url) == expected


@pytest.mark.parametrize(
    'log, commands, expected',
    [
        (['move forward'], ['move'], True),
        (['variable set on'], ['set'], True),
        (['put'], ['put'], True)
    ]
)
def test_if_logs_has_any_of_commands(log, commands, expected):
    assert if_logs_has_any_of_commands(log, commands) == expected


def test_extract_all_constants_from_ast():
    expression = '5/3+8'
    ast_tree = ast.parse(expression)
    const = extract_all_constants_from_ast(ast_tree)
    assert type(const) == list


@pytest.mark.parametrize(
    'word, expected',
    [
        ('SuperClass', True),
        ('nonameclass', False)
    ]
)
def test_is_camel_case_word(word, expected):
    assert is_camel_case_word(word) == expected


@pytest.mark.parametrize(
    'camel_cased_word, expected',
    [
        ('SuperMegaClass', ['super', 'mega', 'class']),
        ('userName', ['user', 'name'])
    ]
)
def test_split_camel_case_words(camel_cased_word, expected):
    assert split_camel_case_words(camel_cased_word) == expected


@pytest.mark.parametrize(
    'path, exclude, expected',
    [
        ('user/project/template', ['project', 'projects'], True),
        ('lib/bin/', ['project', 'projects'], False)
    ]
)
def test_is_path_in_exclude_list(path, exclude, expected):
    assert is_path_in_exclude_list(path, exclude) == expected


def test_get_full_class_name():
    class SomeClass():
        pass

    x = SomeClass()
    y = 'Hello World'
    assert get_full_class_name(x) == 'test_code.SomeClass'
    assert get_full_class_name(y) == 'str'


@pytest.mark.parametrize(
    'items, default, expected',
    [
        ([], 1, 1),
        ([1, 2], None, 2),
    ]
)
def test_max_with_default(items, default, expected):
    assert max_with_default(items, default) == expected


def test_is_python_class_name():
    name = 'List'
    assert is_python_class_name(name) == True
