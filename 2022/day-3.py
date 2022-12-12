from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 3

    total = 0
    group_total = 0

    group = []

    def reset(self):
        self.total = 0
        self.group_total = 0

        self.group = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i].strip()

            if line == '':
                continue

            midpoint = len(line) // 2
            sacks = line[:midpoint], line[midpoint:]

            self.total += self.get_matching_item_priority(sacks)

            self.group.append(line)
            if len(self.group) == 3:
                self.group_total += self.get_matching_item_priority(self.group)
                self.group = []

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.total)

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(self.group_total)

    @staticmethod
    def get_matching_item_priority(sacks):
        repeat = None

        for item in sacks[0]:
            if all([item in s for s in sacks[1:]]):
                repeat = item
                break

        return ord(repeat) - (96 if repeat.islower() else 38)


puzzle = Puzzle()
print(puzzle.test_and_run())
