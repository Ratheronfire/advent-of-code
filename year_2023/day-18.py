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

    vertices: list[Point]

    def reset(self):
        self.vertices = []

    def prepare_data(self, input_data: List[str], current_part: int):
        current_point = Point(0, 0)

        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            direction, steps, color = line.split()

            if current_part == 2:
                steps = int(color[2:-2], 16)
                direction = color[-2:-1]

            current_point += DIRECTIONS[direction] * int(steps)
            self.vertices.append(current_point)

    def get_inside_count(self):
        is_inside = False
        last_corner_was_up = None

        inside_tiles = 0

        ys = list(sorted(set([vertex.y for vertex in self.vertices])))
        ys += [ys[0] + 1] + [y - 1 for y in ys[1:-1]] + [y + 1 for y in ys[1:-1]] + [ys[-1] - 1]
        ys = sorted(set(ys))

        lines = [sorted([self.vertices[i-1], self.vertices[i]], key=lambda p: (p.y, p.x))
                 for i in range(len(self.vertices))]
        lines = sorted(lines, key=lambda l: l[0].x + l[1].x)

        for i, y in enumerate(ys):
            tiles_this_line = 0

            is_inside = False
            overlaps = [line for line in lines if line[0].y <= y <= line[1].y or
                                                  line[1].y <= y <= line[0].y]

            for j, overlap in enumerate(overlaps):
                if overlap[0].x == overlap[1].x:
                    # vertical line
                    tiles_this_line += 1
                    # print(f'Adding tile for vertical line {overlap[0]}->{overlap[1]}.')

                    if y in [overlap[0].y, overlap[1].y]:
                        line_end = overlap[1].y if overlap[0].y == y else overlap[0].y
                        corner_is_up = line_end < y

                        if last_corner_was_up is None:
                            last_corner_was_up = corner_is_up
                        else:
                            if last_corner_was_up != corner_is_up:
                                is_inside = not is_inside
                            last_corner_was_up = None
                    else:
                        is_inside = not is_inside

                    if is_inside and j <= len(overlaps) - 2:
                        next_overlap = overlaps[j+1]
                        if overlap[0].x == overlap[1].x and \
                            next_overlap[0].x == next_overlap[1].x:
                            # inbetween two vertical lines
                            tiles_this_line += abs(next_overlap[0].x - overlap[0].x) - 1
                            # print(f'Adding gap between x={overlap[0].x}->{next_overlap[0].x} at y={y}.')
                else:
                    # horizontal line
                    tiles_this_line += abs(overlap[1].x - overlap[0].x) - 1
                    # print(f'Adding line from x={overlap[0].x}->{overlap[1].x} at y={y}.')

            if i <= len(ys) - 2:
                y_gap = max(1, abs(ys[i+1] - ys[i]))
                # print(f'Repeating last row {y_gap} times => {tiles_this_line} * {y_gap} = {tiles_this_line * y_gap} tiles.\n')
                inside_tiles += tiles_this_line * y_gap
            else:
                # print(f'Adding final row.')
                inside_tiles += tiles_this_line

        return inside_tiles

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.get_inside_count())

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.get_inside_count())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
