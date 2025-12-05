"""Base class for various types of interest rate indexes (e.g. IBORs, OIS, etc.)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    import numpy as np
    from pendulum.date import Date
    from pendulum.duration import Duration

    from quant_py.daycounter import Daycounter
    from quant_py.scheduling.adjuster import BusdayConvention


# TODO(jkitzlr): OIS get optional publish_delay prop
# TODO(jkitzlr): Included secured/unsecured info?
@dataclass(
    init=True,
    frozen=True,
    slots=True,
    weakref_slot=False,
)
class RateIndexMetadata:
    """Metadata/conventions for a particular index."""

    name: str
    currency: str
    tenor: Duration
    pay_cal: np.busdaycalendar
    busday_conv: BusdayConvention
    daycounter: Daycounter


@dataclass(
    init=True,
    frozen=True,
    slots=True,
    weakref_slot=False,
)
class RateIndex[T: RateIndexMetadata](ABC):
    """WIP."""

    metadata: T

    @abstractmethod
    def calc_fixing_dt(self: Self, dt: Date) -> Date:
        """Calculate the fixing date from date conventions and publish/settle delay.

        Args:
            dt: The date from which to determine the fixing date.

        Returns:
            Fixing date.
        """
