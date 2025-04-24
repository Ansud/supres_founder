"""
Grab data from internet

May be i will support more sources, but currently only alphavantage is supported,
thus this file a bit ridiculous
"""

from source.structures import OHLCData

from .alphavantage import get_daily_data, get_intraday_data


async def download_daily_data(ticker: str) -> list[OHLCData]:
    print(f"Start downloading daily data for {ticker}...")
    data = await get_daily_data(ticker)
    print(f"Complete downloading daily data for {ticker}...")
    return data


async def download_intraday_data(ticker: str) -> list[OHLCData]:
    print(f"Start downloading intraday data for {ticker}...")
    data = await get_intraday_data(ticker)
    print(f"Complete downloading intraday data for {ticker}...")
    return data
