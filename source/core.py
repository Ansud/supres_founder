"""
Entry point for all operations
"""

from .parse_arguments import parse_arguments
from .parser import parse_csv
from .analyzer.finder import find_levels


def run_project():
    data = list()
    # TODO: parse arguments as a class to properly handle some transitions like ohlc
    arguments = parse_arguments()

    if arguments.csv is not None:
        positions = list()
        if arguments.csv_ohlc:
            positions = [int(x) for x in arguments.csv_ohlc.split(',')]
        data = parse_csv(arguments.csv, positions=positions)

    levels = find_levels(data)

    print('We found following levels:')

    if not levels:
        print('No any....')
        return

    for l in levels:
        print('Level price: {0}\tcount {1}'.format(l[0], l[1]))

