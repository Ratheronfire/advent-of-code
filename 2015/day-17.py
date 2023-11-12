from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 17

    containers: list[int]

    def reset(self):
        self.containers = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line.isnumeric():
                self.containers.append(int(line))

    def find_filling_sets(self, available_containers: tuple, liters_left: int) -> list:
        return self._test_filling_sets(available_containers, liters_left, [])

    def _test_filling_sets(self, available_containers: tuple, liters_left: int, partial_set: list) -> list:
        found_sets = []

        if liters_left < 0:
            return found_sets

        if liters_left == 0:
            found_sets.append(partial_set)

        if len(available_containers) == 0 or liters_left == 0:
            return found_sets

        sub_tuple = tuple(list(available_containers)[1:])

        new_partial_set = partial_set.copy()
        new_partial_set.append(available_containers[0])

        test_with = self._test_filling_sets(sub_tuple, liters_left - available_containers[0], new_partial_set)
        test_without = self._test_filling_sets(sub_tuple, liters_left, partial_set)
        found_sets += test_with
        found_sets += test_without

        return found_sets

    def get_day_1_answer(self, use_sample=False) -> str:
        liters = 25 if use_sample else 150

        return str(len(self.find_filling_sets(tuple(self.containers), liters)))

    def get_day_2_answer(self, use_sample=False) -> str:
        liters = 25 if use_sample else 150

        filling_sets = self.find_filling_sets(tuple(self.containers), liters)
        filling_sets = sorted(filling_sets, key=lambda filling_set: len(filling_set))

        shortest_size = len(filling_sets[0])

        return str(len([s for s in filling_sets if len(s) == shortest_size]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
