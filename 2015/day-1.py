from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 1

    movements = ""

    def reset(self):
        self.movements = ""

    def prepare_data(self, input_data: List[str], current_part: int):
        self.movements = input_data[0]

    def navigate(self):
        floor = 0
        for char in self.movements:
            floor += 1 if char == "(" else -1

        return floor

    def navigate_to_basement(self):
        floor = 0
        steps = 0
        for char in self.movements:
            steps += 1
            floor += 1 if char == "(" else -1

            if floor == -1:
                break

        return steps

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.navigate())

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(self.navigate_to_basement())


puzzle = Puzzle()
print(puzzle.test_and_run())
