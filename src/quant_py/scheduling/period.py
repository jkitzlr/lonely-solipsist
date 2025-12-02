"""Schedule period."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from pendulum.date import Date
    from pendulum.duration import Duration

    from quant_py.daycounter._base import Daycounter
    from quant_py.scheduling.roll_convention import RollConventions


# TODO(jkitzlr): should this store all the necessary conventions to generate the dates?
@dataclass(
    init=True,
    slots=True,
    frozen=True,
    weakref_slot=False,
)
class Period:
    """Schedule period.

    Attributes:
        unadj_start: The unadjusted start date of the schedule period.
        unadj_end: The unadjusted end date of the schedule period.
        start: The adjusted start date of the schedule period.
        start: The adjusted end date of the schedule period.
    """

    start: Date
    end: Date
    unadj_start: Date
    unadj_end: Date

    def __len__(self: Self) -> int:  # noqa: D105
        return self.length_in_days

    @property
    def length_in_days(self: Self) -> int:
        """Get the number of days in the period."""
        return (self.end - self.start).days

    def calc_year_frac(
        self: Self, daycounter: Daycounter, *, adjusted: bool = True
    ) -> float:
        """Calculate the year fraction of the period.

        Args:
            daycounter: Daycounter with desired daycount convention.
            adjusted: Whether to calc the year frac on adjusted or unadjusted dates.
            Defaults to True.

        Returns:
            Year fraction of the period.
        """
        return (
            daycounter.count(self.start, self.end)
            if adjusted
            else daycounter.count(self.unadj_start, self.unadj_end)
        )

    def is_regular(self: Self, roll_conv: RollConventions, tenor: Duration) -> bool:
        """Determine if this schedule period represents a regular period.

        Args:
            roll_conv: The roll conventions to generate regular dates.
            tenor: The tenor/period between successive regular dates.

        Returns:
            Indicator for whether the period is a regular period.
        """
        return (self.unadj_end == roll_conv.next(self.unadj_start, tenor)) and (
            self.unadj_start == roll_conv.previous(self.unadj_end, tenor)
        )
