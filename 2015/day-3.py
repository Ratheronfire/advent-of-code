from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 3

    grid: Grid
    pos: Point
    robot_pos: Point

    movements: str
    houses_visited = 0

    def reset(self):
        self.pos = Point(0, 0)
        self.robot_pos = Point(0, 0)

        self.movements = ''
        self.houses_visited = 1

    def prepare_data(self, input_data: List[str], current_part: int):
        self.movements = input_data[0]
        self.grid = Grid.create_empty(0, 0, '.')
        self.grid[(0, 0)] = 'S'

    def move(self, index, robot_moving=False):
        x, y = (self.robot_pos.x, self.robot_pos.y) if robot_moving else (self.pos.x, self.pos.y)
        movement = self.movements[index]

        # print(f"\nMove {index} ({self.pos})\n====\n")
        # print(self.grid)

        if movement == '>':
            x += 1
        elif movement == '<':
            x -= 1
        elif movement == '^':
            y += 1
        elif movement == 'v':
            y -= 1

        if robot_moving:
            self.robot_pos = Point(x, y)
        else:
            self.pos = Point(x, y)

        if self.grid[(x, y)] in ['.', '', None]:
            self.houses_visited += 1

        self.grid[(x, y)] = movement

    def get_day_1_answer(self, use_sample=False) -> str:
        for i in range(len(self.movements)):
            self.move(i, False)

        return str(self.houses_visited)

    def get_day_2_answer(self, use_sample=False) -> str:
        for i in range(len(self.movements)):
            self.move(i, i % 2 == 1)

        return str(self.houses_visited)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
