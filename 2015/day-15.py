import re
from typing import List

from puzzle_base import PuzzleBase


class Ingredient:
    name: str

    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name

        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def __mul__(self, other) -> tuple[int, int, int, int]:
        assert isinstance(other, int)

        return self.capacity * other, self.durability * other, self.flavor * other, self.texture * other


class Puzzle(PuzzleBase):
    year = 2015
    day = 15

    ingredients: list[Ingredient]

    _cached_ingredient_scores: dict[tuple[int], int]

    def reset(self):
        self.ingredients = []
        self._cached_ingredient_scores = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            sections = re.search(r'(.+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line)
            ingredient = Ingredient(sections[1], int(sections[2]), int(sections[3]), int(sections[4]), int(sections[5]), int(sections[6]))
            self.ingredients.append(ingredient)

    def get_ingredient_score(self, ingredient_amounts: tuple):
        if ingredient_amounts in self._cached_ingredient_scores:
            return self._cached_ingredient_scores[ingredient_amounts]

        ingredient_totals = [self.ingredients[i] * ingredient_amounts[i] for i in range(len(ingredient_amounts))]

        total_capacity = sum([total[0] for total in ingredient_totals])
        total_durability = sum([total[1] for total in ingredient_totals])
        total_flavor = sum([total[2] for total in ingredient_totals])
        total_texture = sum([total[3] for total in ingredient_totals])

        if total_capacity <= 0 or total_durability <= 0 or total_flavor <= 0 or total_texture <= 0:
            total = 0
        else:
            total = total_capacity * total_durability * total_flavor * total_texture

        self._cached_ingredient_scores[ingredient_amounts] = total

        return total

    def get_highest_score(self, ingredient_selections, teaspoons_left, target_calories=False):
        first_unclaimed = -1
        for selection in ingredient_selections:
            if selection[1] is None:
                first_unclaimed = ingredient_selections.index(selection)
                break

        score_results = []

        min_value = 1 if first_unclaimed < len(ingredient_selections) - 1 else teaspoons_left
        for i in range(min_value, teaspoons_left + 1):
            ingredient_selections[first_unclaimed] = (ingredient_selections[first_unclaimed][0], i)

            unclaimed_count = len([s for s in ingredient_selections if s[1] is None])

            if teaspoons_left - i < unclaimed_count:
                # not enough teaspoons left for the unclaimed ingredients, so we can't calculate this selection
                continue

            if target_calories and unclaimed_count == 0:
                calories = sum([s[0].calories * s[1] for s in ingredient_selections])
                if calories != 500:
                    continue

            if first_unclaimed == len(ingredient_selections) - 1:
                score_results.append(self.get_ingredient_score(tuple([s[1] for s in ingredient_selections])))
            else:
                score_results.append(self.get_highest_score(ingredient_selections.copy(), teaspoons_left - i, target_calories))

        return max(score_results) if len(score_results) else 0

    def calculate_score(self, target_calories=False):
        return self.get_highest_score([(i, None) for i in self.ingredients], 100, target_calories)

    def get_part_1_answer(self, use_sample=False) -> str:
        return str(self.calculate_score(False))

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.calculate_score(True))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
