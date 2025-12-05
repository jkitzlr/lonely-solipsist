import numpy as np
import pytest
from pendulum.date import Date

from quant_py.buscal import BusinessCalendar


@pytest.fixture
def buscal() -> BusinessCalendar:
    holidays = [
        "2025-01-01",
        "2025-01-20",
        "2025-02-17",
        "2025-04-18",
        "2025-05-26",
        "2025-06-19",
        "2025-07-04",
        "2025-09-01",
        "2025-10-13",
        "2025-11-11",
        "2025-11-27",
        "2025-12-25",
    ]
    return BusinessCalendar(
        holidays=np.asarray(holidays, dtype="M8[D]"),
        weekmask="1111100",
    )


@pytest.mark.parametrize(
    argnames=("dt", "expected"),
    argvalues=[
        (Date(2025, 1, 2), True),
        (Date(2025, 2, 17), False),
        (Date(2025, 11, 29), False),
    ],
    ids=["busday", "holiday", "weekend"],
)
@pytest.mark.unit
def test_is_busday(dt: Date, expected: bool, buscal: BusinessCalendar) -> None:  # noqa: FBT001
    assert buscal.is_busday(dt) == expected
