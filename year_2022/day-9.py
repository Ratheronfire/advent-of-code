from typing import List

from puzzle_base import PuzzleBase

HEAD_MOVEMENTS = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
    'N': (0, 0)
}


def are_equal_vectors(a, b):
    return a[0] == b[0] and a[1] == b[1]


def move_vector(v, movement):
    v[0] += movement[0]
    v[1] += movement[1]

    return v


class Puzzle(PuzzleBase):
    year = 2022
    day = 9

    moves = []
    tiles_visited = []
    rope_segments = []

    def reset(self):
        self.rope_segments = []
        self.tiles_visited = [[0, 0]]
        self.moves = []

    def prepare_data(self, input_data: List[str], current_part: int):
        self.rope_segments = [[0, 0] for _ in range(2 if current_part == 1 else 10)]

        for i in range(len(input_data)):
            line = input_data[i].strip()

            if line == '':
                continue

            move = line.split(' ')
            self.moves.append((move[0], int(move[1])))

    def get_part_1_answer(self, use_sample=False) -> str:
        self.perform_moves()
        return str(len(self.tiles_visited))

    def get_part_2_answer(self, use_sample=False) -> str:
        self.perform_moves()
        return str(len(self.tiles_visited))

    def perform_moves(self):
        for move in self.moves:
            for i in range(move[1]):
                self.perform_move(move[0])

    def perform_move(self, direction):
        head_movement = HEAD_MOVEMENTS[direction]
        self.rope_segments[0] = move_vector(self.rope_segments[0], head_movement)

        for i in range(1, len(self.rope_segments)):
            curr_segment = self.rope_segments[i]
            prev_segment = self.rope_segments[i-1]

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
                self.rope_segments[i] = move_vector(curr_segment, segment_movement)

        if self.rope_segments[-1] not in self.tiles_visited:
            self.tiles_visited.append([self.rope_segments[-1][0], self.rope_segments[-1][1]])

    def __str__(self):
        x_values = [t[0] for t in self.tiles_visited] + [s[0] for s in self.rope_segments]
        y_values = [t[1] for t in self.tiles_visited] + [s[1] for s in self.rope_segments]

        x_values.sort()
        y_values.sort()

        grid_str = ''
        for y in reversed(range(y_values[0], y_values[-1] + 1)):
            for x in range(x_values[0], x_values[-1] + 1):
                is_occupied = False

                for i in range(len(self.rope_segments)):
                    if are_equal_vectors(self.rope_segments[i], [x, y]):
                        grid_str += str(i) if i > 0 else 'H'
                        is_occupied = True
                        break

                if not is_occupied:
                    if are_equal_vectors([x, y], [0, 0]):
                        grid_str += 's'
                    elif any([t for t in self.tiles_visited if are_equal_vectors(t, [x, y])]):
                        grid_str += '#'
                    else:
                        grid_str += '.'

            grid_str += '\n'

        return grid_str


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
