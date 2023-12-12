from enum import Enum
from typing import List

from puzzle_base import PuzzleBase


GearRow = tuple[list[str], list[int]]


class Puzzle(PuzzleBase):
    year = 2023
    day = 12

    gear_rows: list[GearRow]

    def reset(self):
        self.gear_rows = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            gears, broken_runs = line.split()
            self.gear_rows.append((
                [g for g in gears],
                [int(r) for r in broken_runs.split(',')]
            ))

    def get_row_margin(self, gear_row: GearRow):
        return len(gear_row[0]) - sum(gear_row[1]) - (len(gear_row[1]) - 1)

    def simplify_row(self, gear_row: GearRow) -> GearRow:
        possible_regions = []
        current_region = []

        run_lengths: list[int] = gear_row[1].copy()

        # finding any runs that are constrained by the row size
        # if a run's min/max positions overlap, the overlap area must be marked
        row_margin = self.get_row_margin(gear_row)

        offset = 0

        if row_margin == 0:
            return [], []  # Only one possible solution, so no need to think about this one

        for run in gear_row[1]:
            if run >= row_margin:
                for i in range(row_margin + offset, run + offset):
                    gear_row[0][i] = '#'
            offset += run + 1

        # splitting the gear array on operational gears
        gears = gear_row[0].copy()
        gears.append('.')

        for gear in gears:
            if gear == '.':
                if len(current_region):
                    possible_regions.append(current_region)
                    current_region = []
            else:
                current_region.append(gear)

        can_simplify = True
        while can_simplify:
            old_region_length = len(possible_regions)
            old_run_lengths = len(run_lengths)

            # removing any solved gear segments at the start of the array
            while len(possible_regions) and len(run_lengths) and \
                    len(possible_regions[0]) == run_lengths[0] and '#' in possible_regions[0]:
                possible_regions = possible_regions[1:]
                run_lengths = run_lengths[1:]

            # and now from the end
            while len(possible_regions) and len(run_lengths) and \
                    len(possible_regions[-1]) == run_lengths[-1] and '#' in possible_regions[-1]:
                possible_regions = possible_regions[:-1]
                run_lengths = run_lengths[:-1]

            # removing unfillable regions
            while len(possible_regions) and len(run_lengths) and \
                    len(possible_regions[0]) < run_lengths[0]:
                possible_regions = possible_regions[1:]
            while len(possible_regions) and len(run_lengths) and \
                    len(possible_regions[-1]) < run_lengths[-1]:
                possible_regions = possible_regions[:-1]

            if len(possible_regions) == old_region_length and len(run_lengths) == old_run_lengths:
                can_simplify = False

        simplified_gears = []
        for region in possible_regions:
            simplified_gears += ['.'] + region

        return simplified_gears[1:], run_lengths

    def is_row_valid(self, gear_row: GearRow) -> bool:
        current_run = 0

        gears = gear_row[0].copy()
        gears.append('.')  # padding to make testing at the edge easier

        runs_to_test = gear_row[1]

        for i, gear in enumerate(gears):
            if gear == '#':
                current_run += 1

                if current_run > runs_to_test[0]:
                    return False
            elif gear == '.' and current_run > 0:
                if current_run != runs_to_test[0]:
                    return False

                current_run = 0
                runs_to_test = runs_to_test[1:]

                if len(runs_to_test) == 0:
                    return '#' not in gears[i+1:]

        return False

    def get_working_permutations(self, gear_row: GearRow):
        if not len(gear_row[1]):
            return 1  # this row is already satisfied

        if '?' not in gear_row[0]:
            # print(''.join(gear_row[0]), gear_row[1], f' - Is Valid: {self.is_row_valid(gear_row)}')
            return int(self.is_row_valid(gear_row))
        else:
            next_unknown = gear_row[0].index('?')

            broken_row = gear_row[0].copy()
            broken_row[next_unknown] = '#'
            is_broken_valid = self.get_working_permutations((broken_row, gear_row[1]))

            working_row = gear_row[0].copy()
            working_row[next_unknown] = '.'
            is_working_valid = self.get_working_permutations((working_row, gear_row[1]))

            return int(is_broken_valid) + int(is_working_valid)

    def expand_rows(self):
        new_rows = []

        for row in self.gear_rows:
            new_gears = []
            new_runs = []

            for i in range(5):
                new_gears += row[0].copy() + ['?']
                new_runs += row[1].copy()

            new_rows.append((new_gears[:-1], new_runs))

        self.gear_rows = new_rows

    def get_part_1_answer(self, use_sample=False) -> str:
        total = 0

        for row in self.gear_rows:
            # print((''.join(row[0])), row[1])

            simplified_row = self.simplify_row(row)
            solutions = self.get_working_permutations(simplified_row)

            # print((''.join(simplified_row[0])), simplified_row[1], f' - Solutions: {solutions}')
            # print('\n')

            total += solutions

        return str(total)

    def get_part_2_answer(self, use_sample=False) -> str:
        self.expand_rows()

        total = 0

        for row in self.gear_rows:
            print((''.join(row[0])), row[1])

            simplified_row = self.simplify_row(row)
            solutions = self.get_working_permutations(simplified_row)

            print((''.join(simplified_row[0])), simplified_row[1], f' - Solutions: {solutions}')
            print('\n')

            total += solutions

        return str(total)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
