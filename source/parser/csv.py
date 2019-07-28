"""
Parse CSV file to list of OHLC tuples
"""

import csv
from typing import Optional

from source.structures import OHLCData


async def parse_csv(
        file_name: str,
        delimiter: Optional[str] = ',',
        positions: Optional[list] = None
    ):
    """
    Parse CSV values to list of OHLC prices, syncronous.

    :param file_name: File to read from
    :param delimiter: CSV fields delimiter
    :param positions: OHLC positions in CSV lines
    :return: list of tuple(O, H, L, C)
    """
    out = list()

    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=delimiter)

        possible_header = next(reader)

        try:
            out.append(OHLCData(*[possible_header[x] for x in positions]))
        except ValueError:
            # This exception should happen only once or never.
            # Thus it is not handled in loop
            pass

        for row in reader:
            out.append(OHLCData(*[row[x] for x in positions]))

    return out
