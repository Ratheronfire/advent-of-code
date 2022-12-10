import copy
import re


def build_stack(lines):
    stacks = [[] for i in range(len(lines[0]) // 4)]

    for line in lines:
        stack_index = 0
        for i in range(0, len(line), 4):
            if line[i] == '[':
                stacks[stack_index].append(line[i+1])

            stack_index += 1

    return [s[::-1] for s in stacks]


input_path = "inputs/day-5.txt"


stacks_built = False
stack_lines = []
moves = []

with open(input_path, 'r') as input_file:
    for line in input_file.readlines():
        if line == '\n':
            continue

        if not stacks_built and line[1] == '1':
            stacks = build_stack(stack_lines)
            part2_stacks = copy.deepcopy(stacks)
            stacks_built = True
            continue
        elif not stacks_built:
            stack_lines.append(line)
            continue

        moves.append([int(match) for match in re.findall('\\d+', line)])


for move in moves:
    count = move[0]
    first = move[1] - 1
    second = move[2] - 1

    # part 1
    for i in range(count):
        char = stacks[first].pop()
        stacks[second].append(char)

    # part 2
    chars = part2_stacks[first][-count:]

    part2_stacks[first] = part2_stacks[first][:-count]
    part2_stacks[second] += chars


print(''.join([s[-1] for s in stacks]))
print(''.join([s[-1] for s in part2_stacks]))
