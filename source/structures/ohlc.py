"""
Data storage class

TODO: Add ability to analyse bar type
"""

from __future__ import annotations


class OHLCData:
    def __init__(self, open: str, high: str, low: str, close: str) -> None:
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)

    def linearize(self) -> tuple[float, float, float, float]:
        return self.open, self.high, self.low, self.close

    def shadows(self) -> tuple[float, float]:
        return self.high, self.low
