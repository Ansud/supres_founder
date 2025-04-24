"""
Entry point for all operations
"""

import asyncio
from collections.abc import Awaitable

from .analyzer import filter_daily_bars, filter_data, find_levels
from .downloader import download_daily_data, download_intraday_data
from .parse_arguments import ArgumentParser
from .parser import parse_csv
from .structures import OHLCData


async def return_empty() -> list[OHLCData]:
    return list()


def load_data(arguments: ArgumentParser) -> tuple[Awaitable[list[OHLCData]], Awaitable[list[OHLCData]]]:
    """

    :param arguments: program arguments
    :return: coroutines tuple that will return two lists of OHLC data, first element used in filtering
    """
    if arguments.csv_mode:
        if arguments.daily is not None:
            daily = parse_csv(arguments.arguments.daily, positions=arguments.ohlc_positions)
        else:
            daily = return_empty()
        return daily, parse_csv(arguments.arguments.intraday, positions=arguments.ohlc_positions)

    if arguments.fetch_mode:
        return download_daily_data(arguments.ticker), download_intraday_data(arguments.ticker)

    return return_empty(), return_empty()


async def run_project() -> None:
    arguments = ArgumentParser()

    daily_getter, intraday_getter = load_data(arguments)

    daily, intraday = await asyncio.gather(daily_getter, intraday_getter)

    daily = filter_daily_bars(daily)
    data = filter_data(daily, intraday, arguments.price_fuzz)

    levels = find_levels(data, arguments.threshold, arguments.price_sorted)

    print("We found following levels:")

    if not levels:
        print("No any....")
        return

    for level in levels:
        print(f"Level price: {level[0]}\tcount {level[1]}")
