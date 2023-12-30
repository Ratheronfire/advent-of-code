from typing import List

from puzzle_base import PuzzleBase

Lens = tuple[str, int]
Box = list[Lens]


class Puzzle(PuzzleBase):
    year = 2023
    day = 15

    strings: list[str]
    boxes: dict[int, Box]

    def reset(self):
        self.strings = []
        self.boxes = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        self.strings = input_data[0].split(',')

        for i in range(256):
            self.boxes[i] = []

    def hash_string(self, string: str) -> int:
        hash_value = 0

        for char in string:
            hash_value += ord(char)
            hash_value = hash_value * 17
            hash_value = hash_value % 256

        return hash_value

    def run_command(self, command: str):
        if '=' in command:
            label, lens = command.split('=')
            lens = int(lens)
        else:
            label = command.split('-')[0]
            lens = -1

        label_hash = self.hash_string(label)
        box = self.boxes[label_hash]

        existing_lens = [(i, l) for i, l in enumerate(box) if l[0] == label]
        if existing_lens:
            lens_id, lens_value = existing_lens[0]

            if lens != -1:
                box[lens_id] = (label, lens)
            else:
                self.boxes[label_hash] = box[:lens_id] + box[lens_id + 1:]
        elif lens != -1:
            box.append((label, lens))

    def get_box_values(self):
        total_value = 0

        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                total_value = total_value + (i + 1) * (j + 1) * (self.boxes[i][j][1])

        return total_value

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(sum([self.hash_string(s) for s in self.strings]))

    def get_part_2_answer(self, use_sample=False) -> str:
        for command in self.strings:
            self.run_command(command)

        return str(self.get_box_values())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
