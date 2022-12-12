from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 4

    redundant_pairs = 0
    overlap_pairs = 0

    def reset(self):
        self.redundant_pairs = 0
        self.overlap_pairs = 0

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i].strip()

            if line == '':
                continue

            ranges = [[int(i) for i in r.split('-')] for r in line.strip().split(',')]

            if (ranges[0][0] >= ranges[1][0] and ranges[0][1] <= ranges[1][1]) or \
                    (ranges[1][0] >= ranges[0][0] and ranges[1][1] <= ranges[0][1]):
                self.redundant_pairs += 1

            if ranges[1][0] <= ranges[0][0] <= ranges[1][1] or ranges[0][0] <= ranges[1][0] <= ranges[0][1]:
                self.overlap_pairs += 1

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.redundant_pairs)

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(self.overlap_pairs)


puzzle = Puzzle()
print(puzzle.test_and_run())
