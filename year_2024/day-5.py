import math
from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2024
    day = 5

    order_rules: list[tuple]
    updates: list

    def reset(self):
        self.order_rules = []
        self.updates = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.order_rules = []
        self.updates = []

        is_parsing_rules = True

        for i in range(len(input_data)):
            line = input_data[i]

            if line == "":
                is_parsing_rules = False
                continue

            if is_parsing_rules:
                nums = line.split('|')
                self.order_rules.append((int(nums[0]), int(nums[1])))
            else:
                nums = line.split(',')
                self.updates.append([int(i) for i in nums])

    def get_rules_for_update(self, update: list[int]) -> list[tuple]:
        rules = []

        for rule in self.order_rules:
            if rule[0] in update and rule[1] in update:
                rules.append(rule)

        return rules

    def is_rule_valid(self, update: list[int], rule: tuple) -> bool:
        if not rule[0] in update or not rule[1] in update:
            return True

        left_index = update.index(rule[0])
        right_index = update.index(rule[1])

        return left_index < right_index

    def is_update_valid(self, update: list[int]):
        return all([self.is_rule_valid(update, r) for r in self.get_rules_for_update(update)])

    def get_fixed_ordering(self, update: list[int]) -> list[int]:
        rules = self.get_rules_for_update(update)

        new_list = []

        while len(rules):
            lowers = [rule[0] for rule in rules]
            highers = [rule[1] for rule in rules]

            lowest = [low for low in lowers if low not in highers][0]

            new_list.append(lowest)

            if len(rules) == 1:
                new_list.append(rules[0][1])
            rules = [rule for rule in rules if rule[0] != lowest]

        return new_list

    def get_part_1_answer(self, use_sample=False) -> str:
        valid_updates = [u for u in self.updates if self.is_update_valid(u)]

        return str(sum([u[math.floor(len(u) / 2.0)] for u in valid_updates]))

    def get_part_2_answer(self, use_sample=False) -> str:
        invalid_updates = [u for u in self.updates if not self.is_update_valid(u)]

        sum = 0

        for update in invalid_updates:
            update = self.get_fixed_ordering(update)

            midpoint = math.floor(len(update) / 2.0)
            sum += update[midpoint]

        return str(sum)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
