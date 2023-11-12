import re
from typing import List, Union

from puzzle_base import PuzzleBase

Molecule = tuple[str]


class Puzzle(PuzzleBase):
    year = 2015
    day = 19

    replacements: dict[Molecule, list[Molecule]]
    reverse_replacements: dict[Molecule, list[Molecule]]
    base_str: str

    _cached_replacements: dict[Molecule, set[Molecule]]

    def reset(self):
        self.replacements = {}
        self.reverse_replacements = {}
        self.base_str = ''

        self._cached_replacements = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                break

            parts = line.split(' => ')

            left_molecule: Molecule = tuple([parts[0]])
            right_molecule = self.get_molecule_atoms(parts[1])

            if left_molecule in self.replacements:
                self.replacements[left_molecule].append(right_molecule)
            else:
                self.replacements[left_molecule] = [right_molecule]

            if right_molecule in self.reverse_replacements:
                self.reverse_replacements[right_molecule].append(left_molecule)
            else:
                self.reverse_replacements[right_molecule] = [left_molecule]

        self.base_str = input_data[-2]

    def get_replacements(self, molecule: Union[str, Molecule] = None, reverse_replace=False) -> set[Molecule]:
        if molecule is None:
            molecule = self.base_str
        if isinstance(molecule, str):
            molecule = self.get_molecule_atoms(molecule)

        if molecule in self._cached_replacements:
            return self._cached_replacements[molecule]

        replacements = self.reverse_replacements if reverse_replace else self.replacements
        longest_replacement = max([len(r) for r in replacements])

        transformed_molecules = set()

        for i in range(len(molecule)):
            maybe_replacements = []
            for j in range(i+1, i + longest_replacement + 1):
                if j > len(molecule):
                    break
                maybe_replacements.append(molecule[i:j])

            for replacement in maybe_replacements:
                if replacement in replacements:
                    for replacement_after in replacements[replacement]:
                        new_molecule = molecule[:i] + \
                                     tuple(replacement_after) + \
                                     molecule[i + len(replacement):len(molecule)]

                        transformed_molecules.add(new_molecule)

        self._cached_replacements[molecule] = transformed_molecules
        return transformed_molecules

    def find_shortest_reduction(self, base_molecule: Molecule, final_molecule: Molecule, replacement_history=(), current_min=-1) -> tuple:
        if current_min != -1 and len(replacement_history) > current_min:
            return ()

        if len(set(replacement_history)) < len(replacement_history):
            return ()

        # if base_str in self._cached_reductions:
        #     return self._cached_reductions[base_str]

        replacements = list(self.get_replacements(base_molecule, True))

        sub_paths = []

        if len(replacements) == 0:
            # if base_str == final_str:
            #     self._cached_reductions[base_str] = replacement_history
            return replacement_history if base_molecule == final_molecule else ()

        for replacement in replacements:
            # print(f'Depth {len(replacement_history)}, {replacements.index(replacement)}/{len(replacements)}; {base_str} -> {replacements}')
            new_history: list[Molecule] = list(replacement_history)
            new_history.append(replacement)

            inner_history = self.find_shortest_reduction(replacement, final_molecule, tuple(new_history), current_min)

            if len(inner_history) > 0:
                sub_paths.append(inner_history)
                if len(inner_history) < current_min:
                    current_min = len(inner_history)

                # There's a better way to do this I'm sure, but this works for now
                return inner_history

        sub_paths = sorted(sub_paths, key=lambda p: len(p))
        ideal_path = sub_paths[0] if len(sub_paths) else ()

        return ideal_path

    def get_dead_ends(self) -> set[str]:
        dead_ends = []
        for molecule in self.reverse_replacements:
            for atom in molecule:
                if not tuple([atom]) in self.replacements:
                    dead_ends.append(atom)

        return set(dead_ends)

    def get_molecule_atoms(self, molecule_str: str) -> Molecule:
        return tuple([str(m) for m in re.split(r'(e|[A-Z][a-z]*)', molecule_str) if m != ''])

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(len(self.get_replacements()))

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(len(self.find_shortest_reduction(
            self.get_molecule_atoms(self.base_str),
            self.get_molecule_atoms('e'))))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
