import math
import re
from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2023
    day = 8

    path: str
    rooms: dict[str, tuple[str, str]]

    def reset(self):
        self.path = ''
        self.rooms = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        self.path = input_data[0]

        for i in range(2, len(input_data)):
            line = input_data[i]

            if line != '':
                room_values = re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', line)
                self.rooms[room_values[1]] = (room_values[2], room_values[3])

    def find_sync_period(self):
        navigations = 0
        current_rooms = [r for r in self.rooms if r[-1] == 'A']

        visit_times = [-1 for i in range(len(current_rooms))]

        while not all([v != -1 for v in visit_times]):
            next_dir = self.path[navigations % len(self.path)]

            navigations += 1

            for i in range(len(current_rooms)):
                current_rooms[i] = self.rooms[current_rooms[i]][0 if next_dir == 'L' else 1]

                if current_rooms[i][-1] == 'Z' and visit_times[i] == -1:
                    visit_times[i] = navigations

        return math.lcm(*visit_times)

    def follow_path(self):
        navigations = 0
        current_room = 'AAA'

        while current_room != 'ZZZ':
            next_dir = self.path[navigations % len(self.path)]
            current_room = self.rooms[current_room][0 if next_dir == 'L' else 1]
            navigations += 1

        return navigations

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.follow_path())

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.find_sync_period())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
