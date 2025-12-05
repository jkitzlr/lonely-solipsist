import pytest
from pendulum.date import Date

from quant_py.daycounters.act360 import Act360


@pytest.mark.unit
def test_act360() -> None:
    dc = Act360()
    start = Date(2025, 1, 1)
    end = Date(2025, 6, 30)
    assert dc.count(start, end) == 180.0 / 360.0
