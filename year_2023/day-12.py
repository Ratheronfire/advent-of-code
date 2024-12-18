import functools
from enum import Enum
from typing import List, Union

from puzzle_base import PuzzleBase


class GearRow:
    def __init__(self, gears: Union[list[str], tuple[str]], runs: Union[list[int], tuple[int]]):
        self.gears = gears
        self.runs = runs

    def __str__(self):
        return f'{"".join(self.gears)} {",".join([str(r) for r in self.runs])}'

    def __hash__(self):
        return hash(''.join(self.gears))

    def get_row_margin(self):
        return len(self.gears) - sum(self.runs) - (len(self.runs) - 1)

    def is_valid(self, fail_if_more_broken_gears=True) -> bool:
        current_run = 0

        gears = list(self.gears).copy()
        gears.append('.')  # padding to make testing at the edge easier

        runs_to_test = list(self.runs).copy()

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
                    return '#' not in gears[i+1:] or not fail_if_more_broken_gears

        return False


def is_row_valid(gear_row: list[str], runs: list[int], allow_partial_solution: bool) -> bool:
    current_run = 0

    gears = list(gear_row).copy()
    gears.append('.')  # padding to make testing at the edge easier

    runs_to_test = list(runs).copy()

    for i, gear in enumerate(gears):
        if gear == '#':
            current_run += 1

            if current_run > runs_to_test[0]:
                return False
        elif gear == '.' and current_run > 0:
            if not allow_partial_solution and current_run < runs_to_test[0]:
                return False

            current_run = 0
            runs_to_test = runs_to_test[1:]

            if len(runs_to_test) == 0:
                return '#' not in gears[i+1:]

    return False


def fill_run(gears: list[str] | tuple[str], run: int, index: int):
    gears = list(gears.copy())

    if index > 0:
        gears[index - 1] = '.'

    for i in range(run):
        gears[index + i] = '#'

    if index + run < len(gears):
        gears[index + run] = '.'

    return gears


def get_fill_ranges(row: GearRow):
    min_gears = row.gears.copy()
    lefts_valid = [False] * len(row.runs)

    left_indices = [0] * len(row.runs)
    left_indices[-1] = 1

    while (not is_row_valid(min_gears, row.runs, False) or not all(lefts_valid)) and \
            not all([ind == 0 for ind in left_indices]):
        min_gears = row.gears.copy()
        lefts_valid = [False] * len(row.runs)

        for i in range(len(left_indices) - 1, -1, -1):
            left_indices[i] += 1
            if left_indices[i] == len(row.gears):
                left_indices[i] = 0
            else:
                break

        for i, run in enumerate(row.runs):
            run_index = left_indices[i]

            if any([left_indices[ind] == left_indices[i] for ind in range(len(row.runs)) if ind != i]):
                continue

            if can_fill(min_gears, run, run_index):
                min_gears = fill_run(min_gears, run, run_index)
                lefts_valid[i] = True
            else:
                break

    max_gears = row.gears.copy()
    rights_valid = [False] * len(row.runs)

    right_indices = [len(row.gears) - 1] * len(row.runs)
    right_indices[-1] -= 1

    reverse_runs = row.runs.copy()
    reverse_runs.reverse()

    while (not is_row_valid(max_gears, row.runs, False) or not all(rights_valid)) and \
            not all([ind == len(row.gears) - 1 for ind in right_indices]):
        max_gears = row.gears.copy()
        rights_valid = [False] * len(row.runs)

        for i in range(len(right_indices) - 1, -1, -1):
            right_indices[i] -= 1
            if right_indices[i] == -1:
                right_indices[i] = len(row.gears) - 1
            else:
                break

        for i, run in enumerate(reverse_runs):
            run_index = right_indices[i]

            if any([right_indices[ind] == right_indices[i] for ind in range(len(row.runs)) if ind != i]):
                continue

            if can_fill(max_gears, run, run_index):
                max_gears = fill_run(max_gears, run, run_index)
                rights_valid[i] = True
            else:
                break

    # for j, run in enumerate(row.runs):
    #     first = get_first_fill(min_gears, run, row.runs[j+1:], left_index, True)
    #     fill_ranges.append([first])
    #
    #     if first >= 0:
    #         min_gears = fill_run(min_gears, run, first)
    #
    #     left_index = first + run + 1

    # max_gears = row.gears.copy()
    # right_index = len(row.gears)
    #
    # reverse_runs = row.runs.copy()
    # reverse_runs.reverse()
    #
    # for j, run in enumerate(reverse_runs):
    #     last = get_first_fill(max_gears, run, reverse_runs[j+1:], right_index, False)
    #     fill_ranges[len(fill_ranges) - j - 1].append(last)
    #
    #     if last >= 0:
    #         max_gears = fill_run(max_gears, run, last)
    #
    #     right_index = last - 1

    return [[left_indices[i], right_indices[len(row.runs) - i - 1]] for i in range(len(row.runs))], min_gears, max_gears


def can_fill(gears: list[str] | tuple[str], space_to_fill: int, position: int) -> bool:
    if position + space_to_fill > len(gears) or (position > 0 and gears[position - 1] == '#') or \
            (position + space_to_fill < len(gears) and gears[position + space_to_fill] == '#'):
        return False

    return all([gear in '#?' for gear in gears[position:position + space_to_fill]])


def get_first_fill(gears: list[str], space_to_fill: int, next_runs: list[int], start_from=0, from_left=True):
    num_range = range(start_from, len(gears)) \
        if from_left else \
        range(start_from - 1, -1, -1)

    # run_starts = [i for i in num_range if gears[i] == '#' and (i == num_range.start or gears[i - num_range.step] != '#')]
    # if len(run_starts) == len(next_runs) + 1:
    #     print(run_starts)
    #     last_start = run_starts[0] - num_range.step
    #
    #     print(f'Equal number of partial runs and runs to fill, so moving from {start_from} to {last_start} for {space_to_fill}.')
    #     num_range = range(last_start, num_range.stop, num_range.step)
    # else:
    #     # checking if we need to advance forwards to account for partially completed runs in the gear list
    #     next_existing_run = 0
    #
    #     for i in num_range:
    #         if gears[i] == '#':
    #             # if i == num_range.stop - 1 and next_run is None:
    #             #     # We're at the last possible point, so all we can do is back up enough to fit the last run.
    #             #     num_range = range(num_range.stop - space_to_fill, num_range.stop, num_range.step)
    #             #     print(f'Moving to the last possible start for {space_to_fill}, {num_range.stop - space_to_fill}')
    #             #     break
    #             # else:
    #             next_existing_run += 1
    #         elif next_existing_run > 0:
    #             if len(next_runs) == 0 or (next_existing_run == space_to_fill and next_existing_run > next_runs[0] and
    #                                        next_existing_run >= max(next_runs)):
    #                 # an upcoming run is at least as big as the current run but smaller than the next
    #                 # this means we cannot place the current run anywhere before then,
    #                 #    otherwise the next run will have nowhere to go
    #                 num_range = range(i - ((next_existing_run + 1) * num_range.step), num_range.stop, num_range.step)
    #                 print(f'New start for {space_to_fill}, next runs {next_runs}: {start_from - 1} -> {num_range.start}')
    #
    #             break

    for i in num_range:
        if not can_fill(gears, space_to_fill, i):
            # can only claim this space if it's made of # and ?, and the borders are not #
            continue

        test_row = gears.copy()
        fill_run(test_row, space_to_fill, i)
        if not is_row_valid(test_row, True):
            # The run fits in this spot, but still invalidates the row
            continue

        return i

    return -1


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

        for i, row in enumerate(self.gear_rows):
            if not self.is_silent:
                print(f'Calculating row {i+1} of {len(self.gear_rows)}: {row}')

            fill_ranges, min_gears, max_gears = get_fill_ranges(row)

            if not self.is_silent:
                print(f'Leftmost fills:         {"".join(min_gears)}')
                print(f'Rightmost fills:        {"".join(max_gears)}')
                print(f'Ranges:                 {fill_ranges}')

            solutions = 1
            last_fill = 1

            for j, run in enumerate(row.runs):
                valid_fills = 0

                for pos in range(fill_ranges[j][0], fill_ranges[j][1] + 1):
                    if '.' not in row.gears[pos:pos + run]:
                        valid_fills += 1

                if j > 0 and fill_ranges[j][0] <= fill_ranges[j-1][1]:
                    # If we're overlapping the previous run, we'll need to use different logic

                    # undoing the previous step's multiplication
                    solutions /= last_fill
                    overlap_solutions = 0

                    # determining how many solutions can be made in this overlapping section
                    for k in range(fill_ranges[j-1][0], fill_ranges[j-1][1] + 1):
                        if can_fill(row.gears, row.runs[j-1], k):
                            for l in range(k + row.runs[j-1] + 1, fill_ranges[j][1] + 1):
                                if can_fill(row.gears, row.runs[j], l):
                                    overlap_solutions += 1

                    # multiplying it back in as usual
                    solutions *= overlap_solutions
                else:
                    solutions *= valid_fills

                last_fill = valid_fills

            if not self.is_silent:
                print(f'Solutions: {solutions}')
                print('\n')

            total += solutions

        return int(total)

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.calculate_solutions())

    def get_part_2_answer(self, use_sample=False) -> str:
        self.expand_rows()

        return str(self.calculate_solutions())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
