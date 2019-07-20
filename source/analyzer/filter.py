"""
Process daily and intraday data to filter out wrong levels
"""

from source.structures.intervals import Intervals


def filter_daily_bars(daily: list):
    """
    Remove ordinary bars and leave only bars with high shadow
    """
    return daily


def filter_data(daily: list, intraday: list, fuzz: float):
    """
    The idea is simple: need to get all OHLC prices from daily basis and cleanup intraday
    prices to remove all of them which are not located near daily prices with some fuzz.

    :param daily: daily OHLC data
    :param intraday: intraday OHLC data
    :param fuzz: price level neighbourhood
    :return: filtered OHLC data
    """
    if not daily:
        return intraday

    possible = Intervals()
    price_list = [item for ohlc in daily for item in ohlc.shadows()]

    for price in price_list:
        possible.add(price - fuzz, price + fuzz)

    possible.normalize()
    print(possible.intervals)

    out = list()

    for ohlc in intraday:
        for price in ohlc.linearize():
            if possible.miss(price):
                continue

            out.append(ohlc)
            break

    print('Filtering complete:\n\tRemoved\t{0}\n\tRemained\t{1}\n\tOverall\t{2}'.format(
        len(intraday) - len(out), len(out), len(intraday)
    ))

    return out

