from typing import List

from helpers.grid import ArrayGrid, Point
from helpers.number_helpers import clamp
from puzzle_base import PuzzleBase


ROTATIONS = {
    '^': '>',
    'v': '<',
    '<': '^',
    '>': 'v'
}


OFFSETS = {
    '^': Point(0, -1),
    'v': Point(0, 1),
    '<': Point(-1, 0),
    '>': Point(1, 0)
}


class Puzzle(PuzzleBase):
    year = 2024
    day = 6

    grid: ArrayGrid

    cached_next_dirs = {}

    def reset(self):
        self.grid = ArrayGrid.create_empty(0, 0, '.')

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = ArrayGrid.from_strings(input_data)

    def find_guard(self) -> Point:
        guard_pos = Point(-1, -1)

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid[(x, y)] in 'v^<>':
                    guard_pos = Point(x, y)

                    break

        return guard_pos

    def get_next_guard_pos(self, guard_pos: Point, direction: Point) -> Point:
        next_pos = Point(guard_pos.x, guard_pos.y) + direction

        return next_pos

    def step_grid(self, guard_pos: Point, direction: Point):
        next_pos = self.get_next_guard_pos(guard_pos, direction)

        if self.grid[next_pos] is None or self.grid[next_pos] in '.X<>^v':
            return next_pos
        else:
            return guard_pos

    def simulate_guard_path(self) -> int:
        visited_tiles: dict[Point, list[str]] = {}

        guard_pos = self.find_guard()
        guard_dir = self.grid[guard_pos]

        self.cached_next_dirs = {}

        while True:
            next_pos = self.step_grid(guard_pos, OFFSETS[guard_dir])

            if next_pos.x <= -1 or next_pos.x >= self.grid.width or next_pos.y <= -1 or next_pos.y >= self.grid.height:
                # At the edge of the grid, unable to continue (i.e. exited the grid)
                break

            if guard_pos in visited_tiles:
                visited_tiles[guard_pos].append(OFFSETS[guard_dir])
            else:
                visited_tiles[guard_pos] = [guard_dir]

            if guard_pos not in self.cached_next_dirs:
                self.cached_next_dirs[guard_pos] = {}

            if self.grid[self.get_next_guard_pos(guard_pos, OFFSETS[guard_dir])] == '#':
                next_dir = ROTATIONS[guard_dir]
            else:
                next_dir = guard_dir

            self.cached_next_dirs[guard_pos][guard_dir] = (next_pos, next_dir)

            guard_pos = next_pos
            guard_dir = next_dir

        return len(visited_tiles) + 1

    def is_looping(self, start_pos: Point, direction: str) -> bool:
        guard_pos = start_pos
        guard_dir = direction

        while True:
            if guard_pos == start_pos and ROTATIONS[guard_dir] == direction:
                # We've entered a loop
                return True

            if guard_pos in self.cached_next_dirs and guard_dir in self.cached_next_dirs[guard_pos]:
                guard_pos, guard_dir = self.cached_next_dirs[guard_pos][guard_dir]
                continue

            if self.grid[self.get_next_guard_pos(guard_pos, OFFSETS[guard_dir])] == '#':
                guard_dir = ROTATIONS[guard_dir]

            next_pos = self.step_grid(guard_pos, OFFSETS[guard_dir])

            if next_pos.x <= -1 or next_pos.x >= self.grid.width or next_pos.y <= -1 or next_pos.y >= self.grid.height:
                # At the edge of the grid, unable to continue (i.e. exited the grid)
                return False

            guard_pos = next_pos

    def get_loop_count(self) -> int:
        self.simulate_guard_path()

        loops = 0

        guard_pos = self.find_guard()
        guard_dir = self.grid[guard_pos]

        while True:
            if self.grid[self.get_next_guard_pos(guard_pos, OFFSETS[guard_dir])] == '#':
                guard_dir = ROTATIONS[guard_dir]
            elif self.is_looping(guard_pos, ROTATIONS[guard_dir]):
                loops += 1

            next_pos = self.step_grid(guard_pos, OFFSETS[guard_dir])

            if next_pos.x <= -1 or next_pos.x >= self.grid.width or next_pos.y <= -1 or next_pos.y >= self.grid.height:
                # At the edge of the grid, unable to continue (i.e. exited the grid)
                break

            guard_pos = next_pos

        return loops

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.simulate_guard_path())

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.get_loop_count())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
