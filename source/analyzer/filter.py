"""
Process daily and intraday data to filter out wrong levels
"""

from __future__ import annotations

from source.structures import OHLCData
from source.structures.intervals import Intervals


def filter_daily_bars(daily: list[OHLCData]) -> list[OHLCData]:
    """
    Remove ordinary bars and leave only bars with high shadow
    Now this function does nothing.
    """
    return daily


def filter_data(daily: list[OHLCData], intraday: list[OHLCData], fuzz: float) -> list[OHLCData]:
    """
    The idea is simple: need to get all OHLC prices from daily basis and cleanup intraday
    prices to remove all of them, which are not located near daily prices with some fuzz.

    :param daily: daily OHLC data
    :param intraday: intraday OHLC data
    :param fuzz: price level neighborhood
    :return: filtered OHLC data
    """
    if not daily:
        return intraday

    possible = Intervals()
    price_list = [item for ohlc in daily for item in ohlc.shadows()]

    for price in price_list:
        possible.add(price - fuzz, price + fuzz)

    possible.normalize()

    out: list[OHLCData] = list()

    for ohlc in intraday:
        for price in ohlc.linearize():
            if possible.miss(price):
                continue

            out.append(ohlc)
            break

    print(
        f"Filtering complete:\n\tRemoved\t{len(intraday) - len(out)}\n\tRemained\t{len(out)}\n\tOverall\t{len(intraday)}"
    )

    return out
