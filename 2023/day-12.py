from enum import Enum
from typing import List

from puzzle_base import PuzzleBase


class GearRow:
    def __init__(self, gears: list[str], runs: list[int]):
        self.gears = gears
        self.runs = runs

    def __str__(self):
        return f'{self.gears} {self.runs}'

    def get_row_margin(self):
        return len(self.gears) - sum(self.runs) - (len(self.runs) - 1)

    def simplify(self):
        possible_regions = []
        current_region = []

        run_lengths: list[int] = self.runs.copy()

        # finding any runs that are constrained by the row size
        # if a run's min/max positions overlap, the overlap area must be marked
        row_margin = self.get_row_margin()

        offset = 0

        if row_margin == 0:
            # Only one possible solution, so no need to think about this one
            self.gears = []
            self.runs = []

            return

        for run in self.runs:
            if run >= row_margin:
                for i in range(row_margin + offset, run + offset):
                    self.gears[i] = '#'
            offset += run + 1

        # splitting the gear array on operational gears
        gears = self.gears.copy()
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

        self.gears = simplified_gears[1:]
        self.runs = run_lengths

    def is_valid(self) -> bool:
        current_run = 0

        gears = self.gears.copy()
        gears.append('.')  # padding to make testing at the edge easier

        runs_to_test = self.runs.copy()

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
            self.gear_rows.append(GearRow(
                [g for g in gears],
                [int(r) for r in broken_runs.split(',')]
            ))

    def get_working_permutations(self, gear_row: GearRow):
        if not len(gear_row.runs):
            return 1  # this row is already satisfied

        if '?' not in gear_row.gears:
            # print(''.join(gear_row.gears), gear_row.runs, f' - Is Valid: {self.is_row_valid(gear_row)}')
            return int(gear_row.is_valid())
        else:
            next_unknown = gear_row.gears.index('?')

            broken_row = gear_row.gears.copy()
            broken_row[next_unknown] = '#'
            is_broken_valid = self.get_working_permutations(GearRow(broken_row, gear_row.runs))

            working_row = gear_row.gears.copy()
            working_row[next_unknown] = '.'
            is_working_valid = self.get_working_permutations(GearRow(working_row, gear_row.runs))

            return int(is_broken_valid) + int(is_working_valid)

    def expand_rows(self):
        new_rows = []

        for row in self.gear_rows:
            new_gears = []
            new_runs = []

            for i in range(5):
                new_gears += row.gears.copy() + ['?']
                new_runs += row.runs.copy()

            new_rows.append(GearRow(new_gears[:-1], new_runs))

        self.gear_rows = new_rows

    def calculate_solutions(self):
        total = 0

        for row in self.gear_rows:
            print(row)
            row.simplify()
            print(row)

            solutions = self.get_working_permutations(row)
            print(f'Solutions: {solutions}')
            print('\n')

            total += solutions

        return total

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.calculate_solutions())

    def get_part_2_answer(self, use_sample=False) -> str:
        return ''

        self.expand_rows()
        return str(self.calculate_solutions())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
