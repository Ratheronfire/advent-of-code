import math
from typing import List

from helpers.grid import Grid, Point
from puzzle_base import PuzzleBase


WRAP_TILE = ' '
EMPTY_TILE = '.'
WALL_TILE = '#'


FACING_TILES = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'V',
    (0, -1): '^'
}

FACING_MULTIPLIER = {
    (1, 0): 0,
    (-1, 0): 2,
    (0, 1): 1,
    (0, -1): 3
}

FACE_LINKING_DIRS = [
    (0, 1), (0, -1), (1, 0), (-1, 0)
]

SAMPLE_HARDCODED_LINKS = {
    # In order: top, bottom, left, right
    1: {
        (0, 1): None,
        (0, -1): 2,
        (-1, 0): 3,
        (1, 0): 6
    },
    2: {
        (0, 1): 5,
        (0, -1): 1,
        (-1, 0): 6,
        (1, 0): None
    },
    3: {
        (0, 1): 5,
        (0, -1): 1,
        (-1, 0): None,
        (1, 0): None
    },
    4: {
        (0, 1): None,
        (0, -1): None,
        (-1, 0): None,
        (1, 0): 6
    },
    5: {
        (0, 1): 2,
        (0, -1): None,
        (-1, 0): 3,
        (1, 0): None
    },
    6: {
        (0, 1): 2,
        (0, -1): 4,
        (-1, 0): None,
        (1, 0): 1
    }
}

HARDCODED_LINKS = {
    1: {
        (0, 1): None,
        (0, -1): 6,
        (-1, 0): 4,
        (1, 0): None
    },
    2: {
        (0, 1): 3,
        (0, -1): 6,
        (-1, 0): None,
        (1, 0): 5
    },
    3: {
        (0, 1): None,
        (0, -1): None,
        (-1, 0): 4,
        (1, 0): 2
    },
    4: {
        (0, 1): None,
        (0, -1): 3,
        (-1, 0): 1,
        (1, 0): None
    },
    5: {
        (0, 1): 6,
        (0, -1): None,
        (-1, 0): None,
        (1, 0): 2
    },
    6: {
        (0, 1): 2,
        (0, -1): None,
        (-1, 0): 1,
        (1, 0): 5
    }
}


class Puzzle(PuzzleBase):
    year = 2022
    day = 22

    should_strip_data = False

    grid: Grid
    steps = []

    face_size: int
    cube_layout: Grid

    position: Point = (0, 0)
    facing: Point = (1, 0)

    is_cube = False
    is_sample = False

    def reset(self):
        self.grid = Grid.create_empty(0, 0, WRAP_TILE)
        self.steps = []

        self.face_size = 1
        self.cube_layout = Grid.create_empty(0, 0, WRAP_TILE)

        self.position = (0, 0)
        self.facing = (1, 0)

    def prepare_data(self, input_data: List[str], current_part: int):
        grid_lines = []
        reading_grid = True

        for i in range(len(input_data)):
            line = input_data[i].replace('\n', '')

            if reading_grid:
                if line == '':
                    self.grid = Grid.from_strings(grid_lines, WRAP_TILE)
                    reading_grid = False
                    continue

                grid_lines.append(line)
            else:
                substr = ''
                for char in line:
                    if char in '0123456789':
                        substr += char
                    else:
                        if substr != '':
                            self.steps.append(int(substr))
                            substr = ''
                        self.steps.append(char)

                if substr != '':
                    self.steps.append(int(substr))

    def get_first_walkable_tile(self, scan_from: Point, direction: Point):
        dx, dy = direction
        sx, sy = scan_from

        if dx != 0 and dy != 0:
            print(f'Invalid step: {direction}')
            return

        is_x = dx != 0
        step = dx if is_x else dy

        start = 0
        stop = self.grid.width if is_x else self.grid.height

        if step < 0:
            start = stop - 1
            stop = -1

        for i in range(start, stop, step):
            next_pos = (i, sy) if is_x else (sx, i)
            next_tile = self.grid[next_pos]

            if next_tile is None:
                continue
            elif next_tile == WALL_TILE:
                return self.position
            elif next_tile == EMPTY_TILE or next_tile in '<>^v':
                return next_pos

        return self.position

    def wrap_to_cube_face(self):
        # finding where in the face meta-grid we are
        px, py = self.position
        fx, fy = px // self.face_size, py // self.face_size

        # getting the distance from this face's origin point (top left)
        ox, oy = fx * self.face_size, fy * self.face_size

        if self.facing == (1, 0):
            # align to right edge
            ox += self.face_size - 1
        elif self.facing == (0, 1):
            # align to bottom edge
            oy += self.face_size - 1

        dx, dy = (px - ox, py - oy)

        # getting the next face (hardcoded for now)
        face_id = self.cube_layout[(fx, fy)]
        face_links = SAMPLE_HARDCODED_LINKS if self.is_sample else HARDCODED_LINKS
        next_face_id = face_links[face_id][self.facing]

        # placing ourselves relative to the new face's origin
        new_fx, new_fy = [point for point in self.cube_layout.grid if self.cube_layout[point] == next_face_id][0]
        new_ox, new_oy = new_fx * self.face_size, new_fy * self.face_size

        new_facing = [key for key in face_links[next_face_id].keys() if face_links[next_face_id][key] == face_id][0]

        if new_facing == (1, 0):
            # align to right edge
            new_ox += self.face_size - 1
        elif new_facing == (0, 1):
            # align to bottom edge
            new_oy += self.face_size - 1

        if abs(self.facing[0]) != abs(new_facing[0]):
            # we're switching from horizontal to vertical or vice versa, so dx&dy need to be flipped as well
            if dx != 0:
                dy = (self.face_size - 1 - dx) if self.facing[1] != new_facing[0] else dx
                dx = 0
            else:
                dx = (self.face_size - 1 - dy) if self.facing[0] != new_facing[1] else dy
                dy = 0
        elif self.facing[0] != 0 and self.facing[0] == new_facing[0]:
            # We're switching directions vertically, so just flip y
            dy = self.face_size - 1 - dy
        elif self.facing[1] != 0 and self.facing[1] == new_facing[1]:
            # We're switching directions horizontally, so just flip x
            dx = self.face_size - 1 - dx

        new_pos = (new_ox + dx, new_oy + dy)
        if self.grid[new_pos] == WALL_TILE:
            # nevermind, we can't move
            return self.position

        self.position = new_pos

        # changing our facing direction to re-orient to our destination
        self.facing = (new_facing[0] * -1, new_facing[1] * -1)

        return self.position

    def get_next_pos(self):
        px, py = self.position
        dx, dy = self.facing
        nx, ny = next_pos = (px + dx, py + dy)

        if self.grid[next_pos] == WALL_TILE:
            return self.position
        elif self.grid[next_pos] == WRAP_TILE or self.grid[next_pos] is None:
            if self.is_cube:
                return self.wrap_to_cube_face()

            return self.get_first_walkable_tile(self.position, self.facing)
        else:
            return next_pos

    def move(self):
        next_movement = self.steps[0]
        self.steps = self.steps[1:]

        fx, fy = self.facing

        if isinstance(next_movement, int):
            for _ in range(next_movement):
                last_pos = self.position
                self.position = self.get_next_pos()

                if self.position == last_pos:
                    break

                self.grid[self.position] = FACING_TILES[self.facing]
        elif next_movement == 'L':
            if fx != 0:
                self.facing = (0, -fx)
            else:
                self.facing = (fy, 0)

            self.grid[self.position] = FACING_TILES[self.facing]

        elif next_movement == 'R':
            if fy != 0:
                self.facing = (-fy, 0)
            else:
                self.facing = (0, fx)

            self.grid[self.position] = FACING_TILES[self.facing]

    def parse_cube_faces(self):
        self.face_size = math.gcd(self.grid.width, self.grid.height)

        faces_width = self.grid.width // self.face_size
        faces_height = self.grid.height // self.face_size

        self.cube_layout = Grid.create_empty(faces_width, faces_height, WRAP_TILE)

        face_count = 1
        for y in range(faces_height):
            for x in range(faces_width):
                if self.grid[(x * self.face_size, y * self.face_size)] in [EMPTY_TILE, WALL_TILE]:
                    self.cube_layout[(x, y)] = face_count
                    face_count += 1

    def get_score(self):
        px, py = self.position

        return 1000 * (py + 1) + 4 * (px + 1) + FACING_MULTIPLIER[self.facing]

    def get_day_1_answer(self, use_sample=False) -> str:
        self.is_cube = False
        self.is_sample = use_sample

        self.position = self.get_first_walkable_tile((0, 0), (1, 0))

        while len(self.steps):
            self.move()

        return str(self.get_score())

    def get_day_2_answer(self, use_sample=False) -> str:
        self.is_cube = True
        self.is_sample = use_sample

        self.parse_cube_faces()
        print(self.cube_layout)

        self.position = self.get_first_walkable_tile((0, 0), (1, 0))

        while len(self.steps):
            self.move()

        print(self.grid)

        return str(self.get_score())


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
