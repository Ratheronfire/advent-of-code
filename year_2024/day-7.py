from typing import List

from puzzle_base import PuzzleBase

Equation = tuple[int, list[int]]


def concatenate_numbers(left: int, right: int) -> int:
    return int(str(left) + str(right))


class Puzzle(PuzzleBase):
    year = 2024
    day = 7

    equations: list[Equation] = []

    def reset(self):
        self.equations = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            left, rights = line.split(':')

            self.equations.append((int(left), [int(n) for n in rights.strip().split(' ')]))

    def get_solutions(self, right_values: list[int], allow_concat=False) -> list[int]:
        if len(right_values) == 2:
            if allow_concat:
                return [
                    right_values[0] + right_values[1],
                    right_values[0] * right_values[1],
                    concatenate_numbers(right_values[0], right_values[1])
                ]
            else:
                return [right_values[0] + right_values[1], right_values[0] * right_values[1]]

        partial_solutions = self.get_solutions(right_values[:-1], allow_concat)

        solutions = [
            [v + right_values[-1], v * right_values[-1], concatenate_numbers(v, right_values[-1])]
            for v in partial_solutions
        ]

        flat_solutions = []
        for solution in solutions:
            flat_solutions.append(solution[0])
            flat_solutions.append(solution[1])

            if allow_concat:
                flat_solutions.append(solution[2])

        return flat_solutions

    def is_equation_solvable(self, equation: Equation, allow_concat=False) -> bool:
        solutions = self.get_solutions(equation[1], allow_concat)

        return any([s == equation[0] for s in solutions])

    def get_part_1_answer(self, use_sample=False) -> str:
        solveables = [eq for eq in self.equations if self.is_equation_solvable(eq, False)]

        return str(sum([eq[0] for eq in solveables]))

    def get_part_2_answer(self, use_sample=False) -> str:
        solveables = [eq for eq in self.equations if self.is_equation_solvable(eq, True)]

        return str(sum([eq[0] for eq in solveables]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
