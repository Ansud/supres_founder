"""
Parse CSV file to list of OHLC tuples
"""

import csv
from source.structures import OHLCData


def parse_csv(
        file_name,
        delimiter=',',
        positions=None
    ):
    """

    :param file_name: File to read from
    :param delimeter: CSV fields delimener
    :param positions: OHLC positions in CSV lines
    :return: list of tuple(O, H, L, C)
    """
    out = list()

    if positions is not None:
        pos_o = positions[0]
        pos_h = positions[1]
        pos_l = positions[2]
        pos_c = positions[3]
    else:
        pos_o = 0
        pos_h = 1
        pos_l = 2
        pos_c = 3

    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=delimiter)

        for row in reader:
            out.append(OHLCData(
                row[pos_o], row[pos_h], row[pos_l], row[pos_c]
            ))

    return out
