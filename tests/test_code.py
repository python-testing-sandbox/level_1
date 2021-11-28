import io

import pytest
from PIL import Image

import code

from fake_class import Money


@pytest.mark.parametrize('class_name,expected', [
    ('class_name', False),
    ('ClassName', False),
    ('Classname', True)
])
def test_is_python_class_name(class_name, expected):
    assert code.is_python_class_name(class_name) == expected


@pytest.mark.parametrize('items,default,expected', [
    (range(0, 9), None, 8),
    ([], None, 0),
    ([], 3, 3),
    (range(100, 102), 192, 101)
])
def test_max_with_default(items, default, expected):
    assert code.max_with_default(items, default=default) == expected


@pytest.mark.parametrize('obj,class_name', [
    (3, 'int'),
    (object, 'type'),
    (None, 'NoneType'),
    (Money(5), 'fake_class.Money'),
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
    ('', False)
])
def test_split_camel_case_words_without_capital_letters(word, expected):
    assert code.is_camel_case_word(word) == expected


@pytest.mark.parametrize('log,commands', [
    (['log_entity1'], []),
    ([], ['CMD1']),
    ([], [])
])
def test_if_logs_has_any_of_commands_with_epmty_lists(log, commands):
    assert not code.if_logs_has_any_of_commands(log, commands)


def get_image():
    img = Image.new('RGB', (100, 100), color='white')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.read()
