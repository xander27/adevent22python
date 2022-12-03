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
    raise "Atleast one item expected"


def score_item(item):
    initial_value = ord(item)
    if initial_value >= FIRST_LOWER_CASE:
        return initial_value + LOWERCASE_SHIFT
    else:
        return initial_value + UPPERCASE_SHIFT


def score_lines(lines):
    sum = 0
    for line in lines:
        item = find_item_in_line(line)
        sum = sum + score_item(item)
    return sum


def read_lines(fname):
    with open(fname) as file:
        for s in file:
            yield s


def score_file(fname):
    return score_lines(read_lines(fname))


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
        self.assertEqual(score_file("input-test.txt"), 157)


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
