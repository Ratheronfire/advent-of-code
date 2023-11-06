import math
import re
from typing import List, Union
from puzzle_base import PuzzleBase


class Monkey:
    id: int

    items: List[int]

    operator: str
    operand: Union[int, str]

    divide_test_num: int

    true_monkey: int
    false_monkey: int

    inspect_count = 0

    def __init__(self, id, items, operator, operand, divide_test_num, true_monkey, false_monkey):
        self.id = id

        self.items = items
        self.operator = operator

        self.operand = operand
        self.divide_test_num = divide_test_num

        self.true_monkey = true_monkey
        self.false_monkey = false_monkey


class Puzzle(PuzzleBase):
    year = 2022
    day = 11

    monkeys: List[Monkey] = []
    least_common_multiple = -1

    def reset(self):
        self.monkeys = []
        self.least_common_multiple = -1

    def prepare_data(self, input_data: List[str], current_part: int):
        monkey_lines = ''
        for line in input_data:
            if line != '':
                monkey_lines += line + '\n'
            else:
                self.parse_monkey_data(monkey_lines)
                monkey_lines = ''

        # need the last one, too
        self.parse_monkey_data(monkey_lines)

        divisors = [m.divide_test_num for m in self.monkeys]
        self.least_common_multiple = math.lcm(*divisors)

        for _ in range(20 if current_part == 1 else 10000):
            self.process_turn(current_part)

        self.monkeys = sorted(self.monkeys, key=lambda m: m.inspect_count, reverse=True)

    def parse_monkey_data(self, monkey_data):
        match = re.match(r'Monkey (\d+):\n'
                         r'Starting items: ([\d, ]+)\n'
                         r'Operation: new = old (.) (\d+|old)\n'
                         r'Test: divisible by (\d+)\n'
                         r'If true: throw to monkey (\d+)\n'
                         r'If false: throw to monkey (\d+)', monkey_data)

        if not match:
            return

        monkey = Monkey(int(match[1]),
                        [int(item) for item in match[2].split(', ')],
                        match[3],
                        match[4] if match[4] == 'old' else int(match[4]),
                        int(match[5]),
                        int(match[6]),
                        int(match[7]))

        self.monkeys.append(monkey)

    def process_turn(self, current_part: int):
        for monkey in self.monkeys:
            for item in monkey.items:
                operand = item if monkey.operand == 'old' else monkey.operand
                if monkey.operator == '*':
                    item *= operand

                    if current_part == 2:
                        item %= self.least_common_multiple
                elif monkey.operator == '+':
                    item += operand

                if current_part == 1:
                    item //= 3

                next_monkey_id = monkey.true_monkey if item % monkey.divide_test_num == 0 else monkey.false_monkey
                self.monkeys[next_monkey_id].items.append(item)

                monkey.inspect_count += 1

            monkey.items.clear()

    def get_score(self):
        sorted_monkeys = sorted(self.monkeys, key=lambda m: m.inspect_count, reverse=True)
        return sorted_monkeys[0].inspect_count * sorted_monkeys[1].inspect_count

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.get_score())

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(self.get_score())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
