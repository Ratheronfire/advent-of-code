from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2023
    day = 9

    value_sets: list[list[int]]

    def reset(self):
        self.value_sets = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]
            if line != '':
                self.value_sets.append([int(i) for i in line.split()])

    def get_next_value(self, value_set: list[int]):
        edge_values = [value_set[-1]]

        derivative_values = []

        while not all([v == 0 for v in value_set]):
            for i in range(len(value_set) - 1):
                derivative_values.append(value_set[i + 1] - value_set[i])

            value_set = derivative_values.copy()
            derivative_values = []

            edge_values.append(value_set[-1])

        return sum(edge_values)

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(sum([self.get_next_value(v) for v in self.value_sets]))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(sum([self.get_next_value(v[::-1]) for v in self.value_sets]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
