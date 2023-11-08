from typing import List

from puzzle_base import PuzzleBase


class City:
    id: str

    def __init__(self, id: str):
        self.id = id


class Puzzle(PuzzleBase):
    year = 2015
    day = 9

    cities = dict[str, City]
    city_paths = {}

    def reset(self):
        self.cities = {}
        self.city_paths = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            parts = line.split(' ')
            if parts[0] not in self.cities:
                self.cities[parts[0]] = City(parts[0])
            if parts[2] not in self.cities:
                self.cities[parts[2]] = City(parts[2])

            self.city_paths[(parts[0], parts[2])] = int(parts[4])
            self.city_paths[(parts[2], parts[0])] = int(parts[4]) # getting the reverse too

    def get_permutations(self, list: List) -> List:
        if len(list) < 2:
            return list

        if len(list) == 2:
            return [[list[0], list[1]], [list[1], list[0]]]

        permutations = []
        for elem in list:
            sublist = [e for e in list if e != elem]
            sub_permutations = self.get_permutations(sublist)

            for sub_permutation in sub_permutations:
                if [elem] + sub_permutation not in permutations:
                    permutations.append([elem] + sub_permutation)
                if sub_permutation + [elem] not in permutations:
                    permutations.append(sub_permutation + [elem])

        return permutations

    def get_distance(self, path: list[str]):
        total = 0

        for i in range(len(path) - 1):
            connection = (path[i], path[i + 1])
            if connection not in self.city_paths:
                return -1  # this path is impossible

            total += self.city_paths[connection]

        return total

    def get_day_1_answer(self, use_sample=False) -> str:
        permutations = self.get_permutations([c.id for c in self.cities.values()])
        distances = [self.get_distance(p) for p in permutations]

        return str(min([d for d in distances if d >= 0]))

    def get_day_2_answer(self, use_sample=False) -> str:
        permutations = self.get_permutations([c.id for c in self.cities.values()])
        distances = [self.get_distance(p) for p in permutations]

        return str(max([d for d in distances if d >= 0]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
