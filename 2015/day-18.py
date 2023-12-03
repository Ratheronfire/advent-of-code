from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 18

    grid: Grid

    def reset(self):
        self.grid = Grid.create_empty(0, 0)

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = Grid.from_strings(input_data)

    def step(self):
        next_grid = Grid.create_empty(self.grid.width, self.grid.height, '.')

        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                point = Point(x, y)
                neighbors = self.grid.neighbors(point, True)

                total_on = len([n for n in neighbors if n[1] == '#'])

                state = self.grid[point]

                if state == '#':
                    new_state = '#' if total_on == 2 or total_on == 3 else '.'
                else:
                    new_state = '#' if total_on == 3 else '.'

                next_grid[point] = new_state

        self.grid = next_grid

    def lock_corners(self):
        self.grid[(0, 0)] = '#'
        self.grid[(0, self.grid.height - 1)] = '#'
        self.grid[(self.grid.width - 1, 0)] = '#'
        self.grid[(self.grid.width - 1, self.grid.height - 1)] = '#'

    def get_day_1_answer(self, use_sample=False) -> str:
        for i in range(100):
            self.step()

        return str(len([p for p in self.grid.grid.keys() if self.grid[p] == '#']))

    def get_day_2_answer(self, use_sample=False) -> str:
        for i in range(100):
            self.lock_corners()
            self.step()
            self.lock_corners()

        return str(len([p for p in self.grid.grid.keys() if self.grid[p] == '#']))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
