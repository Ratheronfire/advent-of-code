import math
from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2023
    day = 11

    grid: Grid
    galaxies: list[Point]

    def reset(self):
        self.grid = Grid.create_empty(0, 0, '.')
        self.galaxies = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = Grid.from_strings(input_data)

    def expand(self, expansion_amount: int):
        empty_xs = [x for x in range(self.grid.width) if
                    '#' not in str(self.grid[(x, 0):(x, self.grid.height):(1, 1)])]
        empty_ys = [y for y in range(self.grid.height) if
                    '#' not in str(self.grid[(0, y):(self.grid.width, y):(1, 1)])]

        expanded_grid = Grid.create_empty(self.grid.width + len(empty_xs), self.grid.height + len(empty_ys), '.')

        ex, ey = 0, 0

        for x in range(self.grid.extents[0][1] + 1 + len(empty_xs)):
            if x in empty_xs:
                ex += expansion_amount

            for y in range(self.grid.extents[1][1] + 1 + len(empty_ys)):
                if y in empty_ys:
                    ey += expansion_amount
                expanded_grid[(ex, ey)] = self.grid[(x, y)]

                if self.grid[(x, y)] == '#':
                    self.galaxies.append(Point(ex, ey))
                    expanded_grid[(ex, ey)] = str(len(self.galaxies))

                ey += 1

            ex += 1
            ey = 0

        self.grid = expanded_grid

    def get_distances(self):
        total = 0

        for i in range(len(self.galaxies)):
            for j in range(i+1, len(self.galaxies)):
                start = self.galaxies[i]
                end = self.galaxies[j]

                total += abs(start.x - end.x) + abs(start.y - end.y)

        return total

    def get_part_1_answer(self, use_sample=False) -> str:
        self.expand(1)
        return str(self.get_distances())

    def get_part_2_answer(self, use_sample=False) -> str:
        self.expand(999999)
        return str(self.get_distances())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
