import copy
import re


from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 5

    should_strip_data = False

    stacks_built = False
    stack_lines = []
    moves = []

    stacks = []

    def reset(self):
        self.stacks_built = False
        self.stack_lines = []
        self.moves = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '\n' or line == '':
                continue

            if not self.stacks_built and line[1] == '1':
                self.stacks = self.build_stack(self.stack_lines)
                self.stacks_built = True
                continue
            elif not self.stacks_built:
                self.stack_lines.append(line)
                continue

            self.moves.append([int(match) for match in re.findall('\\d+', line)])

        for move in self.moves:
            count = move[0]
            first = move[1] - 1
            second = move[2] - 1

            if current_part == 1:
                for i in range(count):
                    char = self.stacks[first].pop()
                    self.stacks[second].append(char)
            elif current_part == 2:
                chars = self.stacks[first][-count:]

                self.stacks[first] = self.stacks[first][:-count]
                self.stacks[second] += chars

    def get_part_1_answer(self, use_sample=False) -> str:
        return ''.join([s[-1] for s in self.stacks])

    def get_part_2_answer(self, use_sample=False) -> str:
        return ''.join([s[-1] for s in self.stacks])

    @staticmethod
    def build_stack(lines):
        stacks = [[] for i in range((len(lines[0]) + 1) // 4)]

        for line in lines:
            stack_index = 0
            for i in range(0, len(line), 4):
                if line[i] == '[':
                    stacks[stack_index].append(line[i+1])

                stack_index += 1

        return [s[::-1] for s in stacks]


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
