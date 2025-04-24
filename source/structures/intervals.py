"""
Intervals storage.

There is array of intervals, sorted by start.
The main functionality - detect is point belongs to any of them or not.
"""

from __future__ import annotations


class Intervals:
    intervals: list[tuple[float, float]]

    def __init__(self) -> None:
        self.intervals = list()

    def add(self, start: float, end: float) -> None:
        # Let simplify my life and call normalize manually
        self.intervals.append((start, end))

    def normalize(self) -> None:
        # Sort intervals by first point
        self.intervals = sorted(self.intervals, key=lambda x: x[0])

        intervals_iter = iter(self.intervals)
        current = next(intervals_iter)

        # Merge them to another list
        out: list[list[float]] = list()
        # The tuple can't be modified, thus make it list and convert later back
        out.append([current[0], current[1]])
        current_end = out[0][1]

        for item in intervals_iter:
            if item[0] <= current_end:
                if item[1] <= current_end:
                    continue

                out[-1][1] = item[1]
            else:
                out.append([item[0], item[1]])

            current_end = item[1]

        # Convert back to tuples
        self.intervals = [(x[0], x[1]) for x in out]

    def hit(self, point: float) -> bool:
        # Run through the list of intervals to find points
        start = 0
        end = len(self.intervals)

        while True:
            length = (end - start) // 2
            position = start + length
            current = self.intervals[position]

            # Point lay in the interval
            if current[0] <= point <= current[1]:
                return True

            if start == end or not length:
                return False

            # Calculate next interval
            if point > current[1]:
                start = position
            elif point < current[0]:
                end = position

    def miss(self, point: float) -> bool:
        return not self.hit(point)
