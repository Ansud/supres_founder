"""
Grab data from internet

May be i will support more sources, but currently only alphavantage is supported,
thus this file a bit ridiculous
"""

from .alphavantage import get_daily_data, get_intraday_data


def download_daily_data(ticker: str):
    print('Start downloading daily data for {0}...'.format(ticker))
    data = get_daily_data(ticker)
    print('Complete!')
    return data


def download_intraday_data(ticker: str):
    print('Start downloading intraday data for {0}...'.format(ticker))
    data = get_intraday_data(ticker)
    print('Complete!')
    return data
