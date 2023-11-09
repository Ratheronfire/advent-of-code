from typing import List

from puzzle_base import PuzzleBase


class Sue:
    id: int
    values: dict[str, int]

    def __init__(self, id):
        self.id = id

        self.values = {
            'children': -1,
            'cats': -1,
            'samoyeds': -1,
            'pomeranians': -1,
            'akitas': -1,
            'vizslas': -1,
            'goldfish': -1,
            'trees': -1,
            'cars': -1,
            'perfumes': -1
        }

    def __setitem__(self, key, value):
        self.values[key] = value

    def __getitem__(self, item):
        return self.values[item]


class Puzzle(PuzzleBase):
    year = 2015
    day = 16

    sues: list[Sue]

    matching_data = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    def reset(self):
        self.sues = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            parts = line.replace(':', '').replace(',', '').split(' ')

            sue = Sue(int(parts[1]))

            for j in range(2, len(parts), 2):
                sue[parts[j]] = int(parts[j+1])

            self.sues.append(sue)

    def find_candidates(self):
        candidate_sues = self.sues.copy()

        for sue in self.sues:
            for key in sue.values.keys():
                actual = sue[key]
                expected = self.matching_data[key]

                if actual == -1:
                    continue

                if actual != expected:
                    candidate_sues.remove(sue)
                    break

        return candidate_sues

    def find_candidates_part2(self):
        candidate_sues = self.sues.copy()

        for sue in self.sues:
            for key in sue.values.keys():
                actual = sue[key]
                expected = self.matching_data[key]

                if actual == -1:
                    continue

                if key in ['cats', 'trees']:
                    if actual <= expected:
                        candidate_sues.remove(sue)
                        break
                elif key in ['pomeranians', 'goldfish']:
                    if actual >= expected:
                        candidate_sues.remove(sue)
                        break
                elif actual != expected:
                    candidate_sues.remove(sue)
                    break

        return candidate_sues

    def get_day_1_answer(self, use_sample=False) -> str:
        sue = self.find_candidates()[0]
        return str(sue.id)

    def get_day_2_answer(self, use_sample=False) -> str:
        sue = self.find_candidates_part2()[0]
        return str(sue.id)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.run())
