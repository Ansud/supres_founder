"""
Parse CSV file to list of OHLC tuples
"""

from __future__ import annotations

import csv
from pathlib import Path

from source.structures import OHLCData


async def parse_csv(file_name: str, positions: list[int], delimiter: str = ",") -> list[OHLCData]:
    """
    Parse CSV values to list of OHLC prices, syncronous.

    :param file_name: File to read from
    :param delimiter: CSV fields delimiter
    :param positions: OHLC positions in CSV lines
    """
    out = list()

    file_path = Path(file_name)

    with file_path.open("r") as file:  # noqa: ASYNC230
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
