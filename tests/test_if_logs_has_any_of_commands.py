import pytest

from code import if_logs_has_any_of_commands


@pytest.mark.parametrize(
    "log, command, result",
    [
        (["make log with commands" ], ["make"], True),
        (["Log without commands", "pytest Log with commands" ], ["make", "pytest"], True),
        (["Log without commands" ], ["make"], False),
    ],
)
def test_if_logs_has_any_of_commands(log, command, result):
    assert if_logs_has_any_of_commands(log, command) == result