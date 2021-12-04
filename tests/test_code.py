import datetime

import pytest

import code
from tests.fake_class import Money


@pytest.mark.parametrize('class_name,expected', [
    ('class_name', False),
    ('ClassName', False),
    ('Classname', True),
])
def test_is_python_class_name(class_name, expected):
    assert code.is_python_class_name(class_name) == expected


@pytest.mark.parametrize('items,default,expected', [
    (range(0, 9), None, 8),
    ([], None, 0),
    ([], 3, 3),
    (range(100, 102), 192, 101),
])
def test_max_with_default(items, default, expected):
    assert code.max_with_default(items, default=default) == expected


@pytest.mark.parametrize('obj,class_name', [
    (3, 'int'),
    (object, 'type'),
    (None, 'NoneType'),
    (Money(5), 'tests.fake_class.Money'),
])
def test_get_full_class_name(obj, class_name):
    assert code.get_full_class_name(obj) == class_name


@pytest.mark.parametrize('camel_cased_word,words', [
    ('NotYetCamel', ['not', 'yet', 'camel']),
    ('realCamelCaseWords', ['real', 'camel', 'case', 'words']),
])
def test_split_camel_case_words(camel_cased_word, words):
    assert code.split_camel_case_words(camel_cased_word) == words


@pytest.mark.parametrize('word,expected', [
    ('not_camel_cased_word', False),
    ('camelCase', True),
    ('NotCamelCase', True),
    ('', False),
])
def test_split_camel_case_words_without_capital_letters(word, expected):
    assert code.is_camel_case_word(word) == expected


@pytest.mark.parametrize('log,commands', [
    (['log_entity1'], []),
    ([], ['CMD1']),
    ([], []),
    (['CMD12'], ['CMD1']),
])
def test_if_logs_has_any_of_commands_negative(log, commands):
    assert not code.if_logs_has_any_of_commands(log, commands)


@pytest.mark.parametrize('log,commands', [
    (['', 'CMD1'], ['CMD1']),
    (['Log1', 'CREATE_USER email pass'], ['CREATE_USER']),
    (['request DELETE /users/email', '2021-02-22T15:02:01 DELETE_USER {email: EMAIL}'], ['DELETE_USER']),
])
def test_if_logs_has_any_of_commands(log, commands):
    assert code.if_logs_has_any_of_commands(log, commands)


now = datetime.datetime.utcnow()


@pytest.mark.parametrize('iso_datetime_str,expected', [
    (now.isoformat(), now),
    (f'{now.isoformat()}Z', now),
    ('NotRealyISODate', None),
])
def test_parse_iso_datetime(iso_datetime_str, expected):
    assert code.parse_iso_datetime(iso_datetime_str) == expected


@pytest.mark.parametrize('iterable,chunk_size', [
    (list(range(0, 9)), 2),
])
def test_chunks(iterable, chunk_size):
    source = []
    [source.extend(chunk) for chunk in list(code.chunks(iterable, chunk_size))]
    assert source == iterable


@pytest.mark.parametrize('nested,flatted', [
    ([[12, 2, 3], [4]], [12, 2, 3, 4]),
    ([[]], []),
])
def test_flat(nested, flatted):
    assert code.flat(nested) == flatted


@pytest.mark.parametrize('path,exclude', [
    ('/fword/some/path', ['not', 'fword']),
])
def test_is_path_in_exclude_list(path, exclude):
    assert code.is_path_in_exclude_list(path, exclude)


@pytest.mark.parametrize('url,expected', [
    ('//notrealurl.com/img.jpg', None),
    ('asdfjads', None),
    ('https://docs.pytest.org/en/6.2.x/_static/pytest1.png', 143),
])
def test_get_image_height_in_pixels(url, expected):
    assert code.get_image_height_in_pixels(url) == expected
