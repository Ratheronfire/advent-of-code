import sys
from typing import List, Tuple, Optional

from puzzle_base import PuzzleBase


class Node(object):
    x: int
    y: int

    elevation: int
    distance: int

    last_node: 'Node' = None
    next_node_in_path: 'Node' = None

    is_start = False
    is_end = False

    def __init__(self, x: int, y: int, elevation: int):
        self.x = x
        self.y = y

        self.elevation = elevation
        self.distance = sys.maxsize

    def __str__(self):
        return '(%d, %d) - %d' % (self.x, self.y, self.elevation)


class Map(object):
    nodes: List[List[Node]]

    start_pos = (0, 0)
    end_pos = (0, 0)

    def __init__(self, map_data: List[str]):
        self.nodes = []

        for i in range(len(map_data)):
            line = map_data[i].strip()

            if line == '':
                continue

            node_row = []

            for j in range(len(line)):
                char = line[j]
                node_row.append(Node(j, i, ord('z') - ord(char) if char not in 'SE' else 0))

            self.nodes.append(node_row)

            if 'S' in line:
                row_index = line.index('S')
                self.start_pos = (row_index, i)
                self.nodes[i][row_index].is_start = True
                self.nodes[i][row_index].elevation = ord('z') - ord('a') - 1
                self.nodes[i][row_index].distance = 0

            if 'E' in line:
                row_index = line.index('E')
                self.end_pos = (row_index, i)
                self.nodes[i][row_index].is_end = True

    def get_node(self, x: int, y: int) -> Optional[Node]:
        if x < 0 or x >= len(self.nodes[0]) or y < 0 or y >= len(self.nodes):
            return None

        return self.nodes[y][x]

    def get_start_node(self) -> Node:
        return self.nodes[self.start_pos[1]][self.start_pos[0]]

    def get_end_node(self) -> Node:
        return self.nodes[self.end_pos[1]][self.end_pos[0]]

    def set_start(self, new_start_pos):
        old_start = self.nodes[self.start_pos[1]][self.start_pos[0]]

        old_start.is_start = False
        old_start.elevation = ord('z') - ord('a')
        old_start.distance = sys.maxsize

        self.start_pos = new_start_pos

        new_start = self.nodes[self.start_pos[1]][self.start_pos[0]]

        new_start.is_start = True
        new_start.elevation = ord('z') - ord('a')
        new_start.distance = 0

    def __str__(self):
        map_str = ''

        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                node = self.nodes[i][j]

                if node.is_end:
                    map_str += 'E'
                    continue

                if node.next_node_in_path:

                    node_offset = str(node.next_node_in_path.x - node.x) + str(node.next_node_in_path.y - node.y)

                    map_str += {
                        '01': 'v',
                        '0-1': '^',
                        '10': '>',
                        '-10': '<'
                    }[node_offset]
                else:
                    map_str += '.'

            map_str += '\n'

        return map_str


class Puzzle(PuzzleBase):
    year = 2022
    day = 12

    map: Map

    movements = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]

    def reset(self):
        pass

    def prepare_data(self, input_data: List[str], current_part: int):
        self.map = Map(input_data)

    def calc_path(self):
        node_queue = []

        for row in self.map.nodes:
            for node in row:
                if not node.is_start:
                    node.distance = sys.maxsize
                node.last_node = None
                node.next_node_in_path = None

                node_queue.append(node)

        while len(node_queue):
            node_queue = sorted(node_queue, key=lambda node: node.distance, reverse=True)
            node = node_queue.pop()

            for movement in self.movements:
                next_node_coords = (node.y + movement[0], node.x + movement[1])
                next_node = self.map.get_node(next_node_coords[1], next_node_coords[0])

                if not next_node or next_node not in node_queue or node.elevation - next_node.elevation > 1:
                    continue

                movement_cost = node.distance + 1
                if movement_cost < next_node.distance:
                    next_node.distance = movement_cost
                    next_node.last_node = node

    def retrace_path(self) -> int:
        current_node = self.map.get_end_node()
        start_node = self.map.get_start_node()

        path_len = 0
        while current_node != start_node:
            if not current_node or not current_node.last_node:
                return sys.maxsize

            current_node.last_node.next_node_in_path = current_node

            current_node = current_node.last_node
            path_len += 1

        return path_len

    def get_day_1_answer(self, use_sample=False) -> str:
        self.calc_path()

        path_len = self.retrace_path()

        return str(path_len)

    def get_day_2_answer(self, use_sample=False) -> str:
        a_candidates = [self.map.start_pos]
        a_distances = []

        for i in range(len(self.map.nodes)):
            for j in range(len(self.map.nodes[i])):
                node = self.map.nodes[i][j]

                if node.elevation == ord('z') - ord('a'):
                    a_candidates.append((j, i))

        for candidate in a_candidates:
            self.map.set_start(candidate)
            self.calc_path()

            a_distances.append(self.retrace_path())

            print('Tested %d/%d paths.' % (a_candidates.index(candidate) + 1, len(a_candidates)))

        return str(min(a_distances))


puzzle = Puzzle()
print(puzzle.test_and_run())
