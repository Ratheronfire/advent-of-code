import re
from typing import List

from helpers.list_helpers import ListHelper
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 13

    guests: list[str] = []
    happiness_pairs: dict[tuple[str, str], int]

    def reset(self):
        self.guests = []
        self.happiness_pairs = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            sections = re.search(r'(.+) would (gain|lose) (\d+) happiness units? by sitting next to (.+).', line)
            self.happiness_pairs[(sections[1], sections[4])] = int(sections[3]) * (1 if sections[2] == 'gain' else -1)

            if sections[1] not in self.guests:
                self.guests.append(sections[1])
            if sections[4] not in self.guests:
                self.guests.append(sections[4])

    def get_happiness(self, layout):
        total = 0

        for i in range(len(layout)):
            a = layout[i]
            b = layout[i+1] if i < len(layout) - 1 else layout[0]
            total += self.happiness_pairs[(a, b)]
            total += self.happiness_pairs[(b, a)]

        return total

    def get_day_1_answer(self, use_sample=False) -> str:
        permutations = ListHelper().get_permutations(self.guests, True)
        return str(max([self.get_happiness(permutation) for permutation in permutations]))

    def get_day_2_answer(self, use_sample=False) -> str:
        for guest in self.guests:
            self.happiness_pairs[(guest, 'You')] = 0
            self.happiness_pairs[('You', guest)] = 0
        self.guests.append('You')

        permutations = ListHelper().get_permutations(self.guests, True)
        return str(max([self.get_happiness(permutation) for permutation in permutations]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
