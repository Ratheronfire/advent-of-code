import functools
import re
from typing import List

from puzzle_base import PuzzleBase


class Function:
    command: str
    variables: list

    def __init__(self, command: str, variables: list):
        self.command = command
        self.variables = variables

    def run(self):
        if self.command == "mul":
            return functools.reduce(lambda a, b: a*b, [int(v) for v in self.variables])


class Puzzle(PuzzleBase):
    year = 2024
    day = 3

    program_memory = ""

    def reset(self):
        self.program_memory = ""

    def prepare_data(self, input_data: List[str], current_part: int):
        self.program_memory = "\n".join(input_data)

    def get_matching_functions(self, function_names: list[str]) -> list[Function]:
        regex = r"(%s)\(((\d+), ?(\d+))?\)" % "|".join(function_names)
        pattern = re.compile(regex)

        matches = pattern.findall(self.program_memory)
        return [Function(m[0], m[2:]) for m in matches]

    def get_part_1_answer(self, use_sample=False) -> str:
        functions = self.get_matching_functions(["mul"])
        return str(sum([f.run() for f in functions]))

    def get_part_2_answer(self, use_sample=False) -> str:
        functions = self.get_matching_functions(["mul", "do", "don't"])

        sum = 0
        active = True
        for function in functions:
            if function.command == "do":
                active = True
            elif function.command == "don't":
                active = False
            elif function.command == "mul" and active:
                sum += function.run()

        return str(sum)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
