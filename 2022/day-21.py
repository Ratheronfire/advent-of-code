from typing import List, Union
import re

import numpy

from puzzle_base import PuzzleBase


class Monkey:
    id: str

    left_id: str = None
    right_id: str = None
    operation: str = None

    value: Union[int, str] = None

    def __str__(self):
        if self.value is not None:
            return '%s: %f' % (self.id, self.value)

        return '%s: %s %s %s' % (self.id, self.left_id, self.operation, self.right_id)


class Puzzle(PuzzleBase):
    year = 2022
    day = 21

    monkeys: dict[str, Monkey] = {}

    def reset(self):
        self.monkeys = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i].strip()

            if line == '':
                continue

            parts = line.split(' ')

            monkey = Monkey()
            monkey.id = parts[0][:-1]

            if len(parts) == 2:
                monkey.value = float(parts[1])
            else:
                monkey.left_id = parts[1]
                monkey.operation = parts[2]
                monkey.right_id = parts[3]

            self.monkeys[parts[0][:-1]] = monkey

    def get_monkey_value(self, monkey_id):
        monkey = self.monkeys[monkey_id]

        if monkey.value is not None:
            return monkey.value
        else:
            left_value = self.get_monkey_value(monkey.left_id)
            right_value = self.get_monkey_value(monkey.right_id)

            if left_value == 'x':
                left_value = ['x']
            elif right_value == 'x':
                right_value = ['x']

            if isinstance(left_value, list) or isinstance(right_value, list):
                if not isinstance(left_value, list):
                    left_value = [left_value]
                if not isinstance(right_value, list):
                    right_value = [right_value]

                if monkey.id == 'root':
                    # string_representation = '%s %s =' % (str(left_value), str(right_value))
                    representation = left_value + ['='] + right_value
                else:
                    # string_representation = '%s %s %s' % (str(left_value), str(right_value), monkey.operation)
                    representation = ['('] + left_value + [monkey.operation] + right_value + [')']

                return representation

            if monkey.operation == '+':
                return left_value + right_value
            elif monkey.operation == '-':
                return left_value - right_value
            elif monkey.operation == '*':
                return left_value * right_value
            elif monkey.operation == '/':
                return left_value / right_value

            return -1

    def parse_tree(self, monkey_id='root'):
        monkey = self.monkeys[monkey_id]

        if monkey.value:
            return monkey.value

        if monkey_id == 'root':
            right_side = self.parse_tree(monkey.right_id)
            left_side = self.parse_tree(monkey.left_id)

            if isinstance(left_side, float):
                tmp = right_side
                right_side = left_side
                left_side = tmp

            while len(left_side) > 1:
                remainder, operation, number, x_on_left = left_side
                left_side = remainder

                if operation == '+':
                    right_side -= number
                elif operation == '-':
                    if x_on_left:
                        right_side += number
                    else:
                        right_side = number - right_side
                elif operation == '*':
                    right_side /= number
                elif operation == '/':
                    if x_on_left:
                        right_side *= number
                    else:
                        # inverting 1/x by dividing the numerator by the right hand side
                        right_side = number / right_side

            return right_side

        left_monkey = self.monkeys[monkey.left_id]
        right_monkey = self.monkeys[monkey.right_id]

        if not left_monkey.value:
            left_monkey.value = self.parse_tree(left_monkey.id)
        if not right_monkey.value:
            right_monkey.value = self.parse_tree(right_monkey.id)

        if isinstance(left_monkey.value, list):
            return [left_monkey.value, monkey.operation, right_monkey.value, True]
        elif isinstance(right_monkey.value, list):
            return [right_monkey.value, monkey.operation, left_monkey.value, False]

        if monkey.operation == '+':
            return left_monkey.value + right_monkey.value
        elif monkey.operation == '-':
            return left_monkey.value - right_monkey.value
        elif monkey.operation == '*':
            return left_monkey.value * right_monkey.value
        else:
            return left_monkey.value / right_monkey.value

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(int(self.get_monkey_value('root')))

    def get_part_2_answer(self, use_sample=False) -> str:
        self.monkeys['humn'].value = ['x']

        solution = int(self.parse_tree('root'))

        return str(solution)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
