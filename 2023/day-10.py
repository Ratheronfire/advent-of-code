from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


PIPE_NEIGHBOR_OFFSETS = {
    '|': [(0, -1), (0,  1)],
    '-': [(-1, 0), (1,  0)],
    'L': [(0, -1), (1,  0)],
    'J': [(0, -1), (-1, 0)],
    '7': [(0,  1), (-1, 0)],
    'F': [(0,  1), (1,  0)],
    'S': [(0, -1), (0,  1), (-1, 0), (1,  0)],
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

# Key: Tuple containing in/out direction
# Value: List containing 1: pipe, 2: out direction
#   Example: Key ('-', (1, 0)) Means entering rightwards and exiting rightwards
#   Value: First list contains (0, 1) - The point below is on the right side, and the second contains (0, -1)
LOOP_SIDES = {
    # Right
    ('-', (1, 0)): [
        [(0, -1)],
        [(0, 1)]

    ],
    # Left
    ('-', (-1, 0)): [
        [(0, 1)],
        [(0, -1)]
    ],
    # Down
    ('|', (0, 1)): [
        [(1, 0)],
        [(-1, 0)]
    ],
    # Up
    ('|', (0, -1)): [
        [(-1, 0)],
        [(1, 0)]
    ],
    # Right Up
    ('J', (0, -1)): [
        [(-1, -1)],
        [(1, 0), (1, -1), (0, -1)]
    ],
    # Down Left
    ('J', (-1, 0)): [
        [(1, 0), (1, -1), (0, -1)],
        [(-1, -1)]
    ],
    # Right Down
    ('7', (0, 1)): [
        [(1, 0), (1, 1), (0, 1)],
        [(-1, 1)]
    ],
    # Up Left
    ('7', (-1, 0)): [
        [(-1, 1)],
        [(1, 0), (1, 1), (0, 1)]
    ],
    # Left Up
    ('L', (0, -1)): [
        [(-1, 0), (-1, 1), (0, 1)],
        [(1, -1)]
    ],
    # Down Right
    ('L', (1, 0)): [
        [(1, -1)],
        [(-1, 0), (-1, 1), (0, 1)]
    ],
    # Up Right
    ('F', (1, 0)): [
        [(0, -1), (-1, -1), (-1, 0)],
        [(1, 1)]
    ],
    # Left Down
    ('F', (0, 1)): [
        [(1, 1)],
        [(0, -1), (-1, -1), (-1, 0)]

    ]
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

        for offset in PIPE_NEIGHBOR_OFFSETS[self.grid[pipe_pos]]:
            neighbor_value = self.grid[(pipe_pos[0] + offset[0], pipe_pos[1] + offset[1])]
            if neighbor_value and (offset[0] * -1, offset[1] * -1) in PIPE_NEIGHBOR_OFFSETS[neighbor_value]:
                neighbors.append((pipe_pos[0] + offset[0], pipe_pos[1] + offset[1]))

        return neighbors

    def get_start_replacement(self):
        x, y = start = [pos for pos in self.grid.grid if self.grid[pos] == 'S'][0]

        pipe_neighbors = self.get_pipe_neighbors(start)

        if pipe_neighbors[0][0] == x and pipe_neighbors[1][0] == x:
            return '-'
        if pipe_neighbors[0][1] == y and pipe_neighbors[1][1] == y:
            return '|'
        if any([p[0] - x == 1 for p in pipe_neighbors]) and any([p[1] - y == 1 for p in pipe_neighbors]):
            return '7'
        if any([p[0] - x == 1 for p in pipe_neighbors]) and any([p[1] - y == -1 for p in pipe_neighbors]):
            return 'J'
        if any([p[0] - x == -1 for p in pipe_neighbors]) and any([p[1] - y == 1 for p in pipe_neighbors]):
            return 'F'
        if any([p[0] - x == -1 for p in pipe_neighbors]) and any([p[1] - y == -1 for p in pipe_neighbors]):
            return 'L'

        return 'S'

    def locate_loop(self):
        x, y = [pos for pos in self.grid.grid if self.grid[pos] == 'S'][0]

        loop_segments = set()
        loop_segments.add((x, y))

        loop_finished = False

        while not loop_finished:
            pipe_neighbors = self.get_pipe_neighbors((x, y))

            new_neighbors = [n for n in pipe_neighbors if n not in loop_segments]
            if len(new_neighbors):
                x, y = new_neighbors[0]
            else:
                loop_finished = True

            for neighbor in pipe_neighbors:
                loop_segments.add(neighbor)

        self.loop = [l for l in loop_segments]

    def is_point_outside(self, point):
        next_point = point

        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            while self.grid[next_point] == '.':
                next_point = (next_point[0] + direction[0], next_point[1] + direction[1])

            if self.grid[next_point] is None:
                return True  # this point is outside the extents, therefore it's the edge
            # if we got here, we must have hit a pipe

        # check failed in all four directions
        return False

    def check_side(self, x, y, side_checks, found_out_side, is_lefthand):
        is_out_side = False

        for check in side_checks:
            cx, cy = check
            edge = (x + cx, y + cy)

            if self.grid[edge] == '.':
                if not found_out_side:
                    is_out_side = self.is_point_outside(edge)
                self.grid[edge] = 'A' if is_lefthand else 'B'

        return is_out_side

    def scan_loop_edges(self):
        x, y = [pos for pos in self.grid.grid if self.grid[pos] == 'S'][0]

        loop_segments = set()
        loop_segments.add((x, y))

        loop_finished = False

        found_out_side = False
        a_is_outside = False

        while not loop_finished:
            pipe_neighbors = self.get_pipe_neighbors(Point(x, y))

            new_neighbors = [n for n in pipe_neighbors if n not in loop_segments]
            if len(new_neighbors):
                direction = (new_neighbors[0][0] - x, new_neighbors[0][1] - y)

                if self.grid[(x, y)] == 'S':
                    pipe = self.get_start_replacement()
                else:
                    pipe = self.grid[(x, y)]

                side_checks = LOOP_SIDES[(pipe, direction)]

                left_is_out = self.check_side(x, y, side_checks[0], found_out_side, True)
                right_is_out = self.check_side(x, y, side_checks[1], found_out_side, False)

                if not found_out_side and left_is_out:
                    a_is_outside = True
                    found_out_side = True
                if not found_out_side and right_is_out:
                    a_is_outside = False
                    found_out_side = True

                x, y = new_neighbors[0]
            else:
                loop_finished = True

            for neighbor in pipe_neighbors:
                loop_segments.add(neighbor)

        return a_is_outside

    def isolate_loop(self):
        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                if (x, y) not in self.loop and self.grid[(x, y)] not in 'IOS?':
                    self.grid[(x, y)] = self.grid.default_value

    def pretty_print_grid(self):
        grid_copy = Grid.from_strings(str(self.grid).split('\n'))

        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                if (x, y) not in self.loop and grid_copy[(x, y)] not in 'IOSAB?':
                    grid_copy[x, y] = self.grid.default_value
                elif grid_copy[x, y] in CHAR_REPLACEMENTS:
                    grid_copy[x, y] = CHAR_REPLACEMENTS[grid_copy[x, y]]

        print('\n' + str(grid_copy))

    def flood_fill(self, char_to_target):
        univisited_points = [p for p in self.grid.grid if self.grid[p] == char_to_target]
        point_queue = []

        while len(univisited_points):
            point_queue.append(univisited_points[0])

            while len(point_queue):
                x, y = point = point_queue.pop()

                if point in univisited_points:
                    univisited_points.remove(point)

                for neighbor in self.grid.neighbors((x, y)):
                    nx, ny = neighbor[0]
                    neighbor_val = self.grid[neighbor[0]]

                    if neighbor_val != char_to_target and neighbor_val != self.grid.default_value:
                        continue

                    if (nx, ny) in univisited_points or neighbor_val == self.grid.default_value:
                        self.grid[neighbor[0]] = char_to_target
                        point_queue.append((nx, ny))

    def get_part_1_answer(self, use_sample=False) -> str:
        self.locate_loop()

        return str(len(self.loop) // 2)

    def get_part_2_answer(self, use_sample=False) -> str:
        self.locate_loop()
        self.isolate_loop()

        a_is_outside = self.scan_loop_edges()

        self.flood_fill('A')
        self.flood_fill('B')

        matching_char = 'B' if a_is_outside else 'A'

        return str(len([p for p in self.grid.grid if self.grid[p] == matching_char]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
