"""Encapsulate roll day logic.

Specifically, when calculating a sequence of dates with month or year Periodicity,
need a way to adjust the resulting date to the desired day of the month.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self, override

from dateutil.relativedelta import relativedelta

if TYPE_CHECKING:
    from pendulum.date import Date
    from pendulum.duration import Duration


class RollConventions(ABC):
    """Define the interface for roll conventions.

    These handle adjusting dates in a date sequence (e.g. an accrual schedule).
    """

    def next(self: Self, dt: Date, tenor: Duration) -> Date:
        """Calculate the next date in a sequence after ``dt``.

        Args:
            dt: The date to adjust.
            tenor: The tenor/period between dates in the sequence.

        Returns:
            The next date in the sequence, adjusted as appropriate.
        """
        return self.adjust(dt + tenor)

    def previous(self: Self, dt: Date, tenor: Duration) -> Date:
        """Calculate the previous date in a sequence before ``dt``.

        Args:
            dt: The date to adjust.
            tenor: The tenor/period between dates in the sequence.

        Returns:
            The previous date in the sequence, adjusted as appropriate.
        """
        return self.adjust(dt - tenor)

    @abstractmethod
    def adjust(self: Self, dt: Date) -> Date:
        """Adjust the input date to this roll day.

        Args:
            dt: The date to adjust.

        Returns:
            Adjusted date.
        """


# TODO(jkitzlr): How to handle specific day of week, etc.
class DayOfMonth(RollConventions):
    """WIP."""

    def __init__(self: Self, day: int) -> None:
        """WIP."""
        self.day = day

    def __eq__(self: Self, other: object) -> bool:  # noqa: D105
        if isinstance(other, DayOfMonth):
            return self.day == other.day

        return False

    @override
    def adjust(self: Self, dt: Date) -> Date:
        """Adjust the input date to this roll day.

        NOTE: will automatically handle date overflow, e.g., setting roll day to
        31st in a month with fewer than 30 days will return end of month (see examples).

        Args:
            dt: The date to adjust.

        Returns:
            Adjusted date.

        Examples:
            >>> from pendulum import Date
            >>> from quant_py.scheduling.roll_day import RollDay
            >>> dt = Date(2025, 11, 16)
            >>> roll_day = RollDay(15)
            >>> roll_day.adjust(dt)
            Date(2025, 11, 15)
            >>> # automatically handles difference in # of days in months
            >>> roll_day31 = RollDay(31)
            >>> roll_day31.adjust(dt)
            Date(2025, 11, 30)
        """
        return dt + relativedelta(day=self.day)


class Eom(RollConventions):
    """Always roll to the end of the month."""

    def __eq__(self: Self, other: object) -> bool:  # noqa: D105
        return isinstance(other, Eom)

    @override
    def adjust(self: Self, dt: Date) -> Date:
        """Adjust the input date to the last calendar day of the month.

        Args:
            dt: The date to adjust.

        Returns:
            ``dt`` adjust to end of month.

        Examples:
            >>> from pendulum import Date
            >>> from quant_py.scheduling.roll_day import Eom
            >>> roll_day = Eom()
            >>> dt = Date(2025, 11, 28)
            >>> roll_day.adjust(dt)
            Date(2025, 11, 30)
        """
        return dt.end_of(unit="month")


class Bom(RollConventions):
    """Always roll to the start of the month."""

    def __eq__(self: Self, other: object) -> bool:  # noqa: D105
        return isinstance(other, Bom)

    @override
    def adjust(self: Self, dt: Date) -> Date:
        """Adjust the input date to the first calendar day of the month.

        Args:
            dt: The date to adjust.

        Returns:
            ``dt`` adjust to start of month.

        Examples:
            >>> from pendulum import Date
            >>> from quant_py.scheduling.roll_day import Bom
            >>> roll_day = Bom()
            >>> dt = Date(2025, 11, 28)
            >>> roll_day.adjust(dt)
            Date(2025, 11, 1)
        """
        return dt.start_of("month")
