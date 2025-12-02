import pytest
from pendulum.date import Date
from pendulum.duration import Duration

from quant_py.scheduling.roll_convention import Bom, DayOfMonth, Eom


@pytest.mark.unit
def test_roll_conv_adjust() -> None:
    dt = Date(2025, 11, 20)
    roll_day = DayOfMonth(15)
    rslt = roll_day.adjust(dt)
    assert rslt == Date(2025, 11, 15)


@pytest.mark.unit
def test_roll_conv_adjust_overflow() -> None:
    dt = Date(2025, 11, 28)
    roll_day = DayOfMonth(31)
    rslt = roll_day.adjust(dt)
    assert rslt == Date(2025, 11, 30)


@pytest.mark.unit
def test_roll_conv_adjust_eom() -> None:
    dt = Date(2025, 11, 15)
    roll_day = Eom()
    rslt = roll_day.adjust(dt)
    assert rslt == Date(2025, 11, 30)


@pytest.mark.unit
def test_roll_conv_adjust_bom() -> None:
    dt = Date(2025, 11, 15)
    roll_day = Bom()
    rslt = roll_day.adjust(dt)
    assert rslt == Date(2025, 11, 1)


@pytest.mark.unit
def test_roll_conv_next() -> None:
    dt = Date(2023, 8, 31)
    tenor = Duration(months=6)
    roll_conv = DayOfMonth(dt.day)
    rslt = roll_conv.next(dt, tenor)
    assert rslt == Date(2024, 2, 29)


@pytest.mark.unit
def test_roll_conv_prev() -> None:
    dt = Date(2023, 8, 31)
    tenor = Duration(months=6)
    roll_conv = DayOfMonth(dt.day)
    rslt = roll_conv.previous(dt, tenor)
    assert rslt == Date(2023, 2, 28)


@pytest.mark.unit
def test_day_of_month_eq_bad() -> None:
    rc1 = DayOfMonth(1)
    rc2 = Eom()
    assert rc1 != rc2
