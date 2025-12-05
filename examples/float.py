import numpy as np

from quant_py.daycounters.act360 import Act360
from quant_py.indices.ois_index import OisRateIndexMetadata
from quant_py.scheduling.adjuster import BusdayConvention


def usgs() -> np.busdaycalendar:
    """Get US Government Securities calendar."""
    holidays = [
        "2025-01-01",
        "2025-01-20",
        "2025-02-17",
        "2025-04-18",
        "2025-05-26",
        "2025-06-19",
        "2025-07-04",
        "2025-09-01",
        "2025-10-13",
        "2025-11-11",
        "2025-11-27",
        "2025-12-25",
    ]
    return np.busdaycalendar(
        holidays=np.asarray(holidays, dtype="M8[D]"),
        weekmask="1111100",
    )


def main() -> None:
    metadata = OisRateIndexMetadata(
        name="SOFR",
        currency="USD",
        pay_cal=usgs(),
        busday_conv=BusdayConvention.FOLLOWING,
        daycounter=Act360(),
        publish_lag=1,
    )
    print(metadata)


if __name__ == "__main__":
    main()
