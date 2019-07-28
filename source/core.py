"""
Entry point for all operations
"""

import asyncio

from .analyzer import filter_daily_bars, filter_data, find_levels
from .downloader import download_daily_data, download_intraday_data
from .parse_arguments import ArgumentParser
from .parser import parse_csv


async def return_empty():
    return list()


def load_data(arguments: ArgumentParser):
    """

    :param arguments: program arguments
    :return: coroutines tuple that will return two lists of OHLC data, first element used in filtering
    """
    if arguments.csv is not None:
        return return_empty(), parse_csv(arguments.csv, positions=arguments.csv_ohlc)

    if arguments.ticker is not None:
        return download_daily_data(arguments.ticker), download_intraday_data(arguments.ticker)

    return return_empty(), return_empty()


async def run_project():
    arguments = ArgumentParser()

    daily, intraday = load_data(arguments)

    # Convert to tasks
    print('Wait completion')
    daily, intraday = await asyncio.gather(daily, intraday)
    print('Wait completion done')

    daily = filter_daily_bars(daily)
    data = filter_data(daily, intraday, arguments.price_fuzz)

    levels = find_levels(data, arguments.threshold, arguments.price_sorted)

    print('We found following levels:')

    if not levels:
        print('No any....')
        return

    for l in levels:
        print('Level price: {0}\tcount {1}'.format(l[0], l[1]))
