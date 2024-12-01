from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2024
    day = 1

    left_list = []
    right_list = []

    def reset(self):
        self.left_list = []
        self.right_list = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]
            if line == '':
                continue

            nums = line.split(' ')
            self.left_list.append(int(nums[0]))
            self.right_list.append(int(nums[-1]))

    def get_part_1_answer(self, use_sample=False) -> str:
        total = 0

        self.left_list.sort(reverse=True)
        self.right_list.sort(reverse=True)

        while len(self.left_list) > 0 and len(self.right_list) > 0:
            min_left = self.left_list.pop()
            min_right = self.right_list.pop()

            total += abs(min_left - min_right)

        return str(total)

    def get_part_2_answer(self, use_sample=False) -> str:
        total = 0

        right_counts = {}

        for num in self.right_list:
            if num in right_counts:
                right_counts[num] = right_counts[num] + 1
            else:
                right_counts[num] = 1

        for num in self.left_list:
            if num in right_counts:
                total += num * right_counts[num]

        return str(total)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
