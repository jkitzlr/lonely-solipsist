"""Act/360 daycount implementation."""

from typing import TYPE_CHECKING, Self, override

from quant_py.daycounter._base import Daycounter

if TYPE_CHECKING:
    from pendulum.date import Date


class Act360(Daycounter):
    """ACT/360 impl."""

    @override
    def count(self: Self, start: Date, end: Date) -> float:
        days = (end - start).days
        return float(days) / 360.0
