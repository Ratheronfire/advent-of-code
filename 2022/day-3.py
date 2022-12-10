def get_matching_item_priority(sacks):
    repeat = None

    for item in sacks[0]:
        if all([item in s for s in sacks[1:]]):
            repeat = item
            break

    return ord(repeat) - (96 if repeat.islower() else 38)


input_path = "inputs/day-3.txt"

total = 0
group_total = 0

group = []

with open(input_path, 'r') as input_file:
    for line in input_file.readlines():
        line = line.strip()

        midpoint = len(line) // 2
        sacks = line[:midpoint], line[midpoint:]

        total += get_matching_item_priority(sacks)

        group.append(line)
        if len(group) == 3:
            group_total += get_matching_item_priority(group)
            group = []

print(total)
print(group_total)
