from typing import Self, override

import pytest
from pendulum import Date

from quant_py.daycounter import Daycounter


class MockDaycounter(Daycounter):
    @override
    def count(self: Self, start: Date, end: Date) -> float:
        return -1004.0


@pytest.mark.unit
def test_call_magic_method() -> None:
    dc = MockDaycounter()
    start = Date(2025, 1, 1)
    end = Date(2025, 12, 31)
    assert dc(start, end) == -1004.0
