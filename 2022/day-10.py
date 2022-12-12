from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 10

    cycle = 0
    X = 1

    total_signal = 0

    crt = []

    def reset(self):
        self.crt = [[False for _ in range(40)] for __ in range(6)]

        self.cycle = 0
        self.X = 1
        self.total_signal = 0

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            operands = line.strip().split(' ')

            if operands[0] == 'noop':
                self.tick_cycle()
                continue
            elif operands[0] == 'addx':
                self.tick_cycle()
                self.tick_cycle()

                value = int(operands[1])
                self.X += value

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.total_signal)

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(self)

    def tick_cycle(self):
        cycle_col, cycle_row = self.cycle // 40, self.cycle % 40
        is_high_bit = abs(self.cycle % 40 - self.X) <= 1

        self.cycle += 1

        if (self.cycle + 20) % 40 == 0:
            self.total_signal += self.cycle * self.X

        if self.cycle >= 240:
            self.cycle = 0
        self.crt[cycle_col][cycle_row] = is_high_bit

    def __str__(self):
        crt_str = ''
        for y in range(0, 6):
            for x in range(0, 40):
                crt_str += '#' if self.crt[y][x] else '.'
            crt_str += '\n'

        return crt_str.strip()


puzzle = Puzzle()
print(puzzle.test_and_run())
