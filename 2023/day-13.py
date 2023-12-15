import math
from typing import List

from helpers.grid import Grid
from puzzle_base import PuzzleBase


def split_grid_to_str(grid: Grid, split_vertically: bool, split_index: int) -> str:
    grid_str = '   ' + ''.join([str((i+1) // 10) for i in range(grid.width)]) + '\n'
    grid_str += '   ' + ''.join([str((i+1) % 10) for i in range(grid.width)]) + '\n'

    if split_vertically:
        grid_str += '   ' + ' ' * (split_index - 1) + '><' + '\n'
    else:
        grid_str += '\n'

    for i, row in enumerate(str(grid).split('\n')):
        split_char = ' '
        if not split_vertically and i == split_index - 1:
            split_char = 'V'
        elif not split_vertically and i == split_index:
            split_char = '^'

        grid_str += f'{i+1:>2}{split_char}{"".join(row)}\n'

    return grid_str


class Puzzle(PuzzleBase):
    year = 2023
    day = 13

    grids: list[Grid]

    def reset(self):
        self.grids = []

    def prepare_data(self, input_data: List[str], current_part: int):
        grid_strs = []

        for line in input_data:
            if line == '':
                self.grids.append(Grid.from_strings(grid_strs))
                grid_strs = []
            else:
                grid_strs.append(line)

    def find_repeat_point(self, slices, is_part_2: bool):
        mirror_points = []

        for i in range(len(slices) - 1):
            left = slices[i]
            right = slices[i+1]
            imperfections = [j for j in range(len(left)) if left[j] != right[j]]

            if left == right or (is_part_2 and len(imperfections) == 1):
                mirror_points.append((i, len(imperfections)))

        if not len(mirror_points):
            return -1

        for mirror_point, base_imperfections in mirror_points:
            mirror_offset = 1
            is_true_mirror = True
            mirror_imperfections = 0

            while mirror_point - mirror_offset >= 0 and mirror_point + 1 + mirror_offset < len(slices):
                left = slices[mirror_point - mirror_offset]
                right = slices[mirror_point + 1 + mirror_offset]

                imperfections = [i for i in range(len(left)) if left[i] != right[i]]

                if left != right and (not is_part_2 or len(imperfections) != 1):
                    is_true_mirror = False
                mirror_imperfections += len(imperfections)
                mirror_offset += 1

            if is_true_mirror and (not is_part_2 or (base_imperfections + mirror_imperfections) == 1):
                return mirror_point + 1

        return -1

    def find_reflection_value(self, grid: Grid, is_part_2: bool):
        rows = [str(grid[(0, i):(grid.width, i):(1, 1)]) for i in range(grid.height)]
        cols = [str(grid[(i, 0):(i, grid.height):(1, 1)]) for i in range(grid.width)]

        row_repeat_point = self.find_repeat_point(rows, is_part_2)
        col_repeat_point = self.find_repeat_point(cols, is_part_2)

        if is_part_2:
            part1_row_point = self.find_repeat_point(rows, False)
            part1_col_point = self.find_repeat_point(cols, False)

            if part1_row_point == -1 and row_repeat_point != -1:
                col_repeat_point = -1
            if part1_col_point == -1 and col_repeat_point != -1:
                row_repeat_point = -1

        if col_repeat_point > -1:
            # print(f'{col_repeat_point} columns to left.')
            # print(split_grid_to_str(grid, True, col_repeat_point))
            return col_repeat_point
        elif row_repeat_point > -1:
            # print(f'{row_repeat_point} rows above.')
            # print(split_grid_to_str(grid, False, row_repeat_point))
            return row_repeat_point * 100
        else:
            print('Something went wrong with this grid:')
            print(grid)

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(sum([self.find_reflection_value(g, False) for g in self.grids]))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(sum([self.find_reflection_value(g, True) for g in self.grids]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
