import re
from typing import List

from puzzle_base import PuzzleBase


class Reindeer:
    name: str
    speed: int
    fly_time: int
    rest_time: int

    @property
    def period_time(self) -> int:
        return self.fly_time + self.rest_time

    @property
    def period_distnace(self) -> int:
        return self.fly_time * self.speed

    def __init__(self, name, speed, fly_time, rest_time):
        self.name = name
        self.speed = speed
        self.fly_time = fly_time
        self.rest_time = rest_time


class Puzzle(PuzzleBase):
    year = 2015
    day = 14

    reindeer: list[Reindeer]

    def reset(self):
        self.reindeer = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            sections = re.search(r'(.+) can fly (\d+) km/s for (\d+) seconds?, but then must rest for (\d+) seconds?.', line)
            reindeer = Reindeer(sections[1], int(sections[2]), int(sections[3]), int(sections[4]))
            self.reindeer.append(reindeer)

    def get_reindeer_distance(self, reindeer: Reindeer, seconds: int):
        periods = seconds // reindeer.period_time
        period_remainder = seconds % reindeer.period_time

        return periods * reindeer.period_distnace + reindeer.speed * min(period_remainder, reindeer.fly_time)

    def get_day_1_answer(self, use_sample=False) -> str:
        seconds = 1000 if use_sample else 2503
        distances = [self.get_reindeer_distance(reindeer, seconds) for reindeer in self.reindeer]

        return str(max(distances))

    def get_day_2_answer(self, use_sample=False) -> str:
        seconds = 1000 if use_sample else 2503

        scores = {reindeer.name: 0 for reindeer in self.reindeer}

        for i in range(1, seconds + 1):
            distances = [(reindeer.name, self.get_reindeer_distance(reindeer, i)) for reindeer in self.reindeer]
            distances = sorted(distances, key=lambda r: r[1], reverse=True)
            distances = [d for d in distances if d[1] == distances[0][1]]

            for distance in distances:
                scores[distance[0]] += 1

        return str(max(scores.values()))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
