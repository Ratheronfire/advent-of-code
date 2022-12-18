from typing import List, Tuple, Union, Optional

# Based on code from https://www.reddit.com/r/adventofcode/comments/zkc974/python_data_structures_for_2d_grids/


Point = Tuple[Union[int, float], Union[int, float]]
Line = Tuple[Point, Point]


class Grid(object):
    grid = {}

    extents: Tuple[Tuple[int, int], Tuple[int, int]]

    def __init__(self, grid):
        self.grid = grid

        self._calculate_extents()

    def __getitem__(self, item: Union[Tuple[int, int], slice]):
        if isinstance(item, slice):
            subgrid = Grid.create_empty(abs(item.stop[0] - item.start[0]) + 1, abs(item.stop[1] - item.start[1]) + 1, ' ')

            start, stop, step = _get_range_for_slice(item)

            sub_x, sub_y = (0, 0)

            for x in range(start[0], stop[0], step[0]):
                for y in range(start[1], stop[1], step[1]):
                    try:
                        subgrid[(sub_x, sub_y)] = self.grid[(x, y)]
                    except KeyError:
                        subgrid[(sub_x, sub_y)] = '░░'
                    sub_y += 1
                sub_x += 1
                sub_y = 0

            return subgrid
        elif isinstance(item, Tuple):
            return self.grid[item] if item in self.grid else None
        else:
            raise TypeError('Invalid argument for grid indexing.')

    def __setitem__(self, key: Tuple[int, int], value):
        if isinstance(key, slice):
            start, stop, step = _get_range_for_slice(key)

            # if len(value) != abs(start[1] - stop[1]) or len(value[0]) != abs(start[0] - stop[0]):

            sub_x, sub_y = (0, 0)
        else:
            if isinstance(value, List) or isinstance(value, Tuple):
                raise TypeError('Cannot assign multiple values to a single index.')
            else:
                self.grid[key] = value

        self._calculate_extents()

    def __str__(self):
        return '\n'.join([
            ''.join([
                str(self[(x, y)] or '░░') for x in range(self.extents[0][0], self.extents[0][1] + 1)
            ]) for y in range(self.extents[1][0], self.extents[1][1] + 1)
        ])

    def neighbors(self, pos: Tuple[int, int]):
        x0, y0 = pos

        candidates = [(x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1)]
        return [self[p] for p in candidates if p in self]

    def _calculate_extents(self):
        if not len(self.grid.keys()):
            self.extents = ((0, 0), (0, 0))
            return

        self.extents = (
            (min([pos[0] for pos in self.grid.keys()]), max([pos[0] for pos in self.grid.keys()])),
            (min([pos[1] for pos in self.grid.keys()]), max([pos[1] for pos in self.grid.keys()]))
        )

    @staticmethod
    def create_empty(width: int, height: int, default_value):
        grid = Grid({(x, y): default_value for y, line in enumerate(range(height))
                     for x, _ in enumerate(range(width))})

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


def get_line_intersection(a: Line, b: Line) -> Optional[Point]:
    x1, y1 = a[0]
    x2, y2 = a[1]
    x3, y3 = b[0]
    x4, y4 = b[1]

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    print(t)
    print(u)

    if 0 <= t <= 1:
        return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
    elif 0 <= u <= 1:
        return x3 + u * (x4 - x3), y3 + t * (y4 - y3)
    else:
        return None


def _get_range_for_slice(grid_slice):
    if grid_slice.step is None:
        step = (0, 0)

        if grid_slice.start[0] < grid_slice.stop[0]:
            step = (1, step[1])
        elif grid_slice.start[0] > grid_slice.stop[0]:
            step = (-1, step[1])

        if grid_slice.start[1] < grid_slice.stop[1]:
            step = (step[0], 1)
        elif grid_slice.start[1] > grid_slice.stop[1]:
            step = (step[0], -1)
    else:
        step = grid_slice.step

    start = [grid_slice.start[i] for i in [0, 1]]
    stop = [grid_slice.stop[i] + (1 if step[i] > 0 else -1 if step[i] < 0 else 0) for i in [0, 1]]

    return start, stop, step
