"""
Argument specifications and parsing
"""

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=False, type=str, help="CSV file with OHLC bar values")
    parser.add_argument("--csv-ohlc", required=False, type=str, help="CSV OHLC comma separated positions")

    return parser.parse_args()
