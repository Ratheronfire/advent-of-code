from typing import List

from puzzle_base import PuzzleBase


# My solution for part 1.
# def is_safe_record(report: list[int]) -> bool:
#     ascending = report[1] > report[0]
#
#     for i in range(1, len(report)):
#         a, b = report[i], report[i-1]
#         if (a > b) != ascending or abs(a - b) > 3 or a == b:
#             return False
#
#     return True


def is_safe_record(report: list[int], allow_removal=False) -> bool:
    ascending = report[1] > report[0]

    is_safe = True

    for i in range(1, len(report)):
        a, b = report[i], report[i-1]
        if (a > b) != ascending or abs(a - b) > 3 or a == b:
            is_safe = False

    if not is_safe and allow_removal:
        for i in range(len(report)):
            if is_safe_record(report[0:i] + report[i+1:]):
                is_safe = True

    return is_safe


class Puzzle(PuzzleBase):
    year = 2024
    day = 2

    reports = []

    def reset(self):
        self.reports = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line != '':
                self.reports.append([int(n) for n in line.split(' ')])

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(sum([1 for report in self.reports if is_safe_record(report, False)]))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(sum([1 for report in self.reports if is_safe_record(report, True)]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
