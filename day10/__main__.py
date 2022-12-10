
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

def parse_instruction(string):
    parts = string.split()
    if parts[0] == "noop":
        return Noop()
    return Add(int(parts[1]))

def execute(instructions):
    states = [1, 1]
    last  = 1
    for instruction in instructions:
        states.append(last)
        if isinstance(instruction, Add):
            new_value = last + instruction.value
            states.append(new_value)
            last = new_value
    return states

def score_results(results):
    """(that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles)"""
    return sum(p * results[p] for p in [20, 60, 100, 140, 180, 220])

def read_instructions(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for s in file:
            yield parse_instruction(s)

def score_file(fname):
    instructuions = read_instructions(fname)
    results = execute(instructuions)
    return score_results(results)

class TestDay(unittest.TestCase):

    COMMANDS = read_instructions("input-test.txt")

    def test_execute_small(self):
        """
        At the start of the first cycle, the noop instruction begins execution. During the first cycle, X is 1. After the first cycle, the noop instruction finishes execution, doing nothing.
        At the start of the second cycle, the addx 3 instruction begins execution. During the second cycle, X is still 1.
        During the third cycle, X is still 1. After the third cycle, the addx 3 instruction finishes execution, setting X to 4.
        At the start of the fourth cycle, the addx -5 instruction begins execution. During the fourth cycle, X is still 4.
        During the fifth cycle, X is still 4. After the fifth cycle, the addx -5 instruction finishes execution, setting X to -1.
        """
        actual = execute([Noop(), Add(3),  Add(-5)])
        #                                 0, 1, 2, 3, 4, 5  
        self.assertSequenceEqual(actual, [1, 1, 1, 1, 4, 4, -1])


    def test_execute(self):
        actual = execute(self.COMMANDS)
        self.assertEqual(actual[20], 21)
        self.assertEqual(actual[60], 19)
        self.assertEqual(actual[100], 18)
        self.assertEqual(actual[140], 21)
        self.assertEqual(actual[180], 16)
        self.assertEqual(actual[220], 18)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), 13140)

if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()