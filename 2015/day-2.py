from typing import List

from puzzle_base import PuzzleBase


class Box:
    l: int
    w: int
    h: int

    def __init__(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h

    @property
    def sides(self):
        return [self.l, self.w, self.h]

    @property
    def surface_area(self):
        return 2 * self.l * self.w + \
               2 * self.w * self.h + \
               2 * self.l * self.h

    @property
    def smallest_sides(self):
        sides = self.sides

        smallest = min(sides)

        for side in sides:
            if side == smallest:
                sides.remove(side)
                break

        return smallest, min(sides)


class Puzzle(PuzzleBase):
    year = 2015
    day = 2

    boxes: List[Box]

    def reset(self):
        self.boxes = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]
            if line == '':
                continue

            dimensions = line.split('x')

            box = Box(int(dimensions[0]), int(dimensions[1]), int(dimensions[2]))
            self.boxes.append(box)

    def get_part_1_answer(self, use_sample=False) -> str:
        total_feet = 0
        for box in self.boxes:
            smallest = box.smallest_sides
            total_feet += box.surface_area + smallest[0] * smallest[1]

        return str(total_feet)

    def get_part_2_answer(self, use_sample=False) -> str:
        total_feet = 0
        for box in self.boxes:
            smallest = box.smallest_sides
            total_feet += 2 * smallest[0] + 2 * smallest[1] + box.l * box.w * box.h

        return str(total_feet)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
