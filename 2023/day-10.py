from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


PIPE_NEIGHBOR_OFFSETS = {
    '|': [Point(0, -1), Point(0,  1)],
    '-': [Point(-1, 0), Point(1,  0)],
    'L': [Point(0, -1), Point(1,  0)],
    'J': [Point(0, -1), Point(-1, 0)],
    '7': [Point(0,  1), Point(-1, 0)],
    'F': [Point(0,  1), Point(1,  0)],
    'S': [Point(0, -1), Point(0,  1), Point(-1, 0), Point(1,  0)],
    '.': [],
    'I': [],
    'O': []
}

CHAR_REPLACEMENTS = {
    '|': '║',
    '-': '═',
    'F': '╔',
    '7': '╗',
    'L': '╚',
    'J': '╝'
}


class Puzzle(PuzzleBase):
    year = 2023
    day = 10

    grid: Grid
    loop: list[Point]

    def reset(self):
        self.grid = Grid.create_empty(0, 0)
        self.loop = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = Grid.from_strings(input_data)

    def get_pipe_neighbors(self, pipe_pos: Point):
        neighbors = []

        for neighbor_offset in PIPE_NEIGHBOR_OFFSETS[self.grid[pipe_pos]]:
            neighbor_value = self.grid[pipe_pos + neighbor_offset]
            if neighbor_value and neighbor_offset * -1 in PIPE_NEIGHBOR_OFFSETS[neighbor_value]:
                neighbors.append(pipe_pos + neighbor_offset)

        return neighbors

    def locate_loop(self):
        x, y = [pos for pos in self.grid.grid if self.grid[pos] == 'S'][0]

        loop_segments = set()
        loop_segments.add(Point(x, y))

        loop_finished = False

        while not loop_finished:
            pipe_neighbors = self.get_pipe_neighbors(Point(x, y))

            new_neighbors = [n for n in pipe_neighbors if n not in loop_segments]
            if len(new_neighbors):
                x, y = new_neighbors[0]
            else:
                loop_finished = True

            for neighbor in pipe_neighbors:
                loop_segments.add(neighbor)

        self.loop = [l for l in loop_segments]

    def isolate_loop(self):
        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                if (x, y) not in self.loop and self.grid[(x, y)] not in 'IOS?':
                    self.grid[x, y] = self.grid.default_value

    def pretty_print_grid(self):
        grid_copy = Grid.from_strings(str(self.grid).split('\n'))

        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                if (x, y) not in self.loop and grid_copy[(x, y)] not in 'IOS?':
                    grid_copy[x, y] = self.grid.default_value
                elif grid_copy[x, y] in CHAR_REPLACEMENTS:
                    grid_copy[x, y] = CHAR_REPLACEMENTS[grid_copy[x, y]]

        print('\n' + str(grid_copy))

    def scale_grid(self):
        scaled_grid = Grid.create_empty(self.grid.width * 2, self.grid.height * 2, '.')

        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                grid_val = self.grid[(x, y)]

                scaled_grid[(x * 2, y * 2)] = self.grid[(x, y)]

                if grid_val != 'S':
                    for neighbor_offset in PIPE_NEIGHBOR_OFFSETS[grid_val]:
                        nx, ny = neighbor_offset
                        scaled_grid[((x * 2) + nx, (y * 2) + ny)] = '-' if ny == 0 else '|'

        return scaled_grid

    def flood_fill(self):
        univisited_points = [p for p in self.grid.grid if self.grid[p] == self.grid.default_value]
        point_queue = []
        pending_points = []

        hit_surfaces = set()
        hit_extents = False

        inside_points = set()

        while len(univisited_points):
            hit_extents = False

            point_queue.append(univisited_points[0])

            while len(point_queue):
                x, y = point = point_queue.pop()
                pending_points.append((x, y))

                # self.grid[(x, y)] = '?'

                if point in univisited_points:
                    univisited_points.remove(point)

                if x in self.grid.extents[0] or y in self.grid.extents[1]:
                    hit_extents = True

                for neighbor in self.grid.neighbors((x, y)):
                    nx, ny = neighbor[0]
                    if self.grid[neighbor[0]] in '|-7FJLS':
                        hit_surfaces.add(neighbor)
                    elif (nx, ny) in univisited_points:
                        point_queue.append((nx, ny))

            for p in pending_points:
                self.grid[p] = 'O' if hit_extents else 'I'

            if not hit_extents:
                for point in pending_points:
                    inside_points.add(point)
            pending_points.clear()
            hit_surfaces = set()

        return len(inside_points)

    def get_inside_points_cheaty(self):
        total = 0

        for x in range(0, self.grid.extents[0][1] + 1, 2):
            for y in range(0, self.grid.extents[1][1] + 1, 2):
                if self.grid[(x, y)] == 'I' and self.grid[(x + 1, y)] == 'I' and \
                   self.grid[(x, y + 1)] == 'I' and self.grid[(x + 1, y + 1)] == 'I':
                    total += 1

        return total

    def get_part_1_answer(self, use_sample=False) -> str:
        self.locate_loop()

        return str(len(self.loop) // 2)

    def get_part_2_answer(self, use_sample=False) -> str:
        self.locate_loop()
        self.isolate_loop()

        self.pretty_print_grid()
        self.grid = self.scale_grid()
        self.locate_loop()

        self.pretty_print_grid()

        self.flood_fill()

        return str(self.get_inside_points_cheaty())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
