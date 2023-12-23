from abc import ABC
from typing import List, Tuple, Union, Optional

# Based on code from https://www.reddit.com/r/adventofcode/comments/zkc974/python_data_structures_for_2d_grids/

# Some helpful grid characters:
# ░░ - Empty space
# ██ - Filled space
# ═║╔╗╝╚ - Pipes


class Point:
    x: Union[int, float]
    y: Union[int, float]

    _base_type = Union[int, float]

    def scale(self, scalar: Union[int, float]):
        return Point(self.x * scalar, self.y * scalar)

    def __init__(self, x: _base_type, y: _base_type):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter([self.x, self.y])

    def __getitem__(self, item: int):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y

    def __str__(self):
        return str((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self.x, self.y) == other
        elif isinstance(other, Point):
            return self.x == other.x and self.y == other.y

        return False

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __mul__(self, scalar: int):
        return Point(self.x * scalar, self.y * scalar)


class Point3D(Point):
    z: Union[int, float]

    _base_type = Union[int, float]

    def scale(self, scalar: Union[int, float]):
        return Point3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __init__(self, x: _base_type, y: _base_type, z: _base_type):
        super().__init__(x, y)
        self.z = z

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __getitem__(self, item: int):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self.x, self.y, self.z) == other
        elif isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y and self.z == other.z

        return False

    def __add__(self, other):
        return Point3D(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        return Point3D(self.x - other[0], self.y - other[1], self.z - other[2])


Line = Tuple[Point, Point]


class Grid(ABC):
    grid: any

    extents: List[List[int]] = []

    invert_y_display = False

    default_value = '░░'

    _key_base_type = Tuple[Union[int, float], Union[int, float]]

    def __init__(self, grid, default_value='░░'):
        self.grid = grid
        self.default_value = default_value

        self._calculate_extents()

    def points(self):
        for y in range(self.extents[1][0], self.extents[1][1] + 1):
            for x in range(self.extents[0][0], self.extents[0][1] + 1):
                yield Point(x, y)

    def __getitem__(self, item: Union[Point, _key_base_type, slice]):
        pass

    def __setitem__(self, key: Union[Point, _key_base_type], value):
        pass

    def __str__(self):
        pass

    def index(self, value):
        pass

    def neighbors(self, pos: Point, include_diagonals=False):
        pass

    def export_values(self) -> dict:
        pass

    def import_values(self, value: dict):
        pass

    @property
    def width(self) -> int:
        pass

    @property
    def height(self) -> int:
        pass

    def _calculate_extents(self, newest_key=None):
        pass

    @staticmethod
    def create_empty(width: int, height: int, default_value='.'):
        pass

    @staticmethod
    def from_strings(strings: List[str], default_value='.'):
        pass

    @staticmethod
    def from_number_strings(strings: List[str], default_value='.'):
        pass

    @staticmethod
    def from_array(rows: List[List[Union[any]]], default_value='.'):
        pass

    @staticmethod
    def from_dict(grid_dict):
        pass


class ArrayGrid(Grid):
    grid: list[list[any]]

    _key_base_type = Tuple[Union[int, float], Union[int, float]]

    def __getitem__(self, item: Union[Point, _key_base_type, slice]):
        if isinstance(item, slice):
            subgrid = ArrayGrid.create_empty(abs(item.stop[0] - item.start[0]),
                                             abs(item.stop[1] - item.start[1]), ' ')

            start, stop, step = _get_range_for_slice(item)

            sub_x, sub_y = (0, 0)

            for x in range(start[0], stop[0] - 1, step[0]):
                for y in range(start[1], stop[1] - 1, step[1]):
                    try:
                        subgrid[(sub_x, sub_y)] = self.grid[y][x]
                    except KeyError:
                        subgrid[(sub_x, sub_y)] = self.default_value
                    sub_y += 1
                sub_x += 1
                sub_y = 0

            return subgrid
        elif isinstance(item, Tuple) or isinstance(item, Point):
            if self.extents[0][0] <= item[0] <= self.extents[0][1] and \
                    self.extents[1][0] <= item[1] <= self.extents[1][1]:
                return self.grid[item[1]][item[0]]

            return None
        else:
            raise TypeError('Invalid argument for grid indexing.')

    def __setitem__(self, key: Union[Point, _key_base_type], value):
        if isinstance(key, slice):
            raise NotImplementedError
        else:
            self.grid[key[1]][key[0]] = value

        self._calculate_extents(key)

    def __str__(self):
        y_range = range(self.extents[1][1], self.extents[1][0] - 1, -1) if self.invert_y_display else \
            range(self.extents[1][0], self.extents[1][1] + 1)

        return '\n'.join([
            ''.join([
                str(self.grid[y][x] or self.default_value) for x in range(self.extents[0][0], self.extents[0][1] + 1)
            ]) for y in y_range
        ])

    def index(self, value):
        for y in range(self.extents[1][1]):
            for x in range(self.extents[0][1]):
                if self[(x, y)] == 'S':
                    return Point(x, y)

        return None

    def neighbors(self, pos: Point, include_diagonals=False):
        x0, y0 = pos

        candidates = [(x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1)]
        if include_diagonals:
            candidates += [(x0 - 1, y0 - 1), (x0 - 1, y0 + 1), (x0 + 1, y0 - 1), (x0 + 1, y0 + 1)]
        return [(p, self[p]) for p in candidates if self[p] is not None]

    def export_values(self) -> list[list[any]]:
        return [row.copy() for row in self.grid]

    def import_values(self, value: list[list[any]]):
        self.grid = [row.copy() for row in value]

    @property
    def width(self) -> int:
        return self.extents[0][1] - self.extents[0][0] + 1

    @property
    def height(self) -> int:
        return self.extents[1][1] - self.extents[1][0] + 1

    def _calculate_extents(self, newest_key=None):
        self.extents = [[0, 0], [0, 0]]

        if not len(self.grid) or not len(self.grid[0]):
            return

        self.extents[0][0] = 0
        self.extents[0][1] = len(self.grid[0]) - 1

        self.extents[1][0] = 0
        self.extents[1][1] = len(self.grid) - 1

    @staticmethod
    def create_empty(width: int, height: int, default_value='.'):
        inner_grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(default_value)
            inner_grid.append(row)

        grid = ArrayGrid(inner_grid, default_value)

        return grid

    @staticmethod
    def from_strings(strings: List[str], default_value='.'):
        grid = ArrayGrid([[char for char in string] for string in strings if string != ''],
                         default_value)

        return grid

    @staticmethod
    def from_number_strings(strings: List[str], default_value='.'):
        grid = ArrayGrid([[int(char) for char in string] for string in strings],
                         default_value)

        return grid

    @staticmethod
    def from_array(rows: List[List[Union[any]]], default_value='.'):
        grid = ArrayGrid(rows, default_value)

        return grid

    @staticmethod
    def from_dict(grid_dict):
        raise NotImplementedError


class SparseGrid(Grid):
    grid = {}

    extents: List[List[int]] = []

    invert_y_display = False

    default_value = '░░'

    _key_base_type = Tuple[Union[int, float], Union[int, float]]

    def __getitem__(self, item: Union[Point, _key_base_type, slice]):
        if isinstance(item, slice):
            subgrid = Grid.create_empty(abs(item.stop[0] - item.start[0]) + 1, abs(item.stop[1] - item.start[1]) + 1, ' ')

            start, stop, step = _get_range_for_slice(item)

            sub_x, sub_y = (0, 0)

            for x in range(start[0], stop[0], step[0]):
                for y in range(start[1], stop[1], step[1]):
                    try:
                        subgrid[(sub_x, sub_y)] = self.grid[(x, y)]
                    except KeyError:
                        subgrid[(sub_x, sub_y)] = self.default_value
                    sub_y += 1
                sub_x += 1
                sub_y = 0

            return subgrid
        elif isinstance(item, Tuple):
            return self.grid[Point(item[0], item[1])] if item in self.grid else self.default_value
        elif isinstance(item, Point):
            return self.grid[item] if item in self.grid else self.default_value
        else:
            raise TypeError('Invalid argument for grid indexing.')

    def __setitem__(self, key: Union[Point, _key_base_type], value):
        if isinstance(key, slice):
            raise NotImplementedError
        else:
            if isinstance(key, tuple):
                key = Point(key[0], key[1])

            self.grid[key] = value

        self._calculate_extents(key)

    def __str__(self):
        y_range = range(self.extents[1][1], self.extents[1][0] - 1, -1) if self.invert_y_display else \
            range(self.extents[1][0], self.extents[1][1] + 1)

        return '\n'.join([
            ''.join([
                str(self[(x, y)] or self.default_value) for x in range(self.extents[0][0], self.extents[0][1] + 1)
            ]) for y in y_range
        ])

    def index(self, value):
        for y in range(self.extents[1][1]):
            for x in range(self.extents[0][1]):
                if self[(x, y)] == value:
                    return Point(x, y)

        return None

    def neighbors(self, pos: Point, include_diagonals=False):
        x0, y0 = pos

        candidates = [(x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1)]
        if include_diagonals:
            candidates += [(x0 - 1, y0 - 1), (x0 - 1, y0 + 1), (x0 + 1, y0 - 1), (x0 + 1, y0 + 1)]
        return [(p, self[p]) for p in candidates if self[p] is not None]

    def export_values(self) -> dict:
        return self.grid.copy()

    def import_values(self, value: dict):
        self.grid = value.copy()

    @property
    def width(self) -> int:
        return self.extents[0][1] - self.extents[0][0] + 1

    @property
    def height(self) -> int:
        return self.extents[1][1] - self.extents[1][0] + 1

    def _calculate_extents(self, newest_key=None):
        if not len(self.grid.keys()):
            self.extents = [[0, 0], [0, 0]]
            return

        if self.extents and newest_key:
            if newest_key[0] < self.extents[0][0]:
                self.extents[0][0] = newest_key[0]
            if newest_key[0] > self.extents[0][1]:
                self.extents[0][1] = newest_key[0]
            if newest_key[1] < self.extents[1][0]:
                self.extents[1][0] = newest_key[1]
            if newest_key[1] > self.extents[1][1]:
                self.extents[1][1] = newest_key[1]

            return

        self.extents = [
            [min([pos[0] for pos in self.grid.keys()]), max([pos[0] for pos in self.grid.keys()]) + 1],
            [min([pos[1] for pos in self.grid.keys()]), max([pos[1] for pos in self.grid.keys()]) + 1]
        ]

    @staticmethod
    def create_empty(width: int, height: int, default_value='.'):
        grid = SparseGrid({(x, y): default_value for y, line in enumerate(range(height))
                           for x, _ in enumerate(range(width))}, default_value)

        return grid

    @staticmethod
    def from_strings(strings: List[str], default_value='.'):
        grid = SparseGrid({(x, y): val for y, line in enumerate(strings)
                           for x, val in enumerate(line)}, default_value)

        return grid

    @staticmethod
    def from_number_strings(strings: List[str], default_value='.'):
        grid = SparseGrid({(x, y): int(val) for y, line in enumerate(strings)
                           for x, val in enumerate(line)}, default_value)

        return grid

    @staticmethod
    def from_array(rows: List[List[Union[any]]], default_value='.'):
        grid = SparseGrid({(x, y): val for y, line in enumerate(rows)
                           for x, val in enumerate(line)}, default_value)

        return grid

    @staticmethod
    def from_dict(grid_dict):
        grid = SparseGrid(grid_dict)

        grid._calculate_extents()

        return grid


class Grid3D(Grid):
    grid = {}

    extents: List[List[int]] = []

    invert_y_display = False

    default_value = '░░'

    _key_base_type = Tuple[Union[int, float], Union[int, float], Union[int, float]]

    def __getitem__(self, item: Union[Point3D, _key_base_type, slice]):
        if isinstance(item, slice):
            raise NotImplementedError
        elif isinstance(item, Tuple):
            return self.grid[Point3D(item[0], item[1], item[2])] if item in self.grid else None
        elif isinstance(item, Point3D):
            return self.grid[item] if item in self.grid else None
        else:
            raise TypeError('Invalid argument for grid indexing.')

    def __setitem__(self, key: Union[Point3D, _key_base_type], value):
        if isinstance(key, slice):
            raise NotImplementedError
        else:
            if isinstance(key, tuple):
                key = Point3D(key[0], key[1], key[2])

            self.grid[key] = value

        self._calculate_extents(key)

    def __str__(self):
        grid_str = ''

        ex, ey, ez = self.extents

        for y in range(ey[0], ey[1] + 1):
            for z in range(ez[0], ez[1] + 1):
                for x in range(ex[0], ex[1] + 1):
                    grid_str += self.grid[(x, y, z)] if (x, y, z) in self.grid else self.default_value

                grid_str += '  '
            grid_str += '\n'

        return grid_str

    def neighbors(self, pos: Point):
        x0, y0, z0 = pos

        candidates = [
            (x0 - 1, y0, z0),
            (x0 + 1, y0, z0),
            (x0, y0 - 1, z0),
            (x0, y0 + 1, z0),
            (x0, y0, z0 - 1),
            (x0, y0, z0 + 1)
        ]
        return [self[p] for p in candidates if self[p] is not None]

    @property
    def width(self) -> int:
        return self.extents[0][1] - self.extents[0][0] + 1

    @property
    def depth(self) -> int:
        return self.extents[1][1] - self.extents[1][0] + 1

    @property
    def height(self) -> int:
        return self.extents[2][1] - self.extents[2][0] + 1

    def _calculate_extents(self, newest_key=None):
        if not len(self.grid.keys()):
            self.extents = [[0, 0], [0, 0], [0, 0]]
            return

        if self.extents and newest_key:
            if newest_key[0] < self.extents[0][0]:
                self.extents[0][0] = newest_key[0]
            if newest_key[0] > self.extents[0][1]:
                self.extents[0][1] = newest_key[0]

            if newest_key[1] < self.extents[1][0]:
                self.extents[1][0] = newest_key[1]
            if newest_key[1] > self.extents[1][1]:
                self.extents[1][1] = newest_key[1]

            if newest_key[2] < self.extents[2][0]:
                self.extents[2][0] = newest_key[2]
            if newest_key[2] > self.extents[2][1]:
                self.extents[2][1] = newest_key[2]

            return

        self.extents = [
            [min([pos.x for pos in self.grid.keys()]), max([pos.x for pos in self.grid.keys()])],
            [min([pos.y for pos in self.grid.keys()]), max([pos.y for pos in self.grid.keys()])],
            [min([pos.z for pos in self.grid.keys()]), max([pos.z for pos in self.grid.keys()])]
        ]

    @staticmethod
    def create_empty(width: int, depth: int, height: int, default_value='.'):
        grid = Grid3D({}, default_value)
        grid.default_value = default_value

        return grid

    @staticmethod
    def from_strings(strings: List[str], default_value='.'):
        raise NotImplementedError

    @staticmethod
    def from_number_strings(strings: List[str], default_value='.'):
        raise NotImplementedError

    @staticmethod
    def from_array(rows: List[List[Union[any]]], default_value='.'):
        raise NotImplementedError

    @staticmethod
    def from_dict(grid_dict, default_value='.'):
        grid = Grid3D(grid_dict, default_value)

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
        return Point(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    elif 0 <= u <= 1:
        return Point(x3 + u * (x4 - x3), y3 + t * (y4 - y3))
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
