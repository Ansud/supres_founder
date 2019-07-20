"""
Process data to find levels
"""


def inc_count(prices, level):
    prices[level] = prices.get(level, 0) + 1


def find_levels(data: list, threshold: int, price_sorted: bool):
    """
    Find levels

    :param data:  list of OHLCData
    :param threshold: do not return levels with kick count less than it
    :param price_sorted: sort levels by price instead of kick count
    :return: list of prices levels sorted by count
    """
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

    key = 0 if price_sorted else 1
    return sorted(levels, key=lambda x: x[key], reverse=True)
