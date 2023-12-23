from typing import List

from helpers.grid import ArrayGrid, Point, Grid, SparseGrid
from puzzle_base import PuzzleBase

DIRECTIONS = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
    '0': Point(1, 0),
    '1': Point(0, 1),
    '2': Point(-1, 0),
    '3': Point(0, -1),
}


class DigInstruction:
    def __init__(self, direction: str, steps: int, color: str):
        self.direction = DIRECTIONS[direction]
        self.steps = steps

        self.true_steps = int(color[:-1], 16)
        self.true_direction = DIRECTIONS[color[-1]]


class Puzzle(PuzzleBase):
    year = 2023
    day = 18

    grid: Grid
    dig_plan: list[DigInstruction]
    last_pos: Point

    def reset(self):
        self.grid = SparseGrid.create_empty(0, 0, '.')
        self.dig_plan = []

        self.last_pos = Point(0, 0)

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            direction, steps, color = line.split()
            self.dig_plan.append(DigInstruction(
                direction, int(steps), color[2:-1]
            ))

    def dig(self, dig_instruction: DigInstruction, true_instruction=False):
        for i in range(dig_instruction.true_steps if true_instruction else dig_instruction.steps):
            self.grid[self.last_pos] = '#'
            self.last_pos = self.last_pos + \
                            (dig_instruction.true_direction
                             if true_instruction else
                             dig_instruction.direction)

    def get_inside_count(self):
        is_inside = False
        last_corner_was_up = None

        inside_tiles = 0

        for point in self.grid.points():
            tile = self.grid[point]

            if tile == '#':
                tile_above = self.grid[point + Point(0, -1)]
                tile_below = self.grid[point + Point(0, 1)]

                if last_corner_was_up is not None and self.grid[point + Point(1, 0)] == '#':
                    continue

                if tile_above == '#' and tile_below == '#':
                    is_inside = not is_inside
                elif tile_below != '#':
                    if last_corner_was_up is None:
                        last_corner_was_up = True
                    elif not last_corner_was_up:
                        is_inside = not is_inside
                elif tile_above != '#':
                    if last_corner_was_up is None:
                        last_corner_was_up = False
                    elif last_corner_was_up:
                        is_inside = not is_inside
            else:
                last_corner_was_up = None

                if is_inside:
                    inside_tiles += 1

            if point.x == self.grid.extents[0][1]:
                is_inside = False

        return inside_tiles

    def get_part_1_answer(self, use_sample=False) -> str:
        for dig_instruction in self.dig_plan:
            self.dig(dig_instruction)

        inside_tiles = self.get_inside_count()

        return str(inside_tiles + len([i for i in self.grid.grid.keys() if self.grid[i] == '#']))

    def get_part_2_answer(self, use_sample=False) -> str:
        for dig_instruction in self.dig_plan:
            self.dig(dig_instruction, True)

        inside_tiles = self.get_inside_count()

        return str(inside_tiles + len([i for i in self.grid.grid.keys() if self.grid[i] == '#']))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
