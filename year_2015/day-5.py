from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 5

    lines: list[str]

    def reset(self):
        self.lines = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.lines = [line for line in input_data if len(line) > 0]

    def is_nice(self, line: str):
        vowels_found = 0
        repeat_found = False

        for i in range(0, len(line)):
            if line[i] in 'aeiou':
                vowels_found += 1
            if i < len(line) - 1 and line[i] == line[i + 1]:
                repeat_found = True

        bad_strs = [bad_str for bad_str in ['ab', 'cd', 'pq', 'xy'] if bad_str in line]

        return vowels_found >= 3 and repeat_found and len(bad_strs) == 0

    def is_nice_2(self, line: str):
        repeat_pair_found = False
        spaced_pair_found = False

        for i in range(0, len(line)):
            for j in range(i + 2, len(line) - 1):
                if i < len(line) - 1 and line[i:i+2] == line[j:j+2]:
                    repeat_pair_found = True

            if i < len(line) - 2 and line[i] == line[i + 2]:
                spaced_pair_found = True

        return repeat_pair_found and spaced_pair_found

    def get_part_1_answer(self, use_sample=False) -> str:
        nice_lines = len([line for line in self.lines if self.is_nice(line)])
        return str(nice_lines)

    def get_part_2_answer(self, use_sample=False) -> str:
        nice_lines = len([line for line in self.lines if self.is_nice_2(line)])
        return str(nice_lines)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
