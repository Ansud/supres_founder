"""
Process data to find levels
"""


def inc_count(prices, level):
    prices[level] = prices.get(level, 0) + 1


def find_levels(data):
    """
    Find levels

    :param data:  sources.structures.ohlc.OHLCData
    :return: list of prices levels sorted by count
    """
    threshold = 5
    levels = list()
    prices = dict()

    for d in data:
        inc_count(prices, d.open)
        inc_count(prices, d.close)
        inc_count(prices, d.high)
        inc_count(prices, d.low)

    # Linearize and remove levels < threshold count
    for price, count in prices.items():
        if count < threshold:
            continue

        levels.append((price, count))

    return sorted(levels, key=lambda x: x[1], reverse=True)
