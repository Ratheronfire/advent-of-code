import math
from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 20

    present_count: int

    def reset(self):
        self.present_count = 0

    def prepare_data(self, input_data: List[str], current_part: int):
        self.present_count = int(input_data[0])

    def presents_at_house(self, house_number: int) -> int:
        presents = 0
        for i in range(house_number, 0, -1):
            if house_number % i == 0:
                presents += i * 10

        return presents

    def is_prime(self, num: int) -> bool:
        square_root = math.sqrt(num)

        for i in range(2, math.ceil(square_root)):
            if num % i == 0:
                return False

        return True

    def get_part_1_answer(self, use_sample=False) -> str:
        i = 0#int(self.present_count / 60)
        presents = self.presents_at_house(i)

        # Starting by finding the lowest multiple of 6 to cross the threshold
        while presents < self.present_count:
            i += 6 ** math.ceil(math.log(i, 10) / 10 if i > 0 else 1)
            presents = self.presents_at_house(i)

        return str(i)

        # now, backing up to find the first prime below the threshold
        while presents > self.present_count or not self.is_prime(i):
            i -= 1
            presents = self.presents_at_house(i)

        # finally, moving forward again to find the true lowest match
        while presents < self.present_count:
            i += 1
            presents = self.presents_at_house(i)

        return str(i)

    def get_part_2_answer(self, use_sample=False) -> str:
        return ''


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
