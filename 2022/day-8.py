import functools
from typing import List
from puzzle_base import PuzzleBase


def is_visible_in_direction(tree_value, neighbors):
    return len([n for n in neighbors if n >= tree_value]) == 0


def get_trees_visible(tree_value, neighbors):
    i = 0

    for n in neighbors:
        i += 1
        if n >= tree_value:
            break

    return i


class Puzzle(PuzzleBase):
    year = 2022
    day = 8

    trees = []

    def reset(self):
        self.trees = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            if input_data[i].strip() != '':
                self.trees.append([int(char) for char in input_data[i].strip()])

    def get_day_1_answer(self, use_sample=False) -> str:
        visible_trees = []

        for i in range(len(self.trees)):
            for j in range(len(self.trees[0])):
                if self.is_visible(j, i):
                    visible_trees.append((j, i))

        return str(len(visible_trees))

    def get_day_2_answer(self, use_sample=False) -> str:
        scenic_scores = []

        for i in range(len(self.trees)):
            for j in range(len(self.trees[0])):
                scenic_scores.append(self.get_scenic_score(i, j))

        return str(max(scenic_scores))

    def get_adjacent_tree_sets(self, x, y):
        left_trees = self.trees[y][:x]
        right_trees = self.trees[y][x + 1:]
        up_trees = [self.trees[i][x] for i in range(y)]
        down_trees = [self.trees[i][x] for i in range(y + 1, len(self.trees))]

        # So we can traverse them in the correct order.
        left_trees.reverse()
        up_trees.reverse()

        return [left_trees, right_trees, up_trees, down_trees]

    def is_visible(self, x, y):
        if x == 0 or x == len(self.trees[0]) - 1 or y == 0 or y == len(self.trees) - 1:
            return True

        tree_value = self.trees[y][x]

        return any([is_visible_in_direction(tree_value, d) for d in self.get_adjacent_tree_sets(x, y)])

    def get_scenic_score(self, x, y):
        neighbors = self.get_adjacent_tree_sets(x, y)
        tree_value = self.trees[y][x]

        return functools.reduce(lambda a, b: a * b, [get_trees_visible(tree_value, n) for n in neighbors])


puzzle = Puzzle()
print(puzzle.test_and_run())

