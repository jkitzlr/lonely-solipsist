from typing import TYPE_CHECKING

import pytest
from pendulum.date import Date
from pendulum.duration import Duration

from quant_py.daycounter.act360 import Act360
from quant_py.scheduling.period import Period
from quant_py.scheduling.roll_convention import DayOfMonth

if TYPE_CHECKING:
    from quant_py.daycounter._base import Daycounter


@pytest.fixture
def regular_period() -> Period:
    return Period(
        start=Date(2025, 2, 17),
        end=Date(2025, 8, 15),
        unadj_start=Date(2025, 2, 15),
        unadj_end=Date(2025, 8, 15),
    )


@pytest.fixture
def long_period() -> Period:
    return Period(
        start=Date(2024, 12, 2),
        end=Date(2025, 8, 15),
        unadj_start=Date(2024, 12, 1),
        unadj_end=Date(2025, 8, 15),
    )


@pytest.mark.unit
def test_length_in_days(regular_period: Period) -> None:
    assert regular_period.length_in_days == 179


@pytest.mark.unit
def test_len_magic_method(regular_period: Period) -> None:
    assert len(regular_period) == 179


@pytest.mark.parametrize(
    argnames=("adjusted", "daycounter", "expected"),
    argvalues=[
        (True, Act360(), 179.0 / 360.0),
        (False, Act360(), 181.0 / 360.0),
    ],
)
@pytest.mark.unit
def test_year_frac(
    adjusted: bool,  # noqa: FBT001
    daycounter: Daycounter,
    expected: float,
    regular_period: Period,
) -> None:
    assert regular_period.calc_year_frac(daycounter, adjusted=adjusted) == expected


def test_is_regular_regular(regular_period: Period) -> None:
    roll_conv = DayOfMonth(15)
    tenor = Duration(months=6)
    assert regular_period.is_regular(roll_conv, tenor)


def test_is_regular_stub(long_period: Period) -> None:
    roll_conv = DayOfMonth(15)
    tenor = Duration(months=6)
    assert not long_period.is_regular(roll_conv, tenor)
