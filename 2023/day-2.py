from functools import reduce
from typing import List

from puzzle_base import PuzzleBase


Cubes = dict[str, int]
Game = list[Cubes]


class Puzzle(PuzzleBase):
    year = 2023
    day = 2

    games: List[Game]

    def reset(self):
        self.games = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            line = line.split(':')

            reveal_sets = line[1].split(';')

            game: Game = []
            for reveal_set in reveal_sets:
                hints: Cubes = {}
                reveal = reveal_set.split(', ')

                for reveal in reveal:
                    hint_sections = reveal.strip().split(' ')
                    hints[hint_sections[1]] = int(hint_sections[0])

                game.append(hints)

            self.games.append(game)

    def is_game_possible(self, game: Game, max_set: Cubes):
        for cube_set in game:
            for color in cube_set.keys():
                if cube_set[color] > max_set[color]:
                    print(f'Impossible set: {str(cube_set)} ({cube_set[color]} > {max_set[color]})')
                    return False

        return True

    def get_power(self, game: Game):
        max_set: Cubes = {}

        for cube_set in game:
            for color in cube_set.keys():
                if color not in max_set or cube_set[color] > max_set[color]:
                    max_set[color] = cube_set[color]

        return reduce(lambda a, b: a * b, max_set.values())

    def get_day_1_answer(self, use_sample=False) -> str:
        count = 0
        max_set = {'red': 12, 'green': 13, 'blue': 14}

        for i in range(len(self.games)):
            if self.is_game_possible(self.games[i], max_set):
                count += i + 1

        return str(count)

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(sum([self.get_power(game) for game in self.games]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
