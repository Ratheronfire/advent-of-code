import re
from typing import List, Union

input_path = "inputs/day-11.txt"

monkeys = []
least_common_multiple = -1


class Monkey:
    id: int

    items: List[int]

    operator: str
    operand: Union[int, str]

    divide_test_num: int

    true_monkey: int
    false_monkey: int

    inspect_count = 0

    def __init__(self, id, items, operator, operand, divide_test_num, true_monkey, false_monkey):
        self.id = id

        self.items = items
        self.operator = operator

        self.operand = operand
        self.divide_test_num = divide_test_num

        self.true_monkey = true_monkey
        self.false_monkey = false_monkey


def parse_monkey_data(monkey_data):
    match = re.match(r'Monkey (\d+):\n'
                     r'Starting items: ([\d, ]+)\n'
                     r'Operation: new = old (.) (\d+|old)\n'
                     r'Test: divisible by (\d+)\n'
                     r'If true: throw to monkey (\d+)\n'
                     r'If false: throw to monkey (\d+)', monkey_data)

    monkey = Monkey(int(match[1]),
                    [int(item) for item in match[2].split(', ')],
                    match[3],
                    match[4] if match[4] == 'old' else int(match[4]),
                    int(match[5]),
                    int(match[6]),
                    int(match[7]))

    return monkey


def read_data():
    global monkeys
    global least_common_multiple

    monkeys = []

    with open(input_path, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    monkey_lines = ''
    for line in lines:
        if line != '':
            monkey_lines += line + '\n'
        else:
            monkeys.append(parse_monkey_data(monkey_lines))
            monkey_lines = ''

    # need the last one, too
    monkeys.append(parse_monkey_data(monkey_lines))

    base_divisors = [m.divide_test_num for m in monkeys]
    divisors = [m.divide_test_num for m in monkeys]
    while not all([d == divisors[0] for d in divisors]):
        min_divisor = min(divisors)
        min_index = divisors.index(min_divisor)

        divisors[min_index] += base_divisors[min_index]

    least_common_multiple = divisors[0]


def process_turn(is_part_2=False):
    for monkey in monkeys:
        for item in monkey.items:
            operand = item if monkey.operand == 'old' else monkey.operand
            if monkey.operator == '*':
                item *= operand

                if is_part_2:
                    item %= least_common_multiple
            elif monkey.operator == '+':
                item += operand

            if not is_part_2:
                item //= 3

            next_monkey_id = monkey.true_monkey if item % monkey.divide_test_num == 0 else monkey.false_monkey
            monkeys[next_monkey_id].items.append(item)

            monkey.inspect_count += 1

        monkey.items.clear()


def get_score():
    sorted_monkeys = sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)
    return sorted_monkeys[0].inspect_count * sorted_monkeys[1].inspect_count


print("====== PART 1 ======")
read_data()

for i in range(20):
    process_turn(False)

monkeys = sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)

print('Part 1 - Monkey business score: %d.' % get_score())

print("====== PART 2 ======")
read_data()

for i in range(10000):
    process_turn(True)

    if i in [0, 19] or i % 1000 == 999:
        print('== After Round %d ==:' % (i + 1))

        for monkey in monkeys:
            print('Monkey %d inspected items %d times.' % (monkey.id, monkey.inspect_count))

print('Part 2 - Monkey business score: %d.' % get_score())
