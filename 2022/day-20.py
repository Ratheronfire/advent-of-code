from copy import deepcopy
from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 20

    numbers: list
    tuples_by_index = {}
    zero_index = -1

    def reset(self):
        self.numbers = []
        self.tuples_by_index = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            number_tuple = (int(line), i)
            self.numbers.append(number_tuple)
            self.tuples_by_index[i] = number_tuple

            if number_tuple[0] == 0:
                self.zero_index = i

    def mix(self):
        for i in range(len(self.numbers)):
            number, original_index = number_tuple = self.tuples_by_index[i]
            current_index = self.numbers.index(number_tuple)
            new_index = (current_index + number) % len(self.numbers)

            if new_index < current_index:
                current_index += 1  # keeping the old index aligned if we're adding an element before it

            self.numbers.insert(new_index, number_tuple)
            self.numbers = self.numbers[:current_index] + self.numbers[current_index + 1:]

    def get_day_1_answer(self, use_sample=False) -> str:
        self.mix()

        coordinates = self.numbers[(self.zero_index + 1000) % len(self.numbers)][0] + \
                      self.numbers[(self.zero_index + 2000) % len(self.numbers)][0] + \
                      self.numbers[(self.zero_index + 3000) % len(self.numbers)][0]
        return str(coordinates)

    def get_day_2_answer(self, use_sample=False) -> str:
        return ''


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
