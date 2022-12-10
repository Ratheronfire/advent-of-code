import functools

input_path = "inputs/day-8.txt"


def parse_input():
    _trees = []

    with open(input_path, 'r') as input_file:
        for line in input_file.readlines():
            _trees.append([int(char) for char in line.strip()])

    return _trees


def get_adjacent_tree_sets(x, y):
    left_trees = trees[y][:x]
    right_trees = trees[y][x + 1:]
    up_trees = [trees[i][x] for i in range(y)]
    down_trees = [trees[i][x] for i in range(y + 1, len(trees))]

    # So we can traverse them in the correct order.
    left_trees.reverse()
    up_trees.reverse()

    return [left_trees, right_trees, up_trees, down_trees]


def is_visible_in_direction(tree_value, neighbors):
    return len([n for n in neighbors if n >= tree_value]) == 0


def get_trees_visible(tree_value, neighbors):
    i = 0

    for n in neighbors:
        i += 1
        if n >= tree_value:
            break

    return i


def is_visible(x, y):
    if x == 0 or x == len(trees[0]) - 1 or y == 0 or y == len(trees) - 1:
        return True

    tree_value = trees[y][x]

    return any([is_visible_in_direction(tree_value, d) for d in get_adjacent_tree_sets(x, y)])


def get_scenic_score(x, y):
    neighbors = get_adjacent_tree_sets(x, y)
    tree_value = trees[y][x]

    return functools.reduce(lambda a, b: a * b, [get_trees_visible(tree_value, n) for n in neighbors])


trees = parse_input()
visible_trees = []

for i in range(len(trees)):
    for j in range(len(trees[0])):
        if is_visible(j, i):
            visible_trees.append((j, i))

print("%d trees visible." % len(visible_trees))

scenic_scores = []
for i in range(len(trees)):
    for j in range(len(trees[0])):
        scenic_scores.append(get_scenic_score(i, j))

print("Highest scenic score: %d" % max(scenic_scores))
