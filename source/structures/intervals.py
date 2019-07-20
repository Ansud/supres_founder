"""
Intervals storage.

There is array of intervals, sorted by start.
The main functionality - detect is point belongs to any of them or not.
"""


class Intervals:
    def __init__(self):
        self.intervals = list()

    def add(self, start: float, end: float):
        # Let simplify my life and call normalize manually
        self.intervals.append((start, end))

    def normalize(self):
        # Sort intervals by first point
        self.intervals = sorted(self.intervals, key=lambda x: x[0])

        intervals_iter = iter(self.intervals)
        current = next(intervals_iter)

        # Merge them to another list
        out = list()
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
        self.intervals = [tuple(x) for x in out]

    def hit(self, point: float):
        # Run through intevals list to find points
        start = 0
        end = len(self.intervals)

        while True:
            length = (end - start) // 2
            position = start + length
            current = self.intervals[position]

            # Point lay in interval
            if current[0] <= point <= current[1]:
                return True

            if start == end or not length:
                return False

            # Calculate next interval
            if point > current[1]:
                start = position
            elif point < current[0]:
                end = position

    def miss(self, point: float):
        return not self.hit(point)

    # TODO: Create tests folder and move to unit tests
    @staticmethod
    def test_normalize():
        values = [(0, 1), (2, 3), (4, 5), (5, 6), (10, 15), (13, 25), (100, 1000), (50, 60), (70, 80), (55, 57)]
        expected = [(0, 1), (2, 3), (4, 6), (10, 25), (50, 60), (70, 80), (100, 1000)]

        interval = Intervals()

        for v in values:
            interval.add(v[0], v[1])

        interval.normalize()

        assert len(expected) == len(interval.intervals)

        for i in range(len(expected)):
            assert expected[i] == interval.intervals[i]

    @staticmethod
    def test_hit():
        test_data = [
            (-1, False), (100000, False), (9, False), (93, False),
            (0.001, True), (4.5, True), (999, True), (80, True), (0, True), (1000, True), (86, True), (51, True),
        ]
        interval = Intervals()

        for v in [(0, 1), (4, 5), (6, 8), (10, 25), (50, 60), (70, 80), (85, 90), (100, 1000)]:
            interval.add(v[0], v[1])

        interval.normalize()

        for item in test_data:
            print('Test {0} -> {1}'.format(item[0], item[1]))
            assert interval.hit(item[0]) == item[1]
