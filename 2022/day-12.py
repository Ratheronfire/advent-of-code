import sys
from typing import List, Tuple, Optional, Union

from helpers.grid import Grid, Grid, Point
from puzzle_base import PuzzleBase


class Node:
    pos: Point

    char_code: str

    elevation: int
    distance: int

    last_node: 'Node' = None
    next_node_in_path: 'Node' = None

    is_start = False
    is_end = False

    def __init__(self, x, y, char_code: str):
        self.pos = Point(x, y)

        self.char_code = char_code

        self.elevation = (ord(char_code) - ord('a') if char_code not in 'SE' else 0)
        self.distance = sys.maxsize

    def __str__(self):
        return self.char_code


class Map(Grid):
    start_pos = (0, 0)
    end_pos = (0, 0)

    @staticmethod
    def create_empty(width: int, height: int, default_value='a'):
        map = Map({(x, y): Node(x, y, default_value) for y, line in enumerate(range(height))
                   for x, _ in enumerate(range(width))}, default_value)

        return map

    @staticmethod
    def from_strings(strings: List[str], default_value='.'):
        map = Map({(x, y): Node(x, y, val)
                   for y, line in enumerate(strings)
                   for x, val in enumerate(line)}, default_value)

        map.locate_start_end()

        return map

    def locate_start_end(self):
        for x in range(self.extents[0][1] + 1):
            for y in range(self.extents[1][1] + 1):
                node = self[(x, y)]

                if node.char_code == 'S':
                    self.start_pos = (x, y)
                    node.is_start = True
                    node.elevation = 0
                elif node.char_code == 'E':
                    self.end_pos = (x, y)
                    node.is_end = True
                    node.elevation = ord('z') - ord('a')
                    node.distance = 0

    def get_start_node(self) -> Node:
        return self.grid[self.start_pos]

    def get_end_node(self) -> Node:
        return self.grid[self.end_pos]

    def set_start(self, new_start_pos):
        old_start = self.get_start_node()

        old_start.is_start = False
        old_start.elevation = 0
        old_start.distance = sys.maxsize

        self.start_pos = new_start_pos

        new_start = self.grid[self.start_pos]

        new_start.is_start = True
        new_start.elevation = 0
        new_start.distance = 0

    # def __str__(self):
    #     map_str = ''
    #
    #     for i in range(len(self.nodes)):
    #         for j in range(len(self.nodes[i])):
    #             node = self.nodes[i][j]
    #
    #             if node.is_end:
    #                 map_str += 'E'
    #                 continue
    #
    #             if node.next_node_in_path:
    #
    #                 node_offset = str(node.next_node_in_path.x - node.x) + str(node.next_node_in_path.y - node.y)
    #
    #                 map_str += {
    #                     '01': '^',
    #                     '0-1': 'v',
    #                     '10': '<',
    #                     '-10': '>'
    #                 }[node_offset]
    #             else:
    #                 map_str += '.'
    #
    #         map_str += '\n'
    #
    #     return map_str


class Puzzle(PuzzleBase):
    year = 2022
    day = 12

    map: Map

    movements: list[Point] = [
        Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)
    ]

    def reset(self):
        pass

    def prepare_data(self, input_data: List[str], current_part: int):
        self.map = Map.from_strings(input_data)

    def calc_path(self):
        node_queue = []

        for x in range(self.map.extents[0][1] + 1):
            for y in range(self.map.extents[1][1] + 1):
                node = self.map[(x, y)]

                if not node.is_end:
                    node.distance = sys.maxsize
                node.last_node = None
                node.next_node_in_path = None

                node_queue.append(node)

        while len(node_queue):
            node_queue = sorted(node_queue, key=lambda node: node.distance, reverse=True)
            node = node_queue.pop()

            # if node.distance >= sys.maxsize:
            #     return False

            for movement in self.movements:
                next_node_coords = node.pos + movement
                next_node = self.map[next_node_coords]

                if not next_node or next_node not in node_queue or node.elevation - next_node.elevation > 1:
                    continue

                movement_cost = node.distance + 1
                if movement_cost < next_node.distance:
                    next_node.distance = movement_cost
                    next_node.last_node = node

        return True

    def retrace_path(self, goal_coords) -> int:
        current_node = self.map[goal_coords]
        goal_node = self.map.get_end_node()

        path_len = 0
        while current_node != goal_node:
            if not current_node or not current_node.last_node:
                return sys.maxsize

            current_node.last_node.next_node_in_path = current_node

            current_node = current_node.last_node
            path_len += 1

        return path_len

    def get_day_1_answer(self, use_sample=False) -> str:
        self.calc_path()

        path_len = self.retrace_path(self.map.start_pos)

        return str(path_len)

    def get_day_2_answer(self, use_sample=False) -> str:
        self.calc_path()

        a_candidates = []

        for x in range(self.map.extents[0][1] + 1):
            for y in range(self.map.extents[1][1] + 1):
                node = self.map[(x, y)]

                if node.elevation == 0:
                    a_candidates.append((x, y))

        path_lens = [self.retrace_path(candidate) for candidate in a_candidates]

        return str(min(path_lens))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
