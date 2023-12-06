import re
import sys
from typing import List

from puzzle_base import PuzzleBase


CATEGORIES = [
    'seed',
    'soil',
    'fertilizer',
    'water',
    'light',
    'temperature',
    'humidity',
    'location'
]


class NumberMap:
    def __init__(self, source_start: int, dest_start: int, length: int):
        self.source_start = source_start
        self.dest_start = dest_start
        self.length = length


class CategoryMap:
    def __init__(self, from_category: str, to_category: str, number_maps: list[NumberMap]):
        self.from_category = from_category
        self.to_category = to_category
        self.number_maps = number_maps


class Puzzle(PuzzleBase):
    year = 2023
    day = 5

    base_seeds: list[int]
    category_maps: list[CategoryMap]

    def reset(self):
        self.base_seeds = []
        self.category_maps = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.base_seeds = [int(seed) for seed in input_data[0].split()[1:]]

        i = 2
        while i < len(input_data):
            _, from_category, to_category, _ = re.split(r'(.+)-to-(.+) map:', input_data[i])
            number_maps = []
            i += 1

            while input_data[i] != '':
                dest_start, source_start, length = [int(num) for num in input_data[i].split()]
                number_maps.append(NumberMap(source_start, dest_start, length))

                i += 1

            self.category_maps.append(CategoryMap(from_category, to_category, number_maps))
            i += 1

    def convert_to_category(self, from_category: str, to_category: str, num: int) -> int:
        category_map = [map for map in self.category_maps if map.to_category == to_category and map.from_category == from_category][0]

        for number_map in category_map.number_maps:
            if number_map.source_start <= num <= number_map.source_start + number_map.length:
                offset = num - number_map.source_start
                return number_map.dest_start + offset

        return num

    def convert_to_location(self, num: int) -> int:
        for i in range(len(CATEGORIES) - 1):
            num = self.convert_to_category(CATEGORIES[i], CATEGORIES[i + 1], num)

        return num

    def test_vertices(self, category: str, vertex_min: int, vertex_max: int):
        if category == CATEGORIES[-1]:
            return vertex_min

        category_index = CATEGORIES.index(category)
        next_category = CATEGORIES[category_index + 1]
        category_map = self.category_maps[category_index]

        destinations = []

        if vertex_min == vertex_max:
            destinations.append(self.convert_to_category(category, next_category, vertex_min))
        else:
            next_vertices = set()
            next_vertices.add(vertex_min)
            next_vertices.add(vertex_max)

            for number_map in category_map.number_maps:
                if vertex_min <= number_map.source_start <= vertex_max:
                    next_vertices.add(number_map.source_start)
                if vertex_min <= number_map.source_start + number_map.length <= vertex_max:
                    next_vertices.add(number_map.source_start + number_map.length)

            next_vertices = sorted(next_vertices)

            for i in range(len(next_vertices) - 1):
                destinations.append(self.test_vertices(next_category,
                                                       self.convert_to_category(category, next_category, next_vertices[i]),
                                                       self.convert_to_category(category, next_category, next_vertices[i+1])))

        return min(destinations)

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(min([self.convert_to_location(seed) for seed in self.base_seeds]))

    def get_part_2_answer(self, use_sample=False) -> str:
        seed_pairs = [(self.base_seeds[i], self.base_seeds[i+1]) for i in range(0, len(self.base_seeds), 2)]
        seed_pairs = sorted(seed_pairs, key=lambda seed: seed[0])

        return str(min([self.test_vertices(CATEGORIES[0], pair[0], pair[0] + pair[1]) for pair in seed_pairs]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
