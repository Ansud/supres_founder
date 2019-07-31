"""
Argument specifications and parsing
"""

import argparse


class ArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='Commands help')
        parser.add_argument("--price-sorted", help="Sort levels by price instead of count", action='store_true')
        parser.add_argument("--threshold", type=int, help="Level kick count threshold", default=5)
        parser.add_argument(
            "--price-fuzz", type=float,
            help="Price fuzz. I.e. count prices in some neighbourhood of level",
            default=0
        )

        csv_parser = subparsers.add_parser('csv', help='Load data from CSV files')

        csv_parser.add_argument("--intraday", type=str, help="CSV file with OHLC intraday bar values")
        csv_parser.add_argument("--daily", type=str, help="CSV file with OHLC bar values in daily timeframe")
        csv_parser.add_argument("--ohlc-positions", type=str, help="CSV OHLC comma separated positions", default='0, 1, 2, 3')

        net_parser = subparsers.add_parser('fetch', help='Fetch data from internet sources')
        net_parser.add_argument("--ticker", type=str, help="Equity ticker (download only)")

        self.arguments = parser.parse_args()

    @property
    def ohlc_positions(self):
        return [int(x) for x in self.arguments.ohlc_positions.split(',')]

    @property
    def ticker(self):
        ticker = self.arguments.ticker

        if ticker:
            ticker = ticker.upper()

        return ticker

    @property
    def csv_mode(self):
        return 'intraday' in self.arguments

    @property
    def fetch_mode(self):
        return 'ticker' in self.arguments

    def __getattr__(self, item):
        return getattr(self.arguments, item)
