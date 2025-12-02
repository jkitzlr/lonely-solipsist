import numpy as np
import pytest
from pendulum.date import Date

from quant_py.scheduling.adjuster import Adjuster, BusdayConvention


@pytest.fixture
def calendar() -> np.busdaycalendar:
    holidays = np.array(
        [
            "2025-01-01",
            "2025-01-20",
            "2025-02-17",
            "2025-04-18",
            "2025-05-26",
            "2025-06-19",
            "2025-07-04",
            "2025-09-01",
            "2025-11-11",
            "2025-11-27",
            "2025-12-25",
        ],
        dtype="M8[D]",
    )
    return np.busdaycalendar(
        weekmask="1111100",
        holidays=holidays,
    )


@pytest.mark.parametrize(
    argnames=("dt", "busday_conv", "expected"),
    argvalues=[
        (Date(2025, 11, 27), BusdayConvention.FOLLOWING, Date(2025, 11, 28)),
        (Date(2025, 11, 27), BusdayConvention.PRECEDING, Date(2025, 11, 26)),
        (Date(2025, 11, 27), BusdayConvention.NONE, Date(2025, 11, 27)),
        (Date(2025, 11, 29), BusdayConvention.MODIFIEDFOLLOWING, Date(2025, 11, 28)),
        (Date(2025, 11, 1), BusdayConvention.MODIFIEDPRECEDING, Date(2025, 11, 3)),
        (Date(2025, 11, 1), BusdayConvention.PRECEDING, Date(2025, 10, 31)),
    ],
)
@pytest.mark.unit
def test_adjust(
    dt: Date,
    busday_conv: BusdayConvention,
    expected: Date,
    calendar: np.busdaycalendar,
) -> None:
    adjuster = Adjuster(calendar=calendar, busday_conv=busday_conv)
    rslt = adjuster.adjust(dt)
    assert rslt == expected
