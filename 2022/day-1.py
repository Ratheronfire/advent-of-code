input_path = "inputs/day-1.txt"

elves = []
i = 0

with open(input_path, 'r') as input_file:
    for line in input_file.readlines():
        if line != '\n' and len(elves) >= i + 1:
            elves[i] += int(line)
        elif line != '\n':
            elves.append(int(line))
        else:
            i += 1

elves = sorted(elves)
print(elves[-1])

print(sum(elves[-3:]))
