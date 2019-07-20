"""
Grab data from alphavantage
"""

from datetime import datetime
import urllib.request
import urllib.parse
import json

from source.structures import OHLCData

# Base alphavantage settings
BASE_URL = 'https://www.alphavantage.co/query'
FUNC_INTRADAY = 'TIME_SERIES_INTRADAY'
FUNC_DAILY = 'TIME_SERIES_DAILY'
# This key is free and can be obtained from alphavantage site
# TODO: make it 'demo' and load from some file or settings.yml
ACCESS_KEY = 'AB9XT0UL83Q50KJ7'


# Keys in returned JSON
KEY_OPEN = '1. open'
KEY_CLOSE = '4. close'
KEY_HIGH = '2. high'
KEY_LOW = '3. low'


# Intraday supported time periods: 1min, 5min, 15min, 30min, 60min
TIME_1MIN = '1min'
TIME_5MIN = '5min'
TIME_15MIN = '15min'
TIME_30MIN = '30min'
TIME_60MIN = '60min'
TIME_DAILY = 'Daily'

SELECTED_TIME = TIME_5MIN


def get_time_series_key(time: str):
    return 'Time Series ({0})'.format(time)


def get_data(ticker: str, function: str):
    parameters = dict(
        function=function,
        symbol=ticker.upper(),
        apikey=ACCESS_KEY,
        outputsize='full',
    )

    if function == FUNC_INTRADAY:
        parameters['interval'] = SELECTED_TIME

    url = BASE_URL + '?' + urllib.parse.urlencode(parameters)

    with urllib.request.urlopen(url) as f:
        # TODO: add exception handling
        output = f.read().decode('utf-8')
        data = json.loads(output)

    return data


def get_parsed_data(ticker: str, function: str):
    raw_data = get_data(ticker, function)

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
        time_format = '%Y-%m-%d'
    else:
        series_key = SELECTED_TIME
        time_format = '%Y-%m-%d %H:%M:%S'

    data = raw_data.get(get_time_series_key(series_key))

    out = list()
    now = datetime.now()

    if not data:
        print('Weird response from server, no data found.\n{0}\n'.format(raw_data))

    for key, item in data.items():
        date = datetime.strptime(key, time_format)

        # I'm interested in last year only
        if (now - date).days > 365:
            continue

        out.append(OHLCData(
            item[KEY_OPEN], item[KEY_HIGH], item[KEY_LOW], item[KEY_CLOSE]
        ))

    return out


def get_daily_data(ticker: str):
    return get_parsed_data(ticker, FUNC_DAILY)


def get_intraday_data(ticker: str):
    return get_parsed_data(ticker, FUNC_INTRADAY)
