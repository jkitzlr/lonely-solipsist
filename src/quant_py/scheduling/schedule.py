"""Scheudle class."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from quant_py.scheduling.adjuster import Adjuster, BusdayConvention
from quant_py.scheduling.period import Period
from quant_py.scheduling.roll_convention import Bom, DayOfMonth, Eom, RollConventions

if TYPE_CHECKING:
    import numpy as np
    from pendulum.date import Date
    from pendulum.duration import Duration


@dataclass(
    init=True,
    frozen=True,
    slots=True,
    weakref_slot=False,
)
class Schedule:
    """Schedule. WIP."""

    periods: list[Period]
    roll_conv: RollConventions
    adjuster: Adjuster
    tenor: Duration

    @classmethod
    def of(
        cls: type[Self],
        effective: Date,
        termination: Date,
        tenor: Duration,
        pay_cal: np.busdaycalendar,
        busday_conv: BusdayConvention,
        front_stub: Date | None = None,
        back_stub: Date | None = None,
        *,
        eom: bool = False,
        bom: bool = False,
    ) -> Self:
        """Construct the Schedule object from conventions.

        Args:
            effective: Start date of the schedule.
            termination: End date of the schedule.
            tenor: The time interval between successive dates in the schedule.
            pay_cal: Busday calendar to use to adjust schedule dates to busdays.
            busday_conv: The busday adjust convention.
            front_stub: First reg payment date (e.g. front is stub). Defaults to None.
            back_stub: The last reg payment date (e.g. back is stub). Defaults to None.
            eom: Whether to roll dates to last cal day of month. Defaults to False.
            bom: Whether to roll dates to first cal day of month. Defaults to False.

        Returns:
            Schedule.
        """
        adjuster = Adjuster(calendar=pay_cal, busday_conv=busday_conv)

        periods: list[Period] = []

        start = effective
        # handle case where there's a front stub
        if front_stub is not None:
            periods.append(
                Period(
                    start=adjuster.adjust(effective),
                    end=adjuster.adjust(front_stub),
                    unadj_start=effective,
                    unadj_end=front_stub,
                )
            )
            start = front_stub

        roll_conv = cls._get_roll_conv(start, eom=eom, bom=bom)
        end = back_stub or termination

        dt = start
        while dt < end:
            p_end = roll_conv.next(dt, tenor)
            periods.append(
                Period(
                    start=adjuster.adjust(dt),
                    end=adjuster.adjust(p_end),
                    unadj_start=dt,
                    unadj_end=p_end,
                )
            )
            dt = p_end

        # handle back stubs
        if back_stub is not None:
            periods.append(
                Period(
                    start=adjuster.adjust(back_stub),
                    end=adjuster.adjust(termination),
                    unadj_start=back_stub,
                    unadj_end=termination,
                )
            )

        return cls(
            periods=periods,
            roll_conv=roll_conv,
            adjuster=adjuster,
            tenor=tenor,
        )

    @staticmethod
    def _get_roll_conv(start: Date, *, eom: bool, bom: bool) -> RollConventions:
        if eom and bom:
            msg = "Schedule cannot roll both beginning and end of month!"
            raise ValueError(msg)

        if eom:
            return Eom()

        if bom:
            return Bom()

        return DayOfMonth(start.day)
