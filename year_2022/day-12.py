import sys
from typing import List, Tuple, Optional, Union

from helpers.grid import Grid, Grid, Point, ArrayGrid
from helpers.pathing_grid import PathingGrid, ElevationNode
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 12

    grid: PathingGrid

    movements: list[Point] = [
        Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)
    ]

    def reset(self):
        pass

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = PathingGrid.from_strings(input_data, node_type=ElevationNode)
        self.locate_start_end()

    def locate_start_end(self):
        for x in range(self.grid.extents[0][1]):
            for y in range(self.grid.extents[1][1]):
                node = self.grid[(x, y)]

                if node.char_code == 'S':
                    self.grid.set_start(Point(x, y))
                elif node.char_code == 'E':
                    self.grid.set_end(Point(x, y))

    def calc_path(self):
        node_queue = []

        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                node = self.grid[(x, y)]

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
                next_node = self.grid[next_node_coords]

                if not next_node or next_node not in node_queue or node.elevation - next_node.elevation > 1:
                    continue

                movement_cost = node.distance + 1
                if movement_cost < next_node.distance:
                    next_node.distance = movement_cost
                    next_node.last_node = node

        return True

    def retrace_path(self, goal_coords) -> int:
        current_node = self.grid[goal_coords]
        goal_node = self.grid.get_end_node()

        path_len = 0
        while current_node != goal_node:
            if not current_node or not current_node.last_node:
                return sys.maxsize

            current_node.last_node.next_node_in_path = current_node

            current_node = current_node.last_node
            path_len += 1

        return path_len

    def get_part_1_answer(self, use_sample=False) -> str:
        self.calc_path()

        path_len = self.retrace_path(self.grid.start_pos)

        if not self.is_silent:
            print(self.grid)

        return str(path_len)

    def get_part_2_answer(self, use_sample=False) -> str:
        self.calc_path()

        a_candidates = []

        for x in range(self.grid.extents[0][1] + 1):
            for y in range(self.grid.extents[1][1] + 1):
                node = self.grid[(x, y)]

                if node.elevation == 0:
                    a_candidates.append((x, y))

        path_lens = [self.retrace_path(candidate) for candidate in a_candidates]

        print(self.grid)

        return str(min(path_lens))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
