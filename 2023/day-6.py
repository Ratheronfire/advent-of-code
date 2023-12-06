from functools import reduce
from typing import List

from puzzle_base import PuzzleBase


class Race:
    def __init__(self, time: int, distance: int):
        self.time = time
        self.distance = distance

    def get_distance(self, seconds_held: int):
        return max(0, (self.time - seconds_held) * seconds_held)


class Puzzle(PuzzleBase):
    year = 2023
    day = 6

    races: list[Race]

    def reset(self):
        self.races = []

    def prepare_data(self, input_data: List[str], current_part: int):
        times = input_data[0].split()[1:]
        distances = input_data[1].split()[1:]

        if current_part == 1:
            for i in range(len(times)):
                self.races.append(Race(int(times[i]), int(distances[i])))
        else:
            self.races.append(Race(int(''.join(times)), int(''.join(distances))))

    def get_winning_range(self, race: Race):
        i, j = 0, 0

        for i in range(1, race.time):
            if race.get_distance(i) > race.distance:
                break

        for j in range(race.time - 1, 0, -1):
            if race.get_distance(j) > race.distance:
                break

        return j - i + 1

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(reduce(lambda a, b: a * b, [self.get_winning_range(race) for race in self.races]))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.get_winning_range(self.races[0]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
