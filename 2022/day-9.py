input_path = "2022/inputs/day-9.txt"


tiles_visited = []

segment_count = 10
rope_segments = [[0, 0] for i in range(segment_count)]

tiles_visited.append([0, 0])

head_movements = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
    'N': (0, 0)
}


def parse_input():
    _moves = []
    with open(input_path, 'r') as input_file:
        for line in input_file.readlines():
            _move = line.strip().split(' ')
            _moves.append((_move[0], int(_move[1])))

    return _moves


def are_equal_vectors(a, b):
    return a[0] == b[0] and a[1] == b[1]


def move_vector(v, movement):
    v[0] += movement[0]
    v[1] += movement[1]

    return v


def print_grid():
    x_values = [t[0] for t in tiles_visited] + [s[0] for s in rope_segments]
    y_values = [t[1] for t in tiles_visited] + [s[1] for s in rope_segments]

    x_values.sort()
    y_values.sort()

    grid_str = ''
    for y in reversed(range(y_values[0], y_values[-1] + 1)):
        for x in range(x_values[0], x_values[-1] + 1):
            is_occupied = False

            for i in range(len(rope_segments)):
                if are_equal_vectors(rope_segments[i], [x, y]):
                    grid_str += str(i) if i > 0 else 'H'
                    is_occupied = True
                    break

            if not is_occupied:
                if are_equal_vectors([x, y], [0, 0]):
                    grid_str += 's'
                elif any([t for t in tiles_visited if are_equal_vectors(t, [x, y])]):
                    grid_str += '#'
                else:
                    grid_str += '.'

        grid_str += '\n'

    print(grid_str)


def perform_move(direction):
    head_movement = head_movements[direction]
    rope_segments[0] = move_vector(rope_segments[0], head_movement)

    for i in range(1, len(rope_segments)):
        curr_segment = rope_segments[i]
        prev_segment = rope_segments[i-1]

        segment_movement = [0, 0]

        if prev_segment[0] == curr_segment[0] and abs(prev_segment[1] - curr_segment[1]) > 1:
            # Vertical movement
            segment_movement[1] = 1 if prev_segment[1] > curr_segment[1] else -1
        elif prev_segment[1] == curr_segment[1] and abs(prev_segment[0] - curr_segment[0]) > 1:
            # Horizontal movement
            segment_movement[0] = 1 if prev_segment[0] > curr_segment[0] else -1
        else:
            # Diagonal movement, or none
            if abs(prev_segment[0] - curr_segment[0]) > 1 or abs(prev_segment[1] - curr_segment[1]) > 1:
                segment_movement[0] = 1 if prev_segment[0] > curr_segment[0] else -1
                segment_movement[1] = 1 if prev_segment[1] > curr_segment[1] else -1

        if not are_equal_vectors(segment_movement, [0, 0]):
            rope_segments[i] = move_vector(curr_segment, segment_movement)

    if rope_segments[-1] not in tiles_visited:
        tiles_visited.append([rope_segments[-1][0], rope_segments[-1][1]])


moves = parse_input()

for move in moves:
    for i in range(move[1]):
        perform_move(move[0])

print_grid()

print(len(tiles_visited))
