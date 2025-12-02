"""Business day adjuster."""

from dataclasses import dataclass
from enum import Enum
from typing import Self

import numpy as np
from pendulum.date import Date


class BusdayConvention(Enum):
    """Enumerate the business day conventions."""

    FOLLOWING = "following"
    PRECEDING = "preceding"
    MODIFIEDFOLLOWING = "modifiedfollowing"
    MODIFIEDPRECEDING = "modifiedpreceding"
    NONE = "none"


@dataclass(
    init=True,
    frozen=True,
    slots=True,
    weakref_slot=False,
)
class Adjuster:
    """Contain business day adjuster logic."""

    calendar: np.busdaycalendar
    busday_conv: BusdayConvention

    def adjust(self: Self, dt: Date) -> Date:
        """Apply these business day adjustments to ``date``.

        Args:
            dt: The date to adjust.

        Returns:
            The adjusted date.
        """
        if self.busday_conv == BusdayConvention.NONE:
            return dt

        adjusted = np.busday_offset(  # type: ignore[no-matching-overload]
            dt, offsets=0, roll=self.busday_conv.value, busdaycal=self.calendar
        )
        return adjusted.astype(Date)
