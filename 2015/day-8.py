from typing import List

from puzzle_base import PuzzleBase

HEX_CHARS = '0123456789abcdefABCDEF'


class Puzzle(PuzzleBase):
    year = 2015
    day = 8

    lines: list[str]

    def reset(self):
        self.lines = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.lines = [l for l in input_data if len(l) > 0]

    def len_escaped(self, line: str) -> int:
        count = 0

        i = 1
        while i < len(line) - 1:
            char = line[i]

            if char == '\\':
                if line[i+1] in '\\"':
                    i += 1
                elif line[i+1] == 'x' and line[i+2] in HEX_CHARS and line[i+3] in HEX_CHARS:
                    i += 3

            i += 1
            count += 1

        print(f'{line} - {len(line)} characters, {count} escaped characters')
        return count

    def escape_line(self, line: str) -> str:
        out_str = '"'

        i = 0
        while i < len(line):
            char = line[i]

            if char == '"':
                out_str += '\\"'
            elif char == '\\':
                out_str += '\\\\'
            else:
                out_str += char

            i += 1

        out_str += '"'
        print(f'{line} -> {out_str} ({len(line)} -> {len(out_str)})')

        return out_str

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(sum([len(l) - self.len_escaped(l) for l in self.lines]))

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(sum([len(self.escape_line(l)) - len(l) for l in self.lines]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
