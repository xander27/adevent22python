
from dataclasses import dataclass
from os import path
import re
import unittest


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


@dataclass
class Range:
    begin: int
    end: int

    def overlap(self, other):
        if self.begin <= other.begin and self.end >= other.begin:
            return True
        if self.begin >= other.begin and self.begin <= other.end:
            return True
        return False

    def join(self, other):
        return Range(min(self.begin, other.begin), max(self.end, other.end))


@dataclass
class Sensor():
    own_x: int
    own_y: int
    beacon_x: int
    beacon_y: int
    distance: int

    def __init__(self, own_x, own_y, beacon_x, beacon_y):
        self.own_x = own_x
        self.own_y = own_y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        self.distance = distance(own_x, own_y, beacon_x, beacon_y)


def parse_sensor(line):
    digits_groups = [(a.start(), a.end())
                     for a in list(re.finditer('\-?[\d]+', line))]
    numbers = []
    for i in range(4):
        begin = digits_groups[i][0]
        end = digits_groups[i][1]
        numbers.append(int(line[begin:end]))
    return Sensor(*numbers)


def read_sensors(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    result = []
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            result.append(parse_sensor(line))
    return result


def append_range(others, new_range):
    while True:
        for i, other in enumerate(others):
            if new_range.overlap(other):
                new_range = new_range.join(other)
                del others[i]
                break
        else:
            others.append(new_range)
            return others


def count_points_in_line(sensors, y):
    ranges = []
    for sensor in sensors:
        y_distance = abs(sensor.own_y - y)
        max_x_distnace = sensor.distance - y_distance
        if max_x_distnace >= 0:
            new_range = Range(sensor.own_x - max_x_distnace,
                              sensor.own_x + max_x_distnace)
            append_range(ranges, new_range)
    return sum(r.end - r.begin for r in ranges)

def solve_file(fname, y):
    sensors = read_sensors(fname)
    return count_points_in_line(sensors, y)


class TestDay(unittest.TestCase):

    SENSORS = [
        Sensor(2, 18, -2, 15),
        Sensor(9, 16, 10, 16),
        Sensor(13, 2, 15, 3),
        Sensor(12, 14, 10, 16),
        Sensor(10, 20, 10, 16),

        Sensor(14, 17, 10, 16),
        Sensor(8, 7, 2, 10),
        Sensor(2, 0, 2, 10),
        Sensor(0, 11, 2, 10),
        Sensor(20, 14, 25, 17),

        Sensor(17, 20, 21, 22),
        Sensor(16, 7, 15, 3),
        Sensor(14, 3, 15, 3),
        Sensor(20, 1, 15, 3)
    ]

    def test_parse_sensor(self):
        self.assertEqual(
            parse_sensor(
                "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"),
            Sensor(2, 18, -2, 15)
        )

    def test_read_sensors(self):
        self.assertEqual(read_sensors("input-test.txt"), self.SENSORS)

    def test_count_points_in_line(self):
        self.assertEqual(count_points_in_line(self.SENSORS, 10), 26)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt", 10), 26)


if __name__ == '__main__':
    print(solve_file("input.txt", 2000000))
    unittest.main()
