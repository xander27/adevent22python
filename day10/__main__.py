
from dataclasses import dataclass
from os import path
import unittest


@dataclass
class Add():
    value: int


class Noop():

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Noop, cls).__new__(cls, *args, **kwargs)
        return cls._instance


@dataclass
class Result:
    registry: list[int]
    crt: str


def parse_instruction(string):
    parts = string.split()
    if parts[0] == "noop":
        return Noop()
    return Add(int(parts[1]))


def reshape_crt(crt):
    return ["".join(crt[i * 40:(i + 1) * 40]) for i in range(6)]


def need_draw(crt_pos, registry):
    rem = crt_pos % 40
    return registry >= rem - 1 and registry <= rem + 1


def execute(instructions):
    registry = [1, 1]
    crt = []
    last = 1
    i = -1
    for instruction in instructions:
        registry.append(last)
        i = i + 1
        draw = need_draw(i, last)
        crt.append("#" if draw else ".")
        if isinstance(instruction, Add):
            i = i + 1
            draw = need_draw(i, last)
            crt.append("#" if draw else ".")
            new_value = last + instruction.value
            registry.append(new_value)
            last = new_value

    return Result(registry, reshape_crt(crt))


def score_registry(results):
    """(that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles)"""
    return sum(p * results[p] for p in [20, 60, 100, 140, 180, 220])


def read_instructions(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for s in file:
            yield parse_instruction(s)


class TestDay(unittest.TestCase):

    INSTRUCTIONS = list(read_instructions("input-test.txt"))

    def test_execute_small(self):
        """
        At the start of the first cycle, the noop instruction begins execution. During the first cycle, X is 1. After the first cycle, the noop instruction finishes execution, doing nothing.
        At the start of the second cycle, the addx 3 instruction begins execution. During the second cycle, X is still 1.
        During the third cycle, X is still 1. After the third cycle, the addx 3 instruction finishes execution, setting X to 4.
        At the start of the fourth cycle, the addx -5 instruction begins execution. During the fourth cycle, X is still 4.
        During the fifth cycle, X is still 4. After the fifth cycle, the addx -5 instruction finishes execution, setting X to -1.
        """
        actual = execute([Noop(), Add(3),  Add(-5)]).registry
        #                                 0, 1, 2, 3, 4, 5
        self.assertSequenceEqual(actual, [1, 1, 1, 1, 4, 4, -1])

    def test_render(self):
        expected = [
            "##..##..##..##..##..##..##..##..##..##..",
            "###...###...###...###...###...###...###.",
            "####....####....####....####....####....",
            "#####.....#####.....#####.....#####.....",
            "######......######......######......####",
            "#######.......#######.......#######....."
        ]
        self.assertSequenceEqual(execute(self.INSTRUCTIONS).crt, expected)

    def test_execute(self):
        actual = execute(self.INSTRUCTIONS).registry
        self.assertEqual(actual[20], 21)
        self.assertEqual(actual[60], 19)
        self.assertEqual(actual[100], 18)
        self.assertEqual(actual[140], 21)
        self.assertEqual(actual[180], 16)
        self.assertEqual(actual[220], 18)


if __name__ == '__main__':
    instructuions = read_instructions("input.txt")
    result = execute(instructuions)
    score_registry(result.registry)
    for raw in result.crt:
        print(raw)
    unittest.main()
