from source.structures.intervals import Intervals


def test_intervals_normalize() -> None:
    values = [(0, 1), (2, 3), (4, 5), (5, 6), (10, 15), (13, 25), (100, 1000), (50, 60), (70, 80), (55, 57)]
    expected = [(0, 1), (2, 3), (4, 6), (10, 25), (50, 60), (70, 80), (100, 1000)]

    interval = Intervals()

    for v in values:
        interval.add(v[0], v[1])

    interval.normalize()

    assert len(expected) == len(interval.intervals)

    for i in range(len(expected)):
        assert expected[i] == interval.intervals[i]


def test_intervals_hit() -> None:
    test_data = [
        (-1, False),
        (100000, False),
        (9, False),
        (93, False),
        (0.001, True),
        (4.5, True),
        (999, True),
        (80, True),
        (0, True),
        (1000, True),
        (86, True),
        (51, True),
    ]
    interval = Intervals()

    for v in [(0, 1), (4, 5), (6, 8), (10, 25), (50, 60), (70, 80), (85, 90), (100, 1000)]:
        interval.add(v[0], v[1])

    interval.normalize()

    for item in test_data:
        print(f"Test {item[0]} -> {item[1]}")
        assert interval.hit(item[0]) == item[1]
