"""
Entry point for all operations
"""

from .parse_arguments import ArgumentParser
from .parser import parse_csv
from .analyzer import find_levels, filter_daily_bars, filter_data
from .downloader import download_intraday_data, download_daily_data


def load_data(arguments: ArgumentParser):
    """

    :param arguments: program arguments
    :return: tuple with two lists of OHLC data, second element used in filtering
    """
    if arguments.csv is not None:
        return parse_csv(arguments.csv, positions=arguments.csv_ohlc), list()

    if arguments.ticker is not None:
        return download_intraday_data(arguments.ticker), download_daily_data(arguments.ticker)

    return list(), list()


def run_project():
    arguments = ArgumentParser()

    intraday, daily = load_data(arguments)

    daily = filter_daily_bars(daily)
    data = filter_data(daily, intraday, arguments.price_fuzz)

    levels = find_levels(data, arguments.threshold, arguments.price_sorted)

    print('We found following levels:')

    if not levels:
        print('No any....')
        return

    for l in levels:
        print('Level price: {0}\tcount {1}'.format(l[0], l[1]))

