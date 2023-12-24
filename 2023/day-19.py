from functools import reduce
from typing import List

from puzzle_base import PuzzleBase


CATEGORIES = 'xmas'


class Part:
    def __init__(self, part_values: list[str]):
        self.parts = {}

        for part_value in part_values:
            key, value = part_value.split('=')
            self.parts[key] = int(value)

    def __getitem__(self, value: str):
        return self.parts[value]

    def __str__(self):
        return str(self.parts)


class Rule:
    def __init__(self, rule_str: str):
        if '<' not in rule_str and '>' not in rule_str:
            self.destination = rule_str
            self.is_fallback = True
            return

        self.category = rule_str[0]

        self.is_fallback = False

        self.comparison_is_greater = rule_str[1] == '>'

        self.compare_to = int(rule_str.split(':')[0][2:])
        self.destination = rule_str.split(':')[1]

    def should_accept(self, part: Part):
        if self.is_fallback:
            return True

        part_value = part[self.category]

        return part_value > self.compare_to if self.comparison_is_greater else part_value < self.compare_to

    def __str__(self):
        if self.is_fallback:
            return self.destination

        return f'{self.category}{">" if self.comparison_is_greater else "<"}{self.compare_to}:{self.destination}'


class Workflow:
    def __init__(self, workflow_str: str):
        self.workflow_id = workflow_str.split('{')[0]

        rules_strs = workflow_str.split('{')[1][:-1].split(',')
        self.rules = [Rule(rules_str) for rules_str in rules_strs]

    def __str__(self):
        return f'{self.workflow_id}{"{"}{", ".join([str(r) for r in self.rules])}{"}"}'


class Puzzle(PuzzleBase):
    year = 2023
    day = 19

    workflows: dict[str, Workflow]
    parts: list[Part]

    def reset(self):
        self.workflows = {}
        self.parts = []

    def prepare_data(self, input_data: List[str], current_part: int):
        parsing_workflows = True

        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                parsing_workflows = False
                continue

            if parsing_workflows:
                workflow = Workflow(line)
                self.workflows[workflow.workflow_id] = workflow
            else:
                self.parts.append(Part(line[1:-1].split(',')))

    def is_part_accepted(self, part: Part):
        category = 'in'

        while category not in 'AR':
            workflow = self.workflows[category]

            for rule in workflow.rules:
                if rule.should_accept(part):
                    category = rule.destination
                    break

        return category == 'A'

    def get_accepted_window(self, workflow_id: str, mins: tuple, maxes: tuple):
        accepted = 0

        mins = list(mins)
        maxes = list(maxes)

        workflow = self.workflows[workflow_id]

        for rule in workflow.rules:
            r_mins = mins.copy()
            r_maxes = maxes.copy()

            if not rule.is_fallback and rule.comparison_is_greater:
                r_mins[CATEGORIES.index(rule.category)] = rule.compare_to + 1
                maxes[CATEGORIES.index(rule.category)] = rule.compare_to
            elif not rule.is_fallback:
                r_maxes[CATEGORIES.index(rule.category)] = rule.compare_to - 1
                mins[CATEGORIES.index(rule.category)] = rule.compare_to

            if rule.destination == 'A':
                accepted_count = reduce(lambda a, b: a * b, [r_maxes[i] - r_mins[i] + 1 for i in range(len(r_mins))])
                print(f'Found {accepted_count} possible values at workflow: {workflow}; rule: {rule}.\n'
                      f'Ranges: {r_mins}, {r_maxes}\n')
                accepted += accepted_count
            elif rule.destination != 'R':
                accepted += self.get_accepted_window(rule.destination,
                                                     tuple(r_mins), tuple(r_maxes))

        return accepted

    def get_part_1_answer(self, use_sample=False) -> str:
        total = 0

        for part in self.parts:
            if self.is_part_accepted(part):
                total += part['x'] + part['m'] + part['a'] + part['s']

        return str(total)

    def get_part_2_answer(self, use_sample=False) -> str:
        return str(self.get_accepted_window('in', (1, 1, 1, 1), (4000, 4000, 4000, 4000)))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
