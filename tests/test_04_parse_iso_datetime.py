import datetime
from code import parse_iso_datetime

import pytest


@pytest.mark.parametrize(
    "iso_datetime, result",
    [
        ("2020-10-22T14:29:38", datetime.datetime(2020, 10, 22, 14, 29, 38)),
        ("2019-09-21T13:18:27Z", datetime.datetime(2019, 9, 21, 13, 18, 27)),
        ("2019.09.21 13:18:27", None),
        ("string", None),
    ],
)
def test_parse_iso_datetime(iso_datetime, result):
    assert parse_iso_datetime(iso_datetime) == result
