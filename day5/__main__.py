from dataclasses import dataclass
from os import path
import unittest


@dataclass
class Command:
    amount: int
    source: int
    target: int


def parse_state(lines):
    value_lines = lines[:-1]
    numbers_line = lines[-1]
    number = len(numbers_line.split())
    state = []
    for i in range(number):
        state.append([])
    for line in reversed(value_lines):
        for i in range(number):
            pos = 4 * i + 1
            value = line[pos]
            if value != ' ':
                state[i].append(value)
    return state


def parse_commands(lines):
    for line in lines:
        parts = line.split()
        yield Command(int(parts[1]), int(parts[3]) - 1, int(parts[5]) - 1)


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def separate_state_and_command_lines(lines):
    state = []
    commands = []
    commands_mode = False
    for line in lines:
        if len(line.strip()) == 0:
            commands_mode = True
        elif commands_mode:
            commands.append(line)
        else:
            state.append(line)
    return state, commands


def apply_commands_9000(state, commands):
    for command in commands:
        for _ in range(command.amount):
            state[command.target].append(state[command.source].pop())


def apply_commands_9001(state, commands):
    for command in commands:
        source = state[command.source]
        moved = source[-command.amount:]
        state[command.source] = state[command.source][:-command.amount]
        state[command.target].extend(moved)


def string_of_tops(state):
    return "".join(map(lambda s: s[-1], state))


def solve_file(fname):
    lines = read_lines(fname)
    state_lines, command_lines = separate_state_and_command_lines(lines)
    commands = list(parse_commands(command_lines))

    state_9000 = parse_state(state_lines)
    state_9001 = [s.copy() for s in state_9000]
    apply_commands_9000(state_9000, commands)
    apply_commands_9001(state_9001, commands)
    tops9000 = string_of_tops(state_9000)
    tops9001 = string_of_tops(state_9001)

    return tops9000, tops9001


class TestDay(unittest.TestCase):

    def test_parse_state(self):
        lines = read_lines("input-test.txt")
        state_lines, _ = separate_state_and_command_lines(lines)
        actual = parse_state(state_lines)
        expected = [['Z', 'N'], ['M', 'C', 'D'], ['P']]
        self.assertEqual(actual, expected)

    def test_parse_commands(self):
        lines = read_lines("input-test.txt")
        _, command_lines = separate_state_and_command_lines(lines)
        actual = list(parse_commands(command_lines))
        expected = [Command(1, 1, 0), Command(3, 0, 2),  Command(2, 1, 0), Command(1, 0, 1)]
        self.assertEqual(actual, expected)

    def test_apply_commands_9000(self):
        state = [['Z', 'N'], ['M', 'C', 'D'], ['P']]
        commands = [Command(1, 1, 0), Command(3, 0, 2), Command(2, 1, 0), Command(1, 0, 1)]
        expected = [['C'], ['M'], ['P', 'D', 'N', 'Z']]
        apply_commands_9000(state, commands)
        self.assertEqual(state, expected)

    def test_apply_commands_9001(self):
        state = [['Z', 'N'], ['M', 'C', 'D'], ['P']]
        commands = [Command(1, 1, 0), Command(3, 0, 2), Command(2, 1, 0), Command(1, 0, 1)]
        expected = [['M'], ['C'], ['P', 'Z', 'N', 'D']]
        apply_commands_9001(state, commands)
        self.assertEqual(state, expected)

    def test_string_of_tops(self):
        state = [['C'], ['M'], ['P', 'D', 'N', 'Z']]
        self.assertEqual(string_of_tops(state), "CMZ")

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), ("CMZ", "MCD"))


if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()
