from typing import TYPE_CHECKING

import pytest
from pendulum.date import Date
from pendulum.duration import Duration

from quant_py.scheduling.adjuster import BusdayConvention
from quant_py.scheduling.period import Period
from quant_py.scheduling.roll_convention import Bom, DayOfMonth, Eom, RollConventions
from quant_py.scheduling.schedule import Schedule

if TYPE_CHECKING:
    import numpy as np


@pytest.fixture
def schedule_semiannual_reg(sifma: np.busdaycalendar) -> Schedule:
    return Schedule.of(
        effective=Date(2025, 8, 15),
        termination=Date(2027, 8, 15),
        tenor=Duration(months=6),
        pay_cal=sifma,
        busday_conv=BusdayConvention.FOLLOWING,
    )


@pytest.fixture
def schedule_semiannual_long_front(sifma: np.busdaycalendar) -> Schedule:
    return Schedule.of(
        effective=Date(2025, 1, 10),
        front_stub=Date(2025, 8, 15),
        termination=Date(2027, 8, 15),
        tenor=Duration(months=6),
        pay_cal=sifma,
        busday_conv=BusdayConvention.FOLLOWING,
    )


@pytest.fixture
def schedule_semiannual_short_back(sifma: np.busdaycalendar) -> Schedule:
    return Schedule.of(
        effective=Date(2025, 8, 15),
        back_stub=Date(2027, 2, 15),
        termination=Date(2027, 7, 31),
        tenor=Duration(months=6),
        pay_cal=sifma,
        busday_conv=BusdayConvention.MODIFIEDFOLLOWING,
    )


@pytest.mark.unit
def test_periods(schedule_semiannual_reg: Schedule) -> None:
    periods = [
        Period(
            start=Date(2025, 8, 15),
            end=Date(2026, 2, 16),
            unadj_start=Date(2025, 8, 15),
            unadj_end=Date(2026, 2, 15),
        ),
        Period(
            start=Date(2026, 2, 16),
            end=Date(2026, 8, 17),
            unadj_start=Date(2026, 2, 15),
            unadj_end=Date(2026, 8, 15),
        ),
        Period(
            start=Date(2026, 8, 17),
            end=Date(2027, 2, 15),
            unadj_start=Date(2026, 8, 15),
            unadj_end=Date(2027, 2, 15),
        ),
        Period(
            start=Date(2027, 2, 15),
            end=Date(2027, 8, 16),
            unadj_start=Date(2027, 2, 15),
            unadj_end=Date(2027, 8, 15),
        ),
    ]
    assert schedule_semiannual_reg.periods == periods


@pytest.mark.unit
def test_periods_long_front(schedule_semiannual_long_front: Schedule) -> None:
    periods = [
        Period(
            start=Date(2025, 1, 10),
            end=Date(2025, 8, 15),
            unadj_start=Date(2025, 1, 10),
            unadj_end=Date(2025, 8, 15),
        ),
        Period(
            start=Date(2025, 8, 15),
            end=Date(2026, 2, 16),
            unadj_start=Date(2025, 8, 15),
            unadj_end=Date(2026, 2, 15),
        ),
        Period(
            start=Date(2026, 2, 16),
            end=Date(2026, 8, 17),
            unadj_start=Date(2026, 2, 15),
            unadj_end=Date(2026, 8, 15),
        ),
        Period(
            start=Date(2026, 8, 17),
            end=Date(2027, 2, 15),
            unadj_start=Date(2026, 8, 15),
            unadj_end=Date(2027, 2, 15),
        ),
        Period(
            start=Date(2027, 2, 15),
            end=Date(2027, 8, 16),
            unadj_start=Date(2027, 2, 15),
            unadj_end=Date(2027, 8, 15),
        ),
    ]
    assert schedule_semiannual_long_front.periods == periods


@pytest.mark.unit
def test_periods_short_back(schedule_semiannual_short_back: Schedule) -> None:
    periods = [
        Period(
            start=Date(2025, 8, 15),
            end=Date(2026, 2, 16),
            unadj_start=Date(2025, 8, 15),
            unadj_end=Date(2026, 2, 15),
        ),
        Period(
            start=Date(2026, 2, 16),
            end=Date(2026, 8, 17),
            unadj_start=Date(2026, 2, 15),
            unadj_end=Date(2026, 8, 15),
        ),
        Period(
            start=Date(2026, 8, 17),
            end=Date(2027, 2, 15),
            unadj_start=Date(2026, 8, 15),
            unadj_end=Date(2027, 2, 15),
        ),
        Period(
            start=Date(2027, 2, 15),
            end=Date(2027, 7, 30),
            unadj_start=Date(2027, 2, 15),
            unadj_end=Date(2027, 7, 31),
        ),
    ]
    assert schedule_semiannual_short_back.periods == periods


@pytest.mark.parametrize(
    argnames=("eom", "bom", "dt", "expected"),
    argvalues=[
        (True, False, Date(2025, 12, 15), Eom()),
        (False, True, Date(2025, 12, 15), Bom()),
        (False, False, Date(2025, 12, 15), DayOfMonth(15)),
    ],
)
def test_get_roll_conv(
    eom: bool,  # noqa: FBT001
    bom: bool,  # noqa: FBT001
    dt: Date,
    expected: RollConventions,
) -> None:
    assert Schedule._get_roll_conv(dt, eom=eom, bom=bom) == expected


@pytest.mark.unit
def test_get_roll_conv_bad_input() -> None:
    with pytest.raises(
        ValueError, match="Schedule cannot roll both beginning and end of month!"
    ):
        _ = Schedule._get_roll_conv(Date.today(), eom=True, bom=True)
