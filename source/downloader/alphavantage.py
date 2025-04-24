"""
Grab data from alphavantage
"""

import json
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any

import aiohttp

from source.structures import OHLCData

# Base alphavantage settings
BASE_URL = "https://www.alphavantage.co/query"
FUNC_INTRADAY = "TIME_SERIES_INTRADAY"
FUNC_DAILY = "TIME_SERIES_DAILY"
# This key is free and can be obtained from alphavantage site
# TODO: store it in settings
ACCESS_KEY = "AB9XT0UL83Q50KJ7"


# Keys in returned JSON
KEY_OPEN = "1. open"
KEY_CLOSE = "4. close"
KEY_HIGH = "2. high"
KEY_LOW = "3. low"


# Intraday supported time periods: 1min, 5min, 15min, 30min, 60min
TIME_1MIN = "1min"
TIME_5MIN = "5min"
TIME_15MIN = "15min"
TIME_30MIN = "30min"
TIME_60MIN = "60min"
TIME_DAILY = "Daily"

SELECTED_TIME = TIME_5MIN


def get_time_series_key(time: str) -> str:
    return f"Time Series ({time})"


async def get_data(ticker: str, function: str) -> dict[str, Any]:
    parameters = dict(function=function, symbol=ticker.upper(), apikey=ACCESS_KEY, outputsize="full")

    if function == FUNC_INTRADAY:
        parameters["interval"] = SELECTED_TIME

    url = BASE_URL + "?" + urllib.parse.urlencode(parameters)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                text = await response.text()
                out = json.loads(text)

                if not isinstance(out, dict):
                    print(f"Weird response from server, incorrect format: \n{text}\n")
                    raise ValueError("Invalid response from server")

                return out
            except json.JSONDecodeError:
                return dict()


async def get_parsed_data(ticker: str, function: str) -> list[OHLCData]:
    raw_data = await get_data(ticker, function)

    """
    Extract values from JSON

        "Time Series (5min)": {
        "2019-07-18 16:00:00": {
            "1. open": "1145.9500",
            "2. high": "1147.5100",
            "3. low": "1145.9500",
            "4. close": "1146.5601",
            "5. volume": "36550"
        },
    """
    if function == FUNC_DAILY:
        series_key = TIME_DAILY
        time_format = "%Y-%m-%d"
    else:
        series_key = SELECTED_TIME
        time_format = "%Y-%m-%d %H:%M:%S"

    data = raw_data.get(get_time_series_key(series_key))

    out = list()
    now = datetime.now()

    if not data:
        print(f"Weird response from server, no data found.\n{raw_data}\n")
        raise ValueError("Invalid response from server")

    for key, item in data.items():
        date = datetime.strptime(key, time_format)

        # I'm interested in last year only
        if (now - date).days > 365:
            continue

        out.append(OHLCData(item[KEY_OPEN], item[KEY_HIGH], item[KEY_LOW], item[KEY_CLOSE]))

    return out


async def get_daily_data(ticker: str) -> list[OHLCData]:
    return await get_parsed_data(ticker, FUNC_DAILY)


async def get_intraday_data(ticker: str) -> list[OHLCData]:
    return await get_parsed_data(ticker, FUNC_INTRADAY)
