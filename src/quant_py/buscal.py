"""Business calendar."""

from typing import TYPE_CHECKING, Self

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


# TODO(jkitzlr): implementation
class BusinessCalendar:
    """WIP."""

    def __init__(  # noqa: D107
        self: Self,
        holidays: NDArray[np.datetime64] | None = None,
        weekmask: str = "1111100",
    ) -> None:
        self.holidays: NDArray[np.datetime64] = holidays or np.array([], dtype="M8[D]")
        self.weekmask = weekmask
