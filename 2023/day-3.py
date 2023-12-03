from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2023
    day = 3

    schematic: Grid

    def reset(self):
        self.schematic = Grid.create_empty(0, 0, default_value='.')

    def prepare_data(self, input_data: List[str], current_part: int):
        self.schematic = Grid.from_strings(input_data)

    def get_number_and_parts(self, number_pos: Point):
        neighbors = []
        num_str = ''

        x, y = number_pos

        while x < self.schematic.extents[0][1] + 1:
            if not self.schematic[(x, y)].isnumeric():
                break

            for neighbor in self.schematic.neighbors(Point(x, y), include_diagonals=True):
                if not neighbor[0] in [n[0] for n in neighbors]:
                    neighbors.append(neighbor)
            num_str += self.schematic[(x, y)]
            x += 1

        return (int(num_str) if num_str.isnumeric() else -1), \
            [n for n in neighbors if not n[1].isnumeric() and n[1] != '.']

    def get_day_1_answer(self, use_sample=False) -> str:
        total = 0

        for y in range(self.schematic.extents[1][1] + 1):
            for x in range(self.schematic.extents[0][1] + 1):
                if self.schematic[(x, y)] == '.':
                    continue

                if x > 0 and self.schematic[(x - 1, y)].isnumeric():
                    continue  # this is part of a number we already saw

                num, adjacent_parts = self.get_number_and_parts(Point(x, y))

                if len(adjacent_parts):
                    total += num

        return str(total)

    def get_day_2_answer(self, use_sample=False) -> str:
        part_adjacencies = {}

        for y in range(self.schematic.extents[1][1] + 1):
            for x in range(self.schematic.extents[0][1] + 1):
                if self.schematic[(x, y)] == '.':
                    continue

                if x > 0 and self.schematic[(x - 1, y)].isnumeric():
                    continue  # this is part of a number we already saw

                num, adjacent_parts = self.get_number_and_parts(Point(x, y))

                for part in adjacent_parts:
                    if part[1] == '*':
                        if part[0] in part_adjacencies:
                            part_adjacencies[part[0]].append(num)
                        else:
                            part_adjacencies[part[0]] = [num]

        total = 0

        for adjacency in part_adjacencies.values():
            if len(adjacency) == 2:
                total += adjacency[0] * adjacency[1]

        return str(total)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
