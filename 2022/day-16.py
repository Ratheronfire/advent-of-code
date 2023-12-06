import itertools
import math
import operator
import re
import sys
from functools import reduce
from typing import List, Union

from helpers.grid import Grid
from puzzle_base import PuzzleBase


class Room:
    id: str
    rate: int
    neighbors: list[str]

    open = False

    def __init__(self, id, rate, neighbors):
        self.id = id
        self.rate = rate
        self.neighbors = neighbors

    def __str__(self):
        return '%s - Rate %d - %s' % (self.id, self.rate, ('Open' if self.open else 'Closed'))


class Puzzle(PuzzleBase):
    year = 2022
    day = 16

    rooms: dict[str, Room] = {}
    cached_room_paths = {}

    def reset(self):
        self.rooms = {}
        self.cached_room_paths = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i].strip()

            if line == '':
                continue

            match = re.match(r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)', line)
            self.rooms[match[1]] = Room(match[1], int(match[2]), match[3].split(', '))

    def get_path_to_target(self, current_room: Room, goal_room: Room) -> list[Room]:
        cached_index = (current_room.id, goal_room.id)
        if cached_index in self.cached_room_paths:
            return self.cached_room_paths[cached_index]

        room_queue = [r for r in self.rooms.values()]

        starting_room = current_room

        parents = {}
        distances = {key: sys.maxsize for key in self.rooms.keys()}
        distances[current_room.id] = 0

        # first, BFS to find the goal
        while len(room_queue):
            room_queue = sorted(room_queue, key=lambda r: distances[r.id], reverse=True)
            current_room = room_queue.pop()

            for neighbor_id in current_room.neighbors:
                neighbor = self.rooms[neighbor_id]
                if neighbor not in room_queue:
                    continue

                new_distance = distances[current_room.id] + 1
                if new_distance < distances[neighbor.id]:
                    distances[neighbor.id] = new_distance
                    parents[neighbor] = current_room
                    room_queue.append(neighbor)

        # now, backtrack
        path_to_room = []
        current_room = goal_room
        while current_room != starting_room:
            path_to_room.append(current_room)
            current_room = parents[current_room]

        path_to_room.reverse()

        self.cached_room_paths[cached_index] = path_to_room
        return path_to_room

    def precalculate_room_traversals(self):
        for room_a in self.rooms.values():
            for room_b in self.rooms.values():
                if room_a != room_b:
                    self.cached_room_paths[(room_a, room_b)] = self.get_path_to_target(room_a, room_b)

    def get_released_pressure(self):
        return sum([r.rate for r in self.rooms.values() if r.open])

    def navigate_caves(self, starting_room: Room, minutes_left, score_so_far=0, opened_rooms=None):
        if opened_rooms is None:
            opened_rooms = []

        current_path: list[Room] = []

        remaining_rooms = [r for r in self.rooms.values()
                           if r.rate > 0 and
                           r not in opened_rooms]

        score_per_turn = sum([r.rate for r in self.rooms.values() if r in opened_rooms])

        while len(remaining_rooms) > 0:
            if len(current_path) == 0:
                next_room = remaining_rooms.pop()
                current_path = self.get_path_to_target(starting_room, next_room)

            if len(current_path):
                # print('Going to room %s.' % current_path[0].id)
                starting_room = current_path[0]
                current_path = current_path[1:]

                if len(current_path) == 0:
                    minutes_left -= 1
                    print('Minute %d: Opening valve %s (rate = %d, total pressure = %d).' %
                          (30 - minutes_left + 1, starting_room.id, starting_room.rate, starting_room.rate * (minutes - 1)))

                    if minutes_left > 0:
                        score_so_far += self.get_released_pressure()

                    starting_room.open = True

            minutes_left -= 1
            if minutes_left > 0:
                score_so_far += self.get_released_pressure()

        return score_so_far + score_per_turn * minutes_left

    def get_highest_subpath_part1(self, starting_room, minutes_left=30, score_so_far=0, opened_rooms=None):
        if opened_rooms is None:
            opened_rooms = []

        remaining_rooms = [r for r in self.rooms.values()
                           if r.rate > 0 and
                           r not in opened_rooms]

        score_per_turn = sum([r.rate for r in self.rooms.values() if r in opened_rooms])

        if len(remaining_rooms) == 0:
            return score_so_far + score_per_turn * minutes_left
        else:
            subpath_totals = []
            for next_room in remaining_rooms:
                minutes_taken = len(self.cached_room_paths[(starting_room.id, next_room.id)]) + 1

                sub_minutes_left = minutes_left - minutes_taken
                if sub_minutes_left < 0:
                    continue

                sub_score_so_far = score_so_far + minutes_taken * score_per_turn
                sub_opened_rooms = [r for r in opened_rooms]
                sub_opened_rooms.append(next_room)

                subpath_totals.append((next_room, self.get_highest_subpath_part1(next_room, sub_minutes_left, sub_score_so_far, sub_opened_rooms)))

            max_possible_score = score_so_far + score_per_turn * minutes_left
            if len(subpath_totals):
                max_path = max(subpath_totals, key=lambda r: r[1])
                max_possible_score = max_path[1]

            return max_possible_score

    def get_highest_subpath_part2(self, starting_room, minutes_left=None, score_so_far=0, opened_rooms=None):
        if minutes_left is None:
            minutes_left = [26, 26]
        if opened_rooms is None:
            opened_rooms = []

        remaining_rooms = [r for r in self.rooms.values()
                           if r.rate > 0 and
                           r not in opened_rooms]

        score_per_turn = sum([r.rate for r in self.rooms.values() if r in opened_rooms])

        if len(remaining_rooms) == 0:
            return score_so_far + score_per_turn * minutes_left[0]
        else:
            subpath_totals = []
            while len(remaining_rooms) > 0:
                if minutes_left[0] == minutes_left[1]:
                    if len(remaining_rooms) > 1:
                        next_moves = [remaining_rooms[0], remaining_rooms[1]]
                    else:
                        next_moves = [remaining_rooms[0], None]
                elif minutes_left[0] > minutes_left[1]:
                    next_moves = [remaining_rooms[0], None]
                else:
                    next_moves = [None, remaining_rooms[0]]

                minutes_taken = [
                    (len(self.cached_room_paths[(starting_room.id, next_moves[0].id)]) + 1) if next_moves else 0,
                    (len(self.cached_room_paths[(starting_room.id, next_moves[1].id)]) + 1) if next_moves else 0
                ]

                sub_minutes_left = [minutes_left[0] - minutes_taken[0], minutes_left[1] - minutes_taken[1]]
                if sub_minutes_left[0] < 0 and sub_minutes_left[1] < 0:
                    continue
                elif sub_minutes_left[0] < 0:
                    next_moves[0] = None
                    minutes_taken[0] = 0
                elif sub_minutes_left[1] < 0:
                    next_moves[1] = None
                    minutes_taken[1] = 0

                if next_moves[0]:
                    remaining_rooms = remaining_rooms[1:]
                if next_moves[1]:
                    remaining_rooms = remaining_rooms[1:]

                sub_score_so_far = score_so_far + minutes_taken * score_per_turn
                sub_opened_rooms = [r for r in opened_rooms]
                sub_opened_rooms.append(next_room)

                subpath_totals.append((next_room, self.get_highest_subpath_part2(next_room, sub_minutes_left, sub_score_so_far, sub_opened_rooms)))

            max_possible_score = score_so_far + score_per_turn * minutes_left
            if len(subpath_totals):
                max_path = max(subpath_totals, key=lambda r: r[1])
                max_possible_score = max_path[1]

            return max_possible_score

    def get_part_1_answer(self, use_sample=False) -> str:
        self.precalculate_room_traversals()

        starting_room = self.rooms['AA']

        best_score = self.get_highest_subpath_part1(starting_room)

        return str(best_score)

    def get_part_2_answer(self, use_sample=False) -> str:
        self.precalculate_room_traversals()

        starting_rooms = [self.rooms['AA'], self.rooms['AA']]

        best_score = self.get_highest_subpath_part2(starting_rooms, [26, 26])

        return str(best_score)
        return ''

    def to_mermaidjs_str(self):
        out_str = 'graph TD\n    Start --> AA\n'

        for room in self.rooms.values():
            for neighbor in room.neighbors:
                out_str += '    %s --> %s\n' % (room.id + ('{%s: %d}' % (room.id, room.rate) if room.rate > 0 else ''), neighbor)

        return out_str


puzzle = Puzzle()
print(puzzle.test_and_run(False))
