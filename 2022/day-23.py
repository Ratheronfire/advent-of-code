from copy import deepcopy
from typing import List

from helpers.grid import Grid
from puzzle_base import PuzzleBase


DEFAULT_MOVEMENTS = [
    [(0, -1), (-1, -1), (1, -1)],
    [(0, 1), (-1, 1), (1, 1)],
    [(-1, 0), (-1, -1), (-1, 1)],
    [(1, 0), (1, -1), (1, 1)]
]


class Puzzle(PuzzleBase):
    year = 2022
    day = 23

    grid: Grid
    movement_desires: Grid

    movements = DEFAULT_MOVEMENTS

    def reset(self):
        self.movements = DEFAULT_MOVEMENTS

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = Grid.from_strings(input_data)

    def select_movements(self):
        self.movement_desires = Grid.create_empty(0, 0, None)

        x_extents, y_extents = self.grid.extents

        for y in range(y_extents[0], y_extents[1] + 1):
            for x in range(x_extents[0], x_extents[1] + 1):
                if self.grid[(x, y)] != '#':
                    continue

                needs_to_move = False
                for neighbor in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
                    nx, ny = neighbor
                    if self.grid[(x + nx, y + ny)] == '#':
                        needs_to_move = True
                        break

                if not needs_to_move:
                    continue

                for movement in self.movements:
                    if all([self.grid[(x + point[0], y + point[1])] != '#' for point in movement]):
                        next_pos = x + movement[0][0], y + movement[0][1]

                        if self.movement_desires[next_pos] is None:
                            self.movement_desires[next_pos] = (x, y)
                        else:
                            self.movement_desires[next_pos] = False

                        break

    def commit_movements(self):
        x_extents, y_extents = self.movement_desires.extents

        for y in range(y_extents[0], y_extents[1] + 1):
            for x in range(x_extents[0], x_extents[1] + 1):
                origin_point = self.movement_desires[(x, y)]
                if not origin_point:
                    continue

                if self.grid[origin_point] != '#':
                    print(f'Invalid origin point {origin_point}.')
                if self.grid[(x, y)] == '#':
                    print(f'Invalid destination point {(x, y)}.')

                self.grid[origin_point] = '.'
                self.grid[(x, y)] = '#'

        self.movements = self.movements[1:] + [self.movements[0]]

    def get_day_1_answer(self, use_sample=False) -> str:
        for _ in range(10):
            self.select_movements()
            self.commit_movements()

        filled_tiles = [t for t in self.grid.grid.keys() if self.grid[t] == '#']

        x0, x1 = (min([f[0] for f in filled_tiles]), max([f[0] for f in filled_tiles]))
        y0, y1 = (min([f[1] for f in filled_tiles]), max([f[1] for f in filled_tiles]))

        area = (y1 + 1 - y0) * (x1 + 1 - x0)

        return str(area - len(filled_tiles))

    def get_day_2_answer(self, use_sample=False) -> str:
        finished = False
        i = 0
        while not finished:
            grid_before = deepcopy(self.grid.grid)

            self.select_movements()
            self.commit_movements()

            i += 1

            if self.grid.grid == grid_before:
                finished = True

        return str(i)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
