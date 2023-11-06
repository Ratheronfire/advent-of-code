from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 1

    elves = []

    def reset(self):
        self.elves = []

    def prepare_data(self, input_data: List[str], current_part: int):
        elf_value = 0
        for i in range(len(input_data)):
            line = input_data[i]

            if line != '':
                elf_value += int(line)

            if line == '' or i == len(input_data) - 1:
                self.elves.append(elf_value)
                elf_value = 0

        self.elves = sorted(self.elves)

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.elves[-1])

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(sum(self.elves[-3:]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
