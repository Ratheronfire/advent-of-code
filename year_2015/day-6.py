import re
from enum import Enum
from typing import List

from helpers.grid import Point, Grid
from puzzle_base import PuzzleBase


class Instruction:
    class InstructionTypes(Enum):
        TOGGLE = 0,
        ON = 1,
        OFF = 2

    type: InstructionTypes
    point_min: Point
    point_max: Point

    def __init__(self, instruction_type: InstructionTypes, x_min, y_min, x_max, y_max):
        self.type = instruction_type
        self.point_min = Point(int(x_min), int(y_min))
        self.point_max = Point(int(x_max), int(y_max))


class Puzzle(PuzzleBase):
    year = 2015
    day = 6

    instructions: List[Instruction]
    grid: Grid

    def reset(self):
        self.instructions = []
        self.grid = Grid.create_empty(1000, 1000, 0)

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            parts = re.split(r'(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)', input_data[i])
            if len(parts) < 6:
                continue

            instruction_type = Instruction.InstructionTypes.TOGGLE
            if parts[1] == 'toggle':
                instruction_type = Instruction.InstructionTypes.TOGGLE
            elif parts[1] == 'turn on':
                instruction_type = Instruction.InstructionTypes.ON
            elif parts[1] == 'turn off':
                instruction_type = Instruction.InstructionTypes.OFF

            instruction = Instruction(instruction_type, parts[2], parts[3], parts[4], parts[5])
            self.instructions.append(instruction)

    def do_instruction(self, instruction: Instruction):
        for x in range(instruction.point_min.x, instruction.point_max.x + 1):
            for y in range(instruction.point_min.y, instruction.point_max.y + 1):
                if instruction.type == Instruction.InstructionTypes.TOGGLE:
                    self.grid[(x, y)] = 1 if self.grid[(x, y)] == 0 else 0
                elif instruction.type == Instruction.InstructionTypes.ON:
                    self.grid[(x, y)] = 1
                elif instruction.type == Instruction.InstructionTypes.OFF:
                    self.grid[(x, y)] = 0

    def do_instruction_2(self, instruction: Instruction):
        for x in range(instruction.point_min.x, instruction.point_max.x + 1):
            for y in range(instruction.point_min.y, instruction.point_max.y + 1):
                if instruction.type == Instruction.InstructionTypes.TOGGLE:
                    self.grid[(x, y)] = self.grid[(x, y)] + 2
                elif instruction.type == Instruction.InstructionTypes.ON:
                    self.grid[(x, y)] = self.grid[(x, y)] + 1
                elif instruction.type == Instruction.InstructionTypes.OFF:
                    self.grid[(x, y)] = self.grid[(x, y)] - 1

                if self.grid[(x, y)] < 0:
                    self.grid[(x, y)] = 0

    def get_total_brightness(self):
        total = 0

        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                total += self.grid[(x, y)]

        return total

    def get_part_1_answer(self, use_sample=False) -> str:
        for i in range(len(self.instructions)):
            self.do_instruction(self.instructions[i])

        return str(self.get_total_brightness())

    def get_part_2_answer(self, use_sample=False) -> str:
        for i in range(len(self.instructions)):
            self.do_instruction_2(self.instructions[i])

        return str(self.get_total_brightness())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
