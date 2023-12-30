from typing import List

from helpers.grid import Grid, Point, ArrayGrid
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
    '|': '║ ',
    '-': '══',
    'F': '╔═',
    '7': '╗ ',
    'L': '╚═',
    'J': '╝ ',
    '.': '  ',
    '#': '██',
    'S': 'SS',
    'I': '██',
    'O': '░░'
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
        self.grid = ArrayGrid.create_empty(0, 0)
        self.loop = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = ArrayGrid.from_strings(input_data)

    def get_pipe_neighbors(self, pipe_pos: Point):
        neighbors = []

        for offset in PIPE_NEIGHBOR_OFFSETS[self.grid[pipe_pos]]:
            neighbor_value = self.grid[(pipe_pos[0] + offset[0], pipe_pos[1] + offset[1])]
            if neighbor_value and (offset[0] * -1, offset[1] * -1) in PIPE_NEIGHBOR_OFFSETS[neighbor_value]:
                neighbors.append((pipe_pos[0] + offset[0], pipe_pos[1] + offset[1]))

        return neighbors

    def get_start_replacement(self):
        x, y = start = self.grid.index('S')

        pipe_neighbors = self.get_pipe_neighbors(start)

        if pipe_neighbors[0][0] == x and pipe_neighbors[1][0] == x:
            return '-'
        if pipe_neighbors[0][1] == y and pipe_neighbors[1][1] == y:
            return '|'
        if any([p[0] - x == -1 for p in pipe_neighbors]) and any([p[1] - y == 1 for p in pipe_neighbors]):
            return '7'
        if any([p[0] - x == 1 for p in pipe_neighbors]) and any([p[1] - y == -1 for p in pipe_neighbors]):
            return 'J'
        if any([p[0] - x == 1 for p in pipe_neighbors]) and any([p[1] - y == 1 for p in pipe_neighbors]):
            return 'F'
        if any([p[0] - x == -1 for p in pipe_neighbors]) and any([p[1] - y == -1 for p in pipe_neighbors]):
            return 'L'

        return 'S'

    def locate_loop(self):
        x, y = s_point = self.grid.index('S')

        loop_segments = set()
        loop_segments.add(s_point)

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

    def isolate_loop(self):
        for x in range(self.grid.extents[0][1]):
            for y in range(self.grid.extents[1][1]):
                if (x, y) not in self.loop and self.grid[(x, y)] and self.grid[(x, y)] not in 'IOS?':
                    self.grid[(x, y)] = self.grid.default_value

    def pretty_print_grid(self):
        grid_copy = ArrayGrid(self.grid.export_values(), self.grid.default_value)

        for x in range(self.grid.extents[0][1]):
            for y in range(self.grid.extents[1][1]):
                if (x, y) not in self.loop and grid_copy[x, y] not in 'IOS':
                    grid_copy[x, y] = CHAR_REPLACEMENTS[self.grid.default_value]
                elif grid_copy[x, y] in CHAR_REPLACEMENTS:
                    grid_copy[x, y] = CHAR_REPLACEMENTS[grid_copy[x, y]]

        print('\n' + str(grid_copy))

    def scan_for_inner_points(self):
        total = 0
        is_inner = False
        last_pipe = ''

        for y in range(self.grid.extents[1][1]):
            for x in range(self.grid.extents[0][1]):
                tile = self.grid[(x, y)]

                if tile and tile in '|L7JF':
                    if last_pipe + tile not in ['L7', 'FJ']:
                        is_inner = not is_inner

                    last_pipe = tile

                if tile == self.grid.default_value:
                    self.grid[(x, y)] = 'I' if is_inner else 'O'

                if is_inner and tile == self.grid.default_value:
                    total += 1

            is_inner = False

        return total

    def get_part_1_answer(self, use_sample=False) -> str:
        self.locate_loop()

        self.pretty_print_grid()

        return str(len(self.loop) // 2)

    def get_part_2_answer(self, use_sample=False) -> str:
        self.locate_loop()
        self.isolate_loop()

        start_pos = self.grid.index('S')
        self.grid[start_pos] = self.get_start_replacement()

        total = self.scan_for_inner_points()
        self.pretty_print_grid()

        return str(total)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
