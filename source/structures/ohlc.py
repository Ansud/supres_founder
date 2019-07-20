"""
Data storage class

TODO: Add ability to analyse bar type
"""


class OHLCData:
    def __init__(self, open, high, low, close):
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)

    def linearize(self):
        return self.open, self.high, self.low, self.close

    def shadows(self):
        return self.high, self.low
