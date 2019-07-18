"""
Data storage class

TODO: Add ability to analyse bar type
"""


class OHLCData:
    def __init__(self, open, high, low, close):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
