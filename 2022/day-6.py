from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):

    year = 2022
    day = 6

    line: str

    def reset(self):
        pass

    def prepare_data(self, input_data: List[str], current_part: int):
        self.line = input_data[0]

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(get_message_start_point(self.line, 4))

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(get_message_start_point(self.line, 14))


def get_message_start_point(input_line, unique_char_count):
    recent_chars = []
    index = 0

    for char in input_line:
        if len(recent_chars) >= unique_char_count:
            recent_chars = recent_chars[1:]

        recent_chars += char

        if len(set(recent_chars)) == unique_char_count:
            return index + 1

        index += 1


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())

