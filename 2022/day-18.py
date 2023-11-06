from typing import List

from helpers.grid import Grid3D, Point3D
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 18

    grid: Grid3D

    def reset(self):
        self.grid = Grid3D.create_empty(0, 0, 0, default_value='.')

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            x, y, z = [int(num) for num in line.split(',')]
            self.grid[(x, y, z)] = '#'

    def get_day_1_answer(self, use_sample=False) -> str:
        surfaces = 0

        for point in self.grid.grid.keys():
            surfaces += 6 - len(self.grid.neighbors(point))

        return str(surfaces)

    def get_day_2_answer(self, use_sample=False) -> str:
        print(self.grid)

        surfaces = 0

        for point in self.grid.grid.keys():
            surfaces += 6 - len(self.grid.neighbors(point))

        enclosed_points = []
        unvisited_points = []
        hit_surfaces = set()
        point_queue = []

        extents_x, extents_y, extents_z = self.grid.extents
        for x in range(extents_x[0], extents_x[1] + 1):
            for y in range(extents_y[0], extents_y[1] + 1):
                for z in range(extents_z[0], extents_z[1] + 1):
                    if self.grid[(x, y, z)] != '#':
                        unvisited_points.append((x, y, z))

        while len(unvisited_points):
            hit_extents = False

            point_queue.append(unvisited_points[0])

            while len(point_queue):
                x, y, z = point = point_queue.pop()

                if point in unvisited_points:
                    unvisited_points.remove(point)

                if x in extents_x or y in extents_y or z in extents_z:
                    hit_extents = True

                for neighbor in [
                    (x - 1, y, z), (x + 1, y, z),
                    (x, y - 1, z), (x, y + 1, z),
                    (x, y, z - 1), (x, y, z + 1)
                ]:
                    nx, ny, nz = neighbor
                    if self.grid[neighbor] == '#':
                        hit_surfaces.add((point, neighbor))
                    elif (nx, ny, nz) in unvisited_points:
                        point_queue.append((nx, ny, nz))

            if not hit_extents:
                surfaces -= len(hit_surfaces)
            hit_surfaces = set()

        return str(surfaces)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
