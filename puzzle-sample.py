from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 0
    day = 1

    sample_data = 0

    def reset(self):
        self.sample_data = 0

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

    def get_day_1_answer(self, use_sample=False) -> str:
        return ''

    def get_day_2_answer(self, use_sample=False) -> str:
        return ''


puzzle = Puzzle()
print(puzzle.test_and_run())
