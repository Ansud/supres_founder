"""
Argument specifications and parsing
"""

import argparse


class ArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--price-sorted", help="Sort levels by price instead of count", action='store_true')
        parser.add_argument("--threshold", type=int, help="Level kick count threshold", default=5)
        parser.add_argument("--csv", type=str, help="CSV file with OHLC bar values")
        parser.add_argument("--csv-ohlc", type=str, help="CSV OHLC comma separated positions", default='0, 1, 2, 3')
        parser.add_argument("--ticker", type=str, help="Equity ticker (download only)")
        parser.add_argument(
            "--price-fuzz", type=float,
            help="Price fuzz. I.e. count prices in some neighbourhood of level"
        )

        self.arguments = parser.parse_args()

    @property
    def csv_ohlc(self):
        return [int(x) for x in self.arguments.csv_ohlc.split(',')]

    @property
    def ticker(self):
        ticker = self.arguments.ticker

        if ticker:
            ticker = ticker.upper()

        return ticker

    def __getattr__(self, item):
        return getattr(self.arguments, item)
