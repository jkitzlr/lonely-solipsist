"""Scheudle class."""

from typing import TYPE_CHECKING, Self

from quant_py.scheduling.adjuster import Adjuster, BusdayConvention
from quant_py.scheduling.period import Period
from quant_py.scheduling.roll_convention import Bom, DayOfMonth, Eom, RollConventions

if TYPE_CHECKING:
    import numpy as np
    from pendulum.date import Date
    from pendulum.duration import Duration


# TODO(jkitzlr): make properties settable(?)
class Schedule:
    """Schedule. WIP."""

    # TODO(jkitzlr): make this a class constructor, __init__ take final attribs(?)
    def __init__(
        self: Self,
        effective: Date,
        termination: Date,
        tenor: Duration,
        pay_cal: np.busdaycalendar,
        busday_conv: BusdayConvention,
        front_stub: Date | None = None,  # ? rename to first reg pmt?
        back_stub: Date | None = None,
        *,
        eom: bool = False,
        bom: bool = False,
    ) -> None:
        """TBD."""
        adjuster = Adjuster(calendar=pay_cal, busday_conv=busday_conv)

        self._periods: list[Period] = []

        start = effective
        # handle case where there's a front stub
        if front_stub is not None:
            self._periods.append(
                Period(
                    start=adjuster.adjust(effective),
                    end=adjuster.adjust(front_stub),
                    unadj_start=effective,
                    unadj_end=front_stub,
                )
            )
            start = front_stub

        roll_conv = self._get_roll_conv(start, eom=eom, bom=bom)
        end = back_stub or termination

        dt = start
        while dt < end:
            p_end = roll_conv.next(dt, tenor)
            self._periods.append(
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
            self._periods.append(
                Period(
                    start=adjuster.adjust(back_stub),
                    end=adjuster.adjust(termination),
                    unadj_start=back_stub,
                    unadj_end=termination,
                )
            )

        self._tenor = tenor
        self._busday_conv = busday_conv
        self._adjuster = adjuster
        self._roll_conv = roll_conv

    @property
    def periods(self: Self) -> list[Period]:
        """Get the list of schedule periods."""
        return self._periods.copy()

    @property
    def roll_convention(self: Self) -> RollConventions:  # pragma: no cover
        """Get the roll convention used to build the schedule."""
        return self._roll_conv

    @property
    def adjuster(self: Self) -> Adjuster:  # pragma: no cover
        """Get the busday adjuster used to generate the schedule."""
        return self._adjuster

    @property
    def tenor(self: Self) -> Duration:  # pragma: no cover
        """Get the period Tenor used to build the schedule."""
        return self._tenor

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
