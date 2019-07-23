"""
Process data to find levels
"""


def inc_count(prices, level, bottom):
    if level not in prices:
        prices[level] = dict(b=0, t=0)

    if bottom:
        prices[level]['b'] += 1
    else:
        prices[level]['t'] += 1


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
        if d.open <= d.close:
            inc_count(prices, d.open, bottom=False)
            inc_count(prices, d.close, bottom=True)
        else:
            inc_count(prices, d.open, bottom=True)
            inc_count(prices, d.close, bottom=False)

        # High hits level from bottom only
        inc_count(prices, d.high, bottom=True)
        # Low hits level from top only
        inc_count(prices, d.low, bottom=False)

    # Linearize and remove levels < threshold count
    for price, tb in prices.items():
        if not tb['t'] and not tb['b']:
            continue

        if tb['t'] + tb['b'] < threshold:
            continue

        levels.append((price, tb['t'] + tb['b']))

    key = 0 if price_sorted else 1
    return sorted(levels, key=lambda x: x[key], reverse=True)
