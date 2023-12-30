from typing import List

from helpers.grid import Grid, Point, SparseGrid, ArrayGrid
from puzzle_base import PuzzleBase


DIR_ANGLES = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]


class Puzzle(PuzzleBase):
    year = 2023
    day = 16

    grid: Grid
    dir_grid: Grid
    active_grid: Grid
    filled_dirs: dict

    base_data: List[str]

    new_lasers: list[tuple[Point, Point]]
    laser_total = 0

    def reset(self):
        self.grid = ArrayGrid.create_empty(0, 0, '.')
        self.dir_grid = ArrayGrid.create_empty(0, 0, '.')
        self.active_grid = ArrayGrid.create_empty(0, 0, '.')
        self.filled_dirs = {}

        self.new_lasers = []
        self.laser_total = 0

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = ArrayGrid.from_strings(input_data)
        self.dir_grid = ArrayGrid.from_strings(input_data)
        self.active_grid = ArrayGrid.from_strings(input_data)

        self.base_data = input_data

    def reset_grids(self):
        self.reset()

        self.grid = ArrayGrid.from_strings(self.base_data)
        self.dir_grid = ArrayGrid.from_strings(self.base_data)
        self.active_grid = ArrayGrid.from_strings(self.base_data)

    def dir_to_char(self, direction: Point):
        if direction == Point(1, 0):
            return '>'
        elif direction == Point(-1, 0):
            return '<'
        elif direction == Point(0, 1):
            return 'V'
        elif direction == Point(0, -1):
            return '^'

    def reflect_laser(self, direction: Point, mirror_char: str):
        if direction not in DIR_ANGLES:
            return Point(0, 0)

        reflected_cw = DIR_ANGLES[(DIR_ANGLES.index(direction) + 1) % len(DIR_ANGLES)]
        reflected_ccw = DIR_ANGLES[DIR_ANGLES.index(direction) - 1]

        if mirror_char == '\\':
            return reflected_cw if direction.y == 0 else reflected_ccw
        elif mirror_char == '/':
            return reflected_cw if direction.x == 0 else reflected_ccw

        return Point(0, 0)

    def can_advance_laser(self, laser_pos: Point, direction: Point):
        if direction == (0, 0):
            return False

        new_pos = laser_pos + direction

        if self.grid[new_pos] != '.':
            return True  # we'll allow overlapping on mirror/split tiles

        is_repeat = new_pos in self.filled_dirs and direction in self.filled_dirs[new_pos]

        return not is_repeat and self.grid[laser_pos + direction] is not None

    def add_laser(self, laser_pos: Point, direction: Point):
        if self.grid[laser_pos] is None:
            return

        if self.dir_grid[laser_pos] and self.dir_grid[laser_pos] in '><^V':
            self.dir_grid[laser_pos] = '2'
        elif self.dir_grid[laser_pos] and self.dir_grid[laser_pos].isnumeric():
            self.dir_grid[laser_pos] = str(int(self.dir_grid[laser_pos]) + 1)
        elif self.dir_grid[laser_pos] and self.dir_grid[laser_pos] not in '<>V^|-\\/':
            self.dir_grid[laser_pos] = self.dir_to_char(direction)

        if self.active_grid[laser_pos] != '#':
            self.active_grid[laser_pos] = '#'
            self.laser_total = self.laser_total + 1

        if laser_pos in self.filled_dirs:
            self.filled_dirs[laser_pos].append(direction)
        else:
            self.filled_dirs[laser_pos] = [direction]

        if direction.x != 0 or direction.y != 0 and (laser_pos, direction) not in self.new_lasers:
            self.new_lasers.append((laser_pos, direction))

    def advance_lasers(self):
        laser_pos, direction = self.new_lasers[0]
        self.new_lasers = self.new_lasers[1:]

        if self.can_advance_laser(laser_pos, direction):
            next_tile = self.grid[laser_pos + direction]

            if next_tile == '\\':
                self.add_laser(laser_pos + direction, Point(0, 0))

                self.add_laser(laser_pos + direction, self.reflect_laser(direction, '\\'))
            elif next_tile == '/':
                self.add_laser(laser_pos + direction, Point(0, 0))

                self.add_laser(laser_pos + direction, self.reflect_laser(direction, '/'))
            elif next_tile == '|' and direction.x != 0:
                self.add_laser(laser_pos + direction, Point(0, 0))

                self.add_laser(laser_pos + direction, Point(0, -1))
                self.add_laser(laser_pos + direction, Point(0, 1))
            elif next_tile == '-' and direction.y != 0:
                self.add_laser(laser_pos + direction, Point(0, 0))

                self.add_laser(laser_pos + direction, Point(-1, 0))
                self.add_laser(laser_pos + direction, Point(1, 0))
            else:
                self.add_laser(laser_pos + direction, direction)

    def run_laser_grid(self, starting_laser: Point, starting_dir: Point):
        self.new_lasers.append((starting_laser, starting_dir))

        while len(self.new_lasers):
            self.advance_lasers()

        grid_strs = [
            str(self.grid).split('\n'),
            str(self.dir_grid).split('\n'),
            str(self.active_grid).split('\n'),
        ]

        combined_str = ''
        for i in range(len(grid_strs[0])):
            combined_str += '  |  '.join([grid_strs[j][i] for j in range(len(grid_strs))]) + '\n'

        print(f'{starting_laser} -> {starting_dir} | {self.laser_total} Laser tiles')
        print(combined_str[:-1])
        print('\n')

        return self.laser_total

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.run_laser_grid(Point(-1, 0), Point(1, 0)))

    def get_part_2_answer(self, use_sample=False) -> str:
        candidates = []

        for x in range(self.grid.width):
            candidates.append(self.run_laser_grid(Point(x, -1), Point(0, 1)))
            self.reset_grids()

            candidates.append(self.run_laser_grid(Point(x, self.grid.height), Point(0, -1)))
            self.reset_grids()

        for y in range(self.grid.height):
            candidates.append(self.run_laser_grid(Point(-1, y), Point(1, 0)))
            self.reset_grids()

            candidates.append(self.run_laser_grid(Point(self.grid.width, y), Point(-1, 0)))
            self.reset_grids()

        return str(max(candidates))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
