"""OIS indices."""

from dataclasses import dataclass, field

from pendulum.duration import Duration

from quant_py.rate_index import RateIndexMetadata


@dataclass(
    init=True,
    frozen=True,
    slots=True,
    weakref_slot=False,
)
class OisRateIndexMetadata(RateIndexMetadata):
    """Metadata for an OIS rate index."""

    publish_lag: int
    tenor: Duration = field(default=Duration(days=1), init=False)
