import math
import os
from copy import deepcopy
from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


EMPTY_TILE = '.'  # '░░'
FALLING_TILE = '@'  # '@@'
SOLID_TILE = '#'  # '██'


BLOCKS = [
    Grid.from_array([[FALLING_TILE, FALLING_TILE, FALLING_TILE, FALLING_TILE]]),
    Grid.from_array([[EMPTY_TILE,   FALLING_TILE, EMPTY_TILE],
                     [FALLING_TILE, FALLING_TILE, FALLING_TILE],
                     [EMPTY_TILE,   FALLING_TILE, EMPTY_TILE]]),
    Grid.from_array([[FALLING_TILE, FALLING_TILE, FALLING_TILE],
                     [EMPTY_TILE,     EMPTY_TILE, FALLING_TILE],
                     [EMPTY_TILE,     EMPTY_TILE, FALLING_TILE]]),
    Grid.from_array([[FALLING_TILE],
                     [FALLING_TILE],
                     [FALLING_TILE],
                     [FALLING_TILE]]),
    Grid.from_array([[FALLING_TILE, FALLING_TILE],
                     [FALLING_TILE, FALLING_TILE]])
]


class Puzzle(PuzzleBase):
    year = 2022
    day = 17

    cave_field: Grid
    jet_streams: list[bool] = []  # True = right, False = left

    block_pos: Point

    current_block = 0
    current_stream = 0

    top_line = 0

    def reset(self):
        self.cave_field = Grid.create_empty(7, 4, EMPTY_TILE)
        self.cave_field.invert_y_display = True

        self.jet_streams = []

        self.block_pos: Point = (2, -1)

        self.current_block = 0
        self.current_stream = 0

        self.top_line = 0

    def prepare_data(self, input_data: List[str], current_part: int):
        for char in input_data[0]:
            self.jet_streams.append(char == '>')

    def can_push(self, direction):
        block_x, block_y = self.block_pos
        block_grid = BLOCKS[self.current_block]

        dir_x, dir_y = direction

        if direction == (-1, 0) and block_x == 0:
            return False
        elif direction == (1, 0) and block_x + block_grid.width == 7:
            return False
        elif direction == (0, -1):
            if block_y == 0:
                return False

        for x in range(block_x, block_grid.width + block_x):
            for y in range(block_y, block_grid.height + block_y):
                if self.cave_field[(x, y)] == FALLING_TILE and self.cave_field[(x + dir_x, y + dir_y)] == SOLID_TILE:
                    return False

        return True

    def move_block(self, new_pos):
        old_x, old_y = self.block_pos
        new_x, new_y = new_pos

        block_grid = BLOCKS[self.current_block]

        for x in range(old_x, old_x + block_grid.width):
            for y in range(old_y, old_y + block_grid.height):
                if self.cave_field[(x, y)] == FALLING_TILE:
                    self.cave_field[(x, y)] = EMPTY_TILE

        for x in range(block_grid.width):
            for y in range(block_grid.height):
                if block_grid[(x, y)] == FALLING_TILE:
                    self.cave_field[(new_x + x, new_y + y)] = block_grid[(x, y)]

        self.block_pos = new_pos

    def drop_block(self):
        block_grid = BLOCKS[self.current_block]

        self.move_block((2, self.top_line + 3))

        # print(self)

        is_stopped = False
        while not is_stopped:
            jet_offset = (1 if self.jet_streams[self.current_stream] else -1)

            if self.can_push((jet_offset, 0)):
                self.move_block((self.block_pos[0] + jet_offset, self.block_pos[1]))

            self.current_stream = (self.current_stream + 1) % len(self.jet_streams)

            if self.can_push((0, -1)):
                self.move_block((self.block_pos[0], self.block_pos[1] - 1))
            else:
                block_x, block_y = self.block_pos

                for x in range(block_x, block_grid.width + block_x):
                    for y in range(block_y, block_grid.height + block_y):
                        if self.cave_field[(x, y)] == FALLING_TILE:
                            self.cave_field[(x, y)] = SOLID_TILE
                is_stopped = True
                if block_y + block_grid.height > self.top_line:
                    self.top_line = block_y + block_grid.height

    def __str__(self):
        depth_limit = max(self.cave_field.height - 20, 0)
        cave_snapshot = self.cave_field[(0, self.cave_field.height):(7, depth_limit)]

        graph_lines = str(cave_snapshot).split('\n')
        jet_char = '>' if self.jet_streams[self.current_stream] else '<'

        out_str = '    %s  \n' % jet_char

        for i in range(len(graph_lines)):
            out_str += f'\n{self.cave_field.height - i: >4} |{graph_lines[i]}|'

        if depth_limit == 0:
            out_str += '\n     +--------+'

        return out_str

    def drop_blocks(self, count):
        lines_before = self.top_line

        for i in range(count):
            self.drop_block()
            self.current_block = (self.current_block + 1) % len(BLOCKS)

        return self.top_line - lines_before

    def get_day_1_answer(self, use_sample=False) -> str:
        self.drop_blocks(2022)

        return str(self.top_line)

    def get_day_2_answer(self, use_sample=False) -> str:
        total_blocks = 1000000000000

        interval = -1
        lines_before = -1
        lines_per_interval = -1

        total_patterns = 0

        last_patterns = []
        interval_found = False
        while not interval_found:
            cave_snapshot_before = self.cave_field[(0, self.cave_field.height): (7, self.cave_field.height - 30)]
            last_patterns.append((str(cave_snapshot_before), self.top_line))

            self.drop_blocks(1)
            total_patterns += 1

            cave_snapshot_after = self.cave_field[(0, self.cave_field.height): (7, self.cave_field.height - 30)]
            repeats = [p for p in last_patterns if p[0] == str(cave_snapshot_after)]
            if repeats:
                interval_found = True

                repeat_index = last_patterns.index(repeats[0])
                interval = total_patterns - repeat_index
                lines_before = last_patterns[repeat_index][1]
                lines_per_interval = self.top_line - lines_before

                total_blocks -= repeat_index

            last_patterns = last_patterns[:len(self.jet_streams)]

        lines_after = self.drop_blocks(total_blocks % interval)

        return str(lines_before + (total_blocks // interval) * lines_per_interval + lines_after)


puzzle = Puzzle()
print(puzzle.test_and_run())
