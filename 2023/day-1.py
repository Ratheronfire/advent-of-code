from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2023
    day = 1

    lines: list[str]

    def reset(self):
        self.lines = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.lines = [l for l in input_data if l != '']

    def fix_num_strs(self, line):
        digit_strs = [
            'one', 'two', 'three', 'four', 'five',
            'six', 'seven', 'eight', 'nine', 'ten', 'zero'
        ]

        found_first = False
        found_last = False

        for i in range(len(line)):
            if found_first or line[i].isnumeric():
                break  # found a real number first

            for digit in digit_strs:
                if line[i:i+len(digit)] == digit:
                    line = line[:i] + str(digit_strs.index(digit) + 1) + line[i+len(digit):]
                    found_first = True
                    break

        for i in range(len(line) - 1, -1, -1):
            if found_last or line[i].isnumeric():
                break  # found a real number first

            for digit in digit_strs:
                if line[i-len(digit)+1:i+1] == digit:
                    line = line[:i-len(digit)+1] + str(digit_strs.index(digit) + 1) + line[i+1:]
                    found_last = True
                    break

        return line

    def get_nums(self, line: str):
        first, last = '', ''

        for i in range(len(line)):
            if first == '' and line[i].isnumeric():
                first = line[i]

            if last == '' and line[len(line) - 1 - i].isnumeric():
                last = line[len(line) - 1 - i]

        return int(first + last)

    def get_part_1_answer(self, use_sample=False) -> str:
        sum = 0

        for line in self.lines:
            line_num = self.get_nums(line)

            sum += line_num

        return str(sum)

    def get_part_2_answer(self, use_sample=False) -> str:
        sum = 0

        for line in self.lines:
            line_num = self.get_nums(self.fix_num_strs(line))

            sum += line_num

        return str(sum)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
