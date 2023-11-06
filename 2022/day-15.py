import random
import re
from copy import deepcopy
from typing import List, Optional

import shapely
from shapely.geometry import Polygon

from helpers.grid import Grid
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 15

    grid: Grid

    sensor_beacons = {}
    sensor_distances = {}

    unoccupied_tiles = set()
    beaconless_polygons: Polygon

    def reset(self):
        self.grid = Grid.create_empty(0, 0, '░░')

        self.sensor_beacons = {}
        self.sensor_distances = {}

        self.unoccupied_tiles = set()
        self.beaconless_polygons = Polygon()

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i].strip()

            if line == '':
                continue

            point_data = re.match(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)', line)

            sensor = (int(point_data[1]), int(point_data[2]))
            beacon = (int(point_data[3]), int(point_data[4]))

            self.grid[sensor] = 'SS'
            self.grid[beacon] = 'BB'

            self.sensor_beacons[sensor] = beacon
            self.sensor_distances[sensor] = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

    def try_marking(self, point):
        if not self.grid[point] or self.grid[point] == '░░':
            self.grid[point] = '██'

    def mark_beaconles_spots(self, sensor_pos):
        beacon = self.sensor_beacons[sensor_pos]

        distance = abs(beacon[0] - sensor_pos[0]) + abs(beacon[1] - sensor_pos[1])

        for x in range(sensor_pos[0] - distance - 1, sensor_pos[0] + distance + 1):
            self.try_marking((x, sensor_pos[1]))

            for y in range(distance - abs(x - sensor_pos[0]) + 1):
                self.try_marking((x, sensor_pos[1] + y))
                self.try_marking((x, sensor_pos[1] - y))

    def get_beaconless_polygon(self, sensor_pos):
        beacon = self.sensor_beacons[sensor_pos]

        distance = abs(beacon[0] - sensor_pos[0]) + abs(beacon[1] - sensor_pos[1])

        x0, y0 = sensor_pos

        corner_polygon = Polygon([
            (x0 + distance - 1, y0),
            (x0, y0 - distance + 1),
            (x0 - distance + 1, y0),
            (x0, y0 + distance - 1)
        ])

        return corner_polygon

    def find_beaconless_tiles_in_row(self, sensor_pos, y_to_scan):
        beacon = self.sensor_beacons[sensor_pos]

        distance = abs(beacon[0] - sensor_pos[0]) + abs(beacon[1] - sensor_pos[1])
        disntance_to_y = sensor_pos[1] - y_to_scan

        if abs(disntance_to_y) > distance:
            return

        remaining_distance = distance - abs(disntance_to_y)

        for x in range(sensor_pos[0] - remaining_distance, sensor_pos[0] + remaining_distance + 1):
            point = (x, y_to_scan)
            if not self.grid[point] or self.grid[point] == '░░':
                self.unoccupied_tiles.add(point)

    def get_day_1_answer(self, use_sample=False) -> str:
        y_to_scan = 10 if use_sample else 2000000

        key_len = len(self.sensor_beacons.keys())
        for point in self.sensor_beacons.keys():
            self.find_beaconless_tiles_in_row(point, y_to_scan)

        return str(len(self.unoccupied_tiles))

    def get_day_2_answer(self, use_sample=False) -> str:
        distress_point = (-1, -1)

        limit = 20 if use_sample else 4000000

        valid_polygon = Polygon([(0, 0), (limit, 0), (limit, limit), (0, limit)])

        for sensor_point in self.sensor_beacons.keys():
            beaconless_polygon = self.get_beaconless_polygon(sensor_point)
            valid_polygon = valid_polygon.difference(beaconless_polygon)

        polygon_points = sorted([p for p in shapely.get_coordinates(valid_polygon)], key=lambda p: (p[0], p[1]))

        for polygon_point in polygon_points:
            p0, p1 = polygon_point
            if self.grid[(p0 + 2, p1)] and self.grid[(p0 + 2, p1)] in ['SS', 'BB', '██']:
                continue

            if [p for p in polygon_points if p[0] == p0 + 4 and p[1] == p1] and \
                    [p for p in polygon_points if p[0] == p0 + 2 and p[1] == p1 - 2] and \
                    [p for p in polygon_points if p[0] == p0 + 2 and p[1] == p1 + 2]:
                distress_point = (int(p0 + 2), int(p1))
                break

        return str((distress_point[0] * 4000000) + distress_point[1])


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())