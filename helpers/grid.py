from typing import List, Tuple

# Based on code from https://www.reddit.com/r/adventofcode/comments/zkc974/python_data_structures_for_2d_grids/


class Grid(object):
    grid = {}

    extents: Tuple[int, int]

    def __init__(self, grid):
        self.grid = grid

        self._calculate_extents()

    def __getitem__(self, item: Tuple[int, int]):
        return self.grid[item] if item in self.grid else None

    def __setitem__(self, key: Tuple[int, int], value):
        self.grid[key] = value

    def __str__(self):
        return '\n'.join([
            ''.join([
                str(self[(x, y)]) for x in range(self.extents[0] + 1)
            ]) for y in range(self.extents[1] + 1)
        ])

    def neighbors(self, pos: Tuple[int, int]):
        x0, y0 = pos

        candidates = [(x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1)]
        return [self[p] for p in candidates if p in self]

    def _calculate_extents(self):
        self.extents = (
            max([pos[0] for pos in self.grid.keys()]),
            max([pos[1] for pos in self.grid.keys()])
        )

    @staticmethod
    def create_empty(width: int, height: int, default_value):
        grid = Grid({(x, y): default_value for y, line in enumerate(range(height))
                     for x, _ in enumerate(range(width))})
        grid.extents = (width, height)

        return grid

    @staticmethod
    def from_number_strings(strings: List[str]):
        return Grid({(x, y): int(val) for y, line in enumerate(strings)
                     for x, val in enumerate(line)})

    @staticmethod
    def from_dict(grid_dict):
        grid = Grid(grid_dict)

        grid._calculate_extents()

        return grid
