"""Business calendar."""

from typing import TYPE_CHECKING, Self

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from pendulum.date import Date


# TODO(jkitzlr): implementation
class BusinessCalendar:
    """WIP."""

    def __init__(  # noqa: D107
        self: Self,
        holidays: NDArray[np.datetime64] | None = None,
        weekmask: str = "1111100",
    ) -> None:
        self.holidays: NDArray[np.datetime64] = (
            np.array([], dtype="M8[D]") if holidays is None else holidays
        )
        self.weekmask = weekmask

    def is_busday(self: Self, dt: Date) -> bool:
        """Check whether the input date ``dt`` is a business day.

        Args:
            dt: the date to check.

        Returns:
            Whether ``dt`` is a busday.
        """
        return np.is_busday(
            dates=dt, weekmask=self.weekmask, holidays=self.holidays
        ).item()
