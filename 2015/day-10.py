from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 10

    base_input = ''

    def reset(self):
        self.base_input = ''

    def prepare_data(self, input_data: List[str], current_part: int):
        self.base_input = input_data[0]

    def look_and_say(self, input: str):
        output = ''

        repeats_found = 1

        for i in range(len(input)):
            number = input[i]
            if i == len(input) - 1 or input[i + 1] != number:
                output += str(repeats_found) + number
                repeats_found = 1
            else:
                repeats_found += 1

        return output

    def get_part_1_answer(self, use_sample=False) -> str:
        input = self.base_input

        for i in range(40):
            input = self.look_and_say(input)

        return str(len(input))

    def get_part_2_answer(self, use_sample=False) -> str:
        input = self.base_input

        for i in range(50):
            input = self.look_and_say(input)

        return str(len(input))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
