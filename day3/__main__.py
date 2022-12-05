from os import path
import unittest

LOWERCASE_SHIFT = - ord("a") + 1
UPPERCASE_SHIFT = - ord("A") + 27
FIRST_LOWER_CASE = ord("a")


def find_item_in_line(line):
    l = len(line) // 2
    a, b = line[:l], line[l:]
    b_set = set(b)
    for i in a:
        if i in b_set:
            return i
    raise BaseException("Atleast one item expected")

def find_badge_in_group(group):
    x, y, z = group
    y = set(y)
    z = set(z)
    for c in x:
        if c in y and c in z:
            return c
    raise BaseException("Atleast one item expected")

def score_item(item):
    initial_value = ord(item)
    if initial_value >= FIRST_LOWER_CASE:
        return initial_value + LOWERCASE_SHIFT
    else:
        return initial_value + UPPERCASE_SHIFT


def score_lines(lines):
    return sum(score_item(find_item_in_line(l)) for l in lines)

def score_groups(lines):
    return sum(score_item(find_badge_in_group(c)) for c in chunks(lines, 3))

def chunks(seq, size):
    res = []
    for element in seq:
        res.append(element)
        if len(res) == size:
            yield res
            res = []
    if res:
        yield res

def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def score_file(fname):
    lines = list(read_lines(fname))
    return (score_lines(lines), score_groups(lines))


class TestDay(unittest.TestCase):

    def test_find_item_in_line(self):
        self.assertEqual(find_item_in_line("vJrwpWtwJgWrhcsFMMfFFhFp"), "p")
        self.assertEqual(
            find_item_in_line("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"),
            "L"
        )
        self.assertEqual(find_item_in_line("PmmdzqPrVvPwwTWBwg"), "P")
        self.assertEqual(
            find_item_in_line("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"),
            "v"
        )
        self.assertEqual(find_item_in_line("ttgJtRGJQctTZtZT"), "t")
        self.assertEqual(find_item_in_line("CrZsJsPPZsGzwwsLwLmpwMDw"), "s")

    def test_find_badge_in_group(self):
        group = [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg"
        ]
        self.assertEqual(find_badge_in_group(group), "r")

    def test_score_groups(self):
        lines = [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw"
        ]
        self.assertEqual(score_groups(lines), 70)


    def test_score_item(self):
        self.assertEqual(score_item("p"), 16)
        self.assertEqual(score_item("L"), 38)
        self.assertEqual(score_item("P"), 42)
        self.assertEqual(score_item("v"), 22)
        self.assertEqual(score_item("t"), 20)
        self.assertEqual(score_item("s"), 19)

    def test_score_lines(self):
        lines = [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw"
        ]
        self.assertEqual(score_lines(lines), 157)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), (157, 70))


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
