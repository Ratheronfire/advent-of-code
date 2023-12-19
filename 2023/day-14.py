from typing import List

from helpers.grid import Grid, Point, ArrayGrid
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2023
    day = 14

    grid: Grid

    rock_cache = {}

    def reset(self):
        self.rock_cache = {}
        self.grid = ArrayGrid.create_empty(0, 0, '.')

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = ArrayGrid.from_strings(input_data)

    def get_round_rocks(self) -> list[Point]:
        rock_positions = []

        for y in range(0, self.grid.height):
            for x in range(0, self.grid.width):
                if self.grid[(x, y)] == 'O':
                    rock_positions.append(Point(x, y))

        return rock_positions

    def get_next_position(self, rock_pos: Point, tilt_dir: Point):
        while self.grid[rock_pos + tilt_dir] == self.grid.default_value:
            rock_pos = rock_pos + tilt_dir

        return rock_pos

    def tilt_grid(self, tilt_dir: Point):
        rocks_before = hash(tuple([(r.x, r.y) for r in self.get_round_rocks()] + [(tilt_dir.x, tilt_dir.y)]))

        if rocks_before in self.rock_cache:
            print('Cached!')
            self.grid.import_values(self.rock_cache[rocks_before])
            return

        rocks = self.get_round_rocks()
        next_rocks = []

        while any([self.grid[r + tilt_dir] == '.' for r in rocks]):
            for rock in rocks:
                new_rock = self.get_next_position(rock, tilt_dir)

                self.grid[rock] = self.grid.default_value
                self.grid[new_rock] = 'O'

                next_rocks.append(new_rock)

            rocks = next_rocks.copy()
            next_rocks.clear()

        self.rock_cache[rocks_before] = self.grid.export_values()

    def spin(self, count: int):
        rock_history = []

        i = 0
        while i < count:
            self.tilt_grid(Point(0, -1))
            self.tilt_grid(Point(-1, 0))
            self.tilt_grid(Point(0, 1))
            self.tilt_grid(Point(1, 0))

            rocks = [(r.x, r.y) for r in self.get_round_rocks()]

            for j, rock_set in enumerate(rock_history):
                if rock_set == rocks:
                    print(f'Loop found from {j} to {i}!')
                    print(self.grid)

                    loop_period = i - j
                    loop_offset = (count - j) % -loop_period - 1
                    return rock_history[loop_offset]

            rock_history.append(rocks)

            i += 1

    def get_load(self, rocks: list[Point]):
        total_load = 0

        for rock in rocks:
            total_load += self.grid.height - rock[1]

        return total_load

    def get_part_1_answer(self, use_sample=False) -> str:
        self.tilt_grid(Point(0, -1))

        print(self.grid)

        return str(self.get_load(self.get_round_rocks()))

    def get_part_2_answer(self, use_sample=False) -> str:
        rocks = self.spin(1000000000)

        return str(self.get_load(rocks))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
