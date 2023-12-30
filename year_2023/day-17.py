import functools
import sys
from typing import List

from helpers.grid import Point
from helpers.pathing_grid import PathingGrid, IntNode
from puzzle_base import PuzzleBase

MOVEMENTS = [
    Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)
]


class Puzzle(PuzzleBase):
    year = 2023
    day = 17

    grid: PathingGrid

    def reset(self):
        self.grid = PathingGrid.create_empty(0, 0)

    def prepare_data(self, input_data: List[str], current_part: int):
        self.grid = PathingGrid.from_strings(input_data, node_type=IntNode)

        self.grid.set_start(Point(0, 0))
        self.grid.set_end(Point(self.grid.extents[0][1], self.grid.extents[1][1]))

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

            for movement in MOVEMENTS:
                next_node_coords = node.pos + movement
                next_node = self.grid[next_node_coords]

                if not next_node or next_node not in node_queue:
                    continue

                # last_positions = []
                # past_node = next_node
                # for i in range(3):
                #     past_node = past_node.last_node
                #
                #     if not past_node:
                #         break
                #
                #     last_positions.append(past_node.pos)
                #
                # if len(last_positions) == 3 and (
                #     all([pos.x == node.pos.x for pos in last_positions]) or
                #     all([pos.y == node.pos.y for pos in last_positions])
                # ):
                #     print(f'Can\'t continue from {node.pos} to {next_node.pos}.')
                #     continue

                movement_cost = node.distance + next_node.value
                if movement_cost < next_node.distance:
                    next_node.distance = movement_cost
                    next_node.last_node = node

        return True

    def retrace_path(self, start_coords) -> int:
        # New algorithm:
        # Start at (0, 0)
        # seen_nodes = []
        # candidate_nodes = []
        # While not at end:
        #   add current to seen_nodes
        #   add all unseeen neighbors to candidate_nodes, seen_nodes
        #   select best neighbor
        #   if last three neighbors in same path as best neighbor:
        #       invalidate it
        #       select second best
        #   increment steps taken
        #   clear candidate_nodes

        current_node = self.grid[start_coords]
        goal_node = self.grid.get_end_node()

        heat_loss = 0
        seen_nodes = [start_coords]
        while current_node != goal_node:
            if not current_node or not current_node.last_node:
                return sys.maxsize

            lookahead_node = current_node
            best_nodes = []

            for i in range(3):
                if lookahead_node is None:
                    break

                neighbors = [neighbor for neighbor in self.grid.neighbors(lookahead_node.pos) \
                             if neighbor[0] not in seen_nodes]
                neighbors = sorted(neighbors, key=lambda n: n[1].distance)

                for neighbor in neighbors:
                    seen_nodes.append(neighbor[0])

                best_nodes.append(neighbors[0][1])
                lookahead_node = lookahead_node.last_node

            if len(best_nodes) == 3 and (
                    all([node.pos.x == current_node.pos.x for node in best_nodes]) or
                    all([node.pos.y == current_node.pos.y for node in best_nodes])):
                best_nodes = best_nodes[:-1]

            for node in best_nodes:
                heat_loss += node.value

            current_node = best_nodes[-1]

        return heat_loss

    @functools.lru_cache(maxsize=None)
    def get_heat_loss(self, x, y, heat_so_far=0, recent_points=tuple(), recent_paths=tuple()) -> int:
        point = Point(x, y)
        node = self.grid[x, y]

        if not node.is_start:
            heat_so_far = heat_so_far + node.value

        if node.is_end:
            return heat_so_far

        neighbors = [n for n in self.grid.neighbors(Point(x, y)) if n[0] not in recent_points]

        if len(recent_paths) == 3 and all([p == recent_paths[0] for p in recent_paths]):
            neighbors = [n for n in neighbors if (n[0][0] - x, n[0][1] - y) != recent_paths[0]]

        if not len(neighbors):
            return sys.maxsize

        neighbor_costs = []
        for neighbor in neighbors:
            if neighbor[0] in recent_points:
                direct_heat_loss = node.value - neighbor[1].value

                if direct_heat_loss >= len(recent_points) - recent_points.index(neighbor[0]):
                    return sys.maxsize  # this route is becoming a loop

            new_points = list(recent_points) + [(x, y)]

            new_paths = list(recent_paths) + [(neighbor[0][0] - x, neighbor[0][1] - y)]
            new_paths = new_paths[-3:]

            neighbor_costs.append(self.get_heat_loss(neighbor[1].pos.x, neighbor[1].pos.y,
                                                     heat_so_far + neighbor[1].value,
                                                     tuple(new_points),
                                                     tuple(new_paths)))

        return min(neighbor_costs)

    def get_part_1_answer(self, use_sample=False) -> str:
        self.calc_path()

        return str(self.retrace_path((0, 0)))

        # return str(self.get_heat_loss(0, 0))

    def get_part_2_answer(self, use_sample=False) -> str:
        return ''


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
