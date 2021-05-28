from code import get_full_class_name

import pytest


class ClassForTest(object):
    def __init__(self):
        pass


class_for_test = ClassForTest()


@pytest.mark.parametrize(
    "obj, result",
    [
        (str, "type"),
        (ClassForTest, "type"),
        (class_for_test, "test_11_get_full_class_name.ClassForTest"),
    ],
)
def test_get_full_class_name(obj, result):
    assert get_full_class_name(obj) == result
