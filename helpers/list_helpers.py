from typing import List


def _does_circular_permutation_exist(list: list, permutations: List):
    circular_list = list

    for i in range(len(list)):
        if circular_list in permutations:
            return True

        circular_list = circular_list[1:] + [circular_list[0]]

    return False


class ListHelper:
    cached_permutations = {}

    def get_permutations(self, list: List, is_circular=False) -> List:
        if len(list) < 2:
            return list
        elif len(list) == 2:
            return [[list[0], list[1]], [list[1], list[0]]]
        elif tuple(list) in self.cached_permutations:
            return self.cached_permutations[tuple(list)]

        permutations = []
        for elem in list:
            sublist = [e for e in list if e != elem]
            sub_permutations = self.get_permutations(sublist, is_circular)

            for sub_permutation in sub_permutations:
                if is_circular and _does_circular_permutation_exist([elem] + sub_permutation, permutations):
                    continue

                if [elem] + sub_permutation not in permutations:
                    permutations.append([elem] + sub_permutation)
                if sub_permutation + [elem] not in permutations:
                    permutations.append(sub_permutation + [elem])

        self.cached_permutations[tuple(list)] = permutations
        return permutations

    def clear_permutation_cache(self):
        self.cached_permutations = {}
