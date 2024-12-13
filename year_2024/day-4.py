from typing import List

from helpers.grid import Point
from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2024
    day = 4

    text = []
    text_searches = []

    def reset(self):
        self.text = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.text = [l for l in input_data if l != '']

    def get_diagonal(self, x: int, y: int, is_right: bool) -> str:
        diagonal = ''

        while 0 <= x < len(self.text[0]) and 0 <= y < len(self.text):
            diagonal += self.text[y][x]
            y += 1
            x += 1 if is_right else -1

        return diagonal

    def is_word(self, position: Point, direction: Point, word_to_match: str) -> bool:
        word = ''

        for i in range(len(word_to_match)):
            if position.x < 0 or position.x > len(self.text[0]) - 1 or position.y < 0 or position.y > len(self.text) - 1:
                break

            word += self.text[position.y][position.x]
            position += direction

        return word == word_to_match

    def get_word_count(self, word: str) -> int:
        count = 0

        for y in range(len(self.text)):
            for x in range(len(self.text[0])):
                dirs = [
                    Point(0, 1),  Point(0, -1),
                    Point(1, 0),  Point(-1, 0),
                    Point(1, 1),  Point(1, -1),
                    Point(-1, 1), Point(-1, -1)
                ]

                for direction in dirs:
                    if self.is_word(Point(x, y), direction, word):
                        count += 1

        return count

    def get_cross_word_count(self, word: str):
        count = 0

        for y in range(1, len(self.text) - 1):
            for x in range(1, len(self.text[0]) - 1):
                dirs = [
                    Point(1, 1), Point(1, -1),
                    Point(-1, 1), Point(-1, -1)
                ]

                crossed_words = 0

                for direction in dirs:
                    if self.is_word(Point(x, y) - direction, direction, word):
                        crossed_words += 1

                if crossed_words >= 2:
                    count += 1

        return count

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.get_word_count('XMAS'))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.get_cross_word_count('MAS'))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
