from code import is_python_class_name

import pytest


@pytest.mark.parametrize(
    "name, result",
    [
        ("Classname", True),
        ("notclassname", False),
        ("NotClassName", False),

    ],
)
def test_is_python_class_name(name, result):
    assert is_python_class_name(name) == result
