from typing import List

from helpers.grid import Grid
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 14

    grid: Grid

    sand_spawn_point = (500, 0)

    last_y_pos = -1

    def reset(self):
        self.grid = Grid.create_empty(1000, 1000, '.')

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            points = [[int(num) for num in pair.split(',')] for pair in line.split(' -> ')]

            for i in range(len(points) - 1):
                point = points[i]
                next_point = points[i+1]

                if point[1] > self.last_y_pos:
                    self.last_y_pos = point[1]
                if next_point[1] > self.last_y_pos:
                    self.last_y_pos = next_point[1]

                offset = (0, 0)
                if point[0] > next_point[0]:
                    offset = (-1, 0)
                elif point[0] < next_point[0]:
                    offset = (1, 0)
                elif point[1] > next_point[1]:
                    offset = (0, -1)
                elif point[1] < next_point[1]:
                    offset = (0, 1)

                while point != next_point:
                    self.grid[(point[0], point[1])] = '#'

                    point[0] += offset[0]
                    point[1] += offset[1]
                self.grid[(point[0], point[1])] = '#'  # last point

    def process_sand(self, current_pos, simulate_floor=False):
        x0, y0 = current_pos

        possible_destinations = [(x0, y0 + 1), (x0 - 1, y0 + 1), (x0 + 1, y0 + 1)]

        for destination in possible_destinations:
            if self.grid[destination] == '.' and (not simulate_floor or destination[1] < self.last_y_pos + 2):
                self.grid[current_pos] = '.'
                self.grid[destination] = 'o'

                current_pos = destination
                break

        return current_pos

    def simulate_sand(self, simulate_floor=False):
        sand_collected = 0

        current_sand_piece = (-1, -1)

        sand_done = False
        while not sand_done:
            if current_sand_piece == (-1, -1):
                current_sand_piece = (500, 0)

            new_position = self.process_sand(current_sand_piece, simulate_floor)

            if new_position == current_sand_piece:
                sand_collected += 1
                current_sand_piece = (-1, -1)

                if new_position == (500, 0):
                    sand_done = True
            elif not simulate_floor and new_position[1] > self.last_y_pos:
                sand_done = True
            else:
                current_sand_piece = new_position

        return sand_collected

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.simulate_sand(False))

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(self.simulate_sand(True))


puzzle = Puzzle()
print(puzzle.test_and_run())
