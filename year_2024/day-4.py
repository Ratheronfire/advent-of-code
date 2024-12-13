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
        self.text_searches = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.text = [l for l in input_data if l != '']

        self.text_searches = []

        # rows
        for i in range(len(self.text)):
            self.text_searches.append((self.text[i], 'row %d' % i))

        # columns
        for x in range(len(self.text[0])):
            col = ''

            for y in range(len(self.text)):
                col += self.text[y][x]

            self.text_searches.append((col, 'column %d' % x))

        # diagonals
        for y in range(len(self.text) - 1):
            self.text_searches.append((
                self.get_diagonal(0, y, True),
                "diagonal right from (%d, %d)" % (0, y)
            ))  # rights first half
            self.text_searches.append((
                self.get_diagonal(len(self.text[0]) - 1, y, False),
                "diagonal left from (%d, %d)" % (len(self.text[0]) - 1, y)
            ))  # lefts first half

        for x in range(1, len(self.text[0]) - 1):
            self.text_searches.append((
                self.get_diagonal(x, 0, True),
                "diagonal right from (%d, %d)" % (x, 0)
            ))  # rights second half
            self.text_searches.append((
                self.get_diagonal(x, 0, False),
                "diagonal left from (%d, %d)" % (x, 0)
            ))  # lefts second half

        self.text_searches.sort(key=lambda s: s[1])

    def get_diagonal(self, x: int, y: int, is_right: bool) -> str:
        diagonal = ''

        while 0 <= x < len(self.text[0]) and 0 <= y < len(self.text):
            diagonal += self.text[y][x]
            y += 1
            x += 1 if is_right else -1

        return diagonal

    def get_word_count(self, word: str) -> int:
        count = 0

        for search in self.text_searches:
            text = search[0]
            for i in range(len(text)):
                if text[i:i+len(word)] == word:
                    count += 1

                if text[::-1][i:i+len(word)] == word:
                    count += 1

        return count

    def is_word(self, position: Point, direction: Point, word_to_match: str) -> bool:
        word = ''

        for i in range(len(word_to_match)):
            if position.x < 0 or position.x > len(self.text[0]) or position.y < 0 or position.y > len(self.text):
                break

            word += self.text[position.y][position.x]
            position += direction

        return word == word_to_match

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
                    print("Cross word at (%d, %d)." % (x, y))
                    count += 1

        return count

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.get_word_count('XMAS'))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.get_cross_word_count('MAS'))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
