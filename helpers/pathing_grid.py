import sys

from helpers.grid import Point, ArrayGrid


class Node:
    pos: Point

    char_code: str

    distance: int

    last_node: 'Node' = None
    next_node_in_path: 'Node' = None

    is_start = False
    is_end = False

    def __init__(self, x, y, char_code: str):
        self.pos = Point(x, y)
        self.char_code = char_code
        self.distance = sys.maxsize

    def __str__(self):
        if self.is_end:
            return 'E'

        if self.next_node_in_path:
            node_offset = str(self.next_node_in_path.pos.x - self.pos.x) +\
                          str(self.next_node_in_path.pos.y - self.pos.y)

            return {
                '01': '^',
                '0-1': 'v',
                '10': '<',
                '-10': '>'
            }[node_offset]

        return self.char_code

    def set_is_start(self, is_start: bool):
        self.is_start = is_start

        if is_start:
            self.distance = 0

    def set_is_end(self, is_end: bool):
        self.is_end = is_end

        if is_end:
            self.distance = 0


class ElevationNode(Node):
    elevation: int

    def __init__(self, x, y, char_code: str):
        super().__init__(x, y, char_code)

        self.elevation = (ord(char_code) - ord('a') if char_code not in 'SE' else 0)

    def set_is_start(self, is_start: bool):
        super().set_is_start(is_start)

        if is_start:
            self.elevation = 0

    def set_is_end(self, is_end: bool):
        super().set_is_end(is_end)

        if is_end:
            self.elevation = ord('z') - ord('a')


class IntNode(Node):
    value: int

    def __init__(self, x, y, char_code: str):
        super().__init__(x, y, char_code)

        self.value = int(char_code)

    def set_is_start(self, is_start: bool):
        super().set_is_start(is_start)

        if is_start:
            self.value = 0


class PathingGrid(ArrayGrid):
    start_pos = Point(0, 0)
    end_pos = Point(0, 0)

    @staticmethod
    def create_empty(width: int, height: int, default_value='.'):
        grid = PathingGrid([], default_value)

        return grid

    @staticmethod
    def from_strings(strings: list[str], default_value='.', node_type=Node):
        grid = PathingGrid([[node_type(x, y, char) for x, char in enumerate(string)]
                            for y, string in enumerate(strings) if string != ''],
                           default_value)

        grid.locate_start_end()

        return grid

    def locate_start_end(self):
        for x in range(self.extents[0][1]):
            for y in range(self.extents[1][1]):
                node = self[(x, y)]

                if node.char_code == 'S':
                    self.start_pos = Point(x, y)
                    node.is_start = True
                    node.elevation = 0
                elif node.char_code == 'E':
                    self.end_pos = Point(x, y)
                    node.is_end = True
                    node.elevation = ord('z') - ord('a')
                    node.distance = 0

    def get_start_node(self) -> Node | None:
        if not self.start_pos:
            return None

        return self.grid[self.start_pos.y][self.start_pos.x]

    def get_end_node(self) -> Node | None:
        if not self.end_pos:
            return None

        return self.grid[self.end_pos.y][self.end_pos.x]

    def set_start(self, new_start_pos: Point):
        old_start = self.get_start_node()
        old_start.set_is_start(False)

        self.start_pos = new_start_pos

        new_start = self[self.start_pos]
        new_start.set_is_start(True)

    def set_end(self, new_end_pos: Point):
        old_end = self.get_end_node()
        old_end.set_is_end(False)

        self.end_pos = new_end_pos

        new_end = self[self.end_pos]
        new_end.set_is_end(True)
