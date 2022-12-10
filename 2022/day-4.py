input_path = "inputs/day-4.txt"

redundant_pairs = 0
overlap_pairs = 0

with open(input_path, 'r') as input_file:
    for line in input_file.readlines():
        ranges = [[int(i) for i in r.split('-')] for r in line.strip().split(',')]

        if (ranges[0][0] >= ranges[1][0] and ranges[0][1] <= ranges[1][1]) or \
                (ranges[1][0] >= ranges[0][0] and ranges[1][1] <= ranges[0][1]):
            redundant_pairs += 1

        if ranges[1][0] <= ranges[0][0] <= ranges[1][1] or ranges[0][0] <= ranges[1][0] <= ranges[0][1]:
            overlap_pairs += 1

print(redundant_pairs)
print(overlap_pairs)
