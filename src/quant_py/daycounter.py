"""Define the interface for a daycounter."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from pendulum import Date


class Daycounter(ABC):
    """Interface for daycounter classes."""

    def __call__(self: Self, start: Date, end: Date) -> float:  # noqa: D102
        return self.count(start, end)

    @abstractmethod
    def count(self: Self, start: Date, end: Date) -> float:
        """Compute the year fraction between start an end under this convention.

        Args:
            start: Start date of the period.
            end: End date of the period.

        Returns:
            Year fraction.
        """
