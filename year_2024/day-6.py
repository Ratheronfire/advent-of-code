from typing import List

from helpers.grid import ArrayGrid, Point
from helpers.number_helpers import clamp
from puzzle_base import PuzzleBase

PathStep = tuple[str, Point]


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

    jumps: dict[PathStep, Point] = {}

    def reset(self):
        self.grid = ArrayGrid.create_empty(0, 0, '.')

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = ArrayGrid.from_strings(input_data)
        self.init_jumps()

    def add_jumps_from_slice(self, grid_slice: ArrayGrid, top_left_coords: Point):
        is_horizontal = grid_slice.height == 1
        offset = Point(1, 0) if is_horizontal else Point(0, 1)
        directions = '><' if is_horizontal else 'v^'

        last_jump = top_left_coords

        for y in range(grid_slice.height):
            for x in range(grid_slice.width):
                point = Point(x, y)

                if grid_slice[point] in '#O' or x == self.grid.width - 1 or y == self.grid.height - 1:
                    previous = point - offset

                    if grid_slice[previous] is None:
                        last_jump = point + top_left_coords + offset
                        continue

                    if grid_slice[point] == '.':
                        self.jumps[(directions[0], last_jump)] = point + top_left_coords
                        self.jumps[(directions[1], point + top_left_coords)] = last_jump
                    elif grid_slice[point] in '#O' and grid_slice[previous] == '.':
                        self.jumps[(directions[0], last_jump)] = previous + top_left_coords
                        self.jumps[(directions[1], previous + top_left_coords)] = last_jump

                    last_jump = point + top_left_coords + offset

    def init_jumps(self):
        self.jumps = {}

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.calculate_jumps(x, y)

    def recalculate_jumps(self, target_pos: Point):
        invalid_keys = []
        for jump in self.jumps.keys():
            if jump[1].x == target_pos.x or jump[1].y == target_pos.y:
                invalid_keys.append(jump)

        for jump in invalid_keys:
            del self.jumps[jump]

        for x in range(0, self.grid.width):
            self.calculate_jumps(x, target_pos.y)
        for y in range(0, self.grid.height):
            self.calculate_jumps(target_pos.x, y)

    def calculate_jumps(self, x: int, y: int):
        pos = Point(x, y)
        neighbors = self.grid.neighbors(Point(x, y), True)

        if x == 0 or x == self.grid.width - 1 \
                or y == 0 or y == self.grid.height - 1 \
                or self.grid[pos] in '<>^v' \
                or any([n[1] in '#O' for n in neighbors]):
            for direction in OFFSETS.keys():
                offset_pos = Point(x, y)

                while self.grid[offset_pos + OFFSETS[direction]] and self.grid[offset_pos + OFFSETS[direction]] in '.><^v':
                    offset_pos += OFFSETS[direction]

                self.jumps[(direction, pos)] = offset_pos

    def display_path(self, path):
        display_grid = self.grid.copy()

        for step in path:
            direction, position = step
            display_grid[position] = direction

        print(display_grid)

    def find_guard(self) -> Point:
        guard_pos = Point(-1, -1)

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid[(x, y)] in 'v^<>':
                    guard_pos = Point(x, y)

                    break

        return guard_pos

    def step_grid(self, guard_pos: Point, direction: str):
        if (direction, guard_pos) in self.jumps:
            return self.jumps[(direction, guard_pos)]

        next_pos = guard_pos + OFFSETS[direction]

        if self.grid[next_pos] is None or self.grid[next_pos] in '.X<>^v':
            return next_pos
        else:
            return guard_pos

    def simulate_guard_path(self, guard_pos: Point, guard_dir: str) -> tuple[list[PathStep], bool]:
        visited_tiles: list[PathStep] = [(guard_dir, guard_pos)]
        looped = False

        while True:
            guard_pos = self.step_grid(guard_pos, guard_dir)

            if self.grid[guard_pos + OFFSETS[guard_dir]] and self.grid[guard_pos + OFFSETS[guard_dir]] in '#O':
                guard_dir = ROTATIONS[guard_dir]

            if self.grid[guard_pos + OFFSETS[guard_dir]] is None:
                # At the edge of the grid, unable to continue (i.e. exited the grid)
                visited_tiles.append((guard_dir, guard_pos))
                break

            if (guard_dir, guard_pos) in visited_tiles:
                # Loop detected.
                looped = True
                visited_tiles.append((guard_dir, guard_pos))
                break

            visited_tiles.append((guard_dir, guard_pos))

        full_tiles: list[PathStep] = []
        for i in range(1, len(visited_tiles)):
            a_dir, a = visited_tiles[i-1]
            b_dir, b = visited_tiles[i]

            x_offset = 1 if a.x <= b.x else -1
            y_offset = 1 if a.y <= b.y else -1

            for y in range(a.y, b.y + y_offset, y_offset):
                for x in range(a.x, b.x + x_offset, x_offset):
                    if (a_dir, Point(x, y)) not in full_tiles:
                        full_tiles.append((a_dir, Point(x, y)))

        return full_tiles, looped

    def get_loop_count(self) -> int:
        start_pos = self.find_guard()
        start_dir = self.grid[start_pos]
        canonical_path = self.simulate_guard_path(start_pos, start_dir)[0]

        loop_points = set()

        for step in canonical_path:
            direction, position = step
            obstacle_pos = position + OFFSETS[direction]

            if obstacle_pos == start_pos or self.grid[obstacle_pos] != '.':
                continue

            self.grid[obstacle_pos] = 'O'
            self.recalculate_jumps(obstacle_pos)

            alternate_path, looped = self.simulate_guard_path(start_pos, start_dir)

            if looped:
                loop_points.add(obstacle_pos)

            self.grid[obstacle_pos] = '.'
            self.recalculate_jumps(obstacle_pos)

        return len(loop_points)

    def get_part_1_answer(self, use_sample=False) -> str:
        guard_pos = self.find_guard()

        visited_tiles = self.simulate_guard_path(guard_pos, self.grid[guard_pos])[0]
        unique_tiles = set([tile[1] for tile in visited_tiles])

        return str(len(unique_tiles))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.get_loop_count())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
