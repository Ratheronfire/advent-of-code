import json
from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 12

    json_data = []

    def reset(self):
        self.json_data = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.json_data = json.loads(input_data[0])

    def reduce_to_number(self, json_segment, ignore_red=False) -> int:
        if isinstance(json_segment, int):
            return json_segment

        if isinstance(json_segment, list):
            list_nums = [self.reduce_to_number(child, ignore_red) for child in json_segment]

            return sum(list_nums)

        if isinstance(json_segment, dict):
            if ignore_red and "red" in json_segment.values():
                return 0

            dict_nums = [self.reduce_to_number(child, ignore_red) for child in json_segment.values()]

            return sum(dict_nums)

        return 0

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.reduce_to_number(self.json_data, False))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.reduce_to_number(self.json_data, True))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
