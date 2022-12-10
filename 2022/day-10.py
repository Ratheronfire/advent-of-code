input_path = "inputs/day-10.txt"

cycle = 0
X = 1

total_signal = 0
important_cycles = [20, 60, 100, 140, 180, 220]

crt = []
for i in range(6):
    row = []
    for j in range(40):
        row.append(False)
    crt.append(row)


def print_crt():
    crt_str = ''
    for y in range(0, 6):
        for x in range(0, 40):
            crt_str += '#' if crt[y][x] else '.'
        crt_str += '\n'

    print(crt_str)


def tick_cycle():
    global cycle
    global total_signal
    global X

    cycle_col, cycle_row = cycle // 40, cycle % 40
    is_high_bit = abs(cycle % 40 - X) <= 1

    cycle += 1

    if (cycle + 20) % 40 == 0:
        total_signal += cycle * X

    if cycle >= 240:
        cycle = 0
    crt[cycle_col][cycle_row] = is_high_bit


with open(input_path, 'r') as input_file:
    for line in input_file.readlines():
        operands = line.strip().split(' ')

        if operands[0] == 'noop':
            tick_cycle()
            continue
        elif operands[0] == 'addx':
            tick_cycle()
            tick_cycle()

            value = int(operands[1])
            X += value

print(total_signal)
print_crt()
