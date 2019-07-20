"""
Grab data from internet

May be i will support more sources, but currently only alphavantage is supported,
thus this file a bit ridiculous
"""

from .alphavantage import get_daily_data, get_intraday_data


def download_daily_data(ticker: str):
    return get_daily_data(ticker)


def download_intraday_data(ticker: str):
    return get_intraday_data(ticker)
