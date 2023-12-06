from hashlib import md5
from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 4

    key: str

    def reset(self):
        self.key = ''

    def prepare_data(self, input_data: List[str], current_part: int):
        self.key = input_data[0]

    def hash(self, number):
        key = (self.key + str(number)).encode()
        return md5(key).hexdigest()

    def get_part_1_answer(self, use_sample=False) -> str:
        i = 1

        while True:
            hash = self.hash(i)

            if hash[:5] == "00000":
                break

            i += 1

        return str(i)

    def get_part_2_answer(self, use_sample=False) -> str:
        i = 1

        while True:
            hash = self.hash(i)

            if hash[:6] == "000000":
                break

            i += 1

        return str(i)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
