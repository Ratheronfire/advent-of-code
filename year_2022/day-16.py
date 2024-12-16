import functools
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

    # runner_states: (current room id, dest room id, turns until arrived (if 0, needs a new room))
    @functools.lru_cache(maxsize=None)
    def get_highest_subpath(self, runner_states: tuple, opened_rooms: tuple, minutes_left: int, points_so_far=0):
        total_permutations = math.factorial(len([r for r in self.rooms.values() if r.rate > 0]))

        cache = self.get_highest_subpath.cache_info()

        if (cache.hits + cache.misses) % 100000 == 0:
            print(f'{cache.hits + cache.misses}/{total_permutations} runs ({100*(cache.hits + cache.hits)/total_permutations}%)')

        opened_rooms = list(opened_rooms)

        # rooms that no runner has reached
        remaining_rooms = [r for r in self.rooms.values()
                           if r.rate > 0 and
                           r.id not in opened_rooms and r.id not in [s[1] for s in runner_states]]

        # preparing the next set of rooms
        next_room_candiates = []
        for i in range(len(runner_states)):
            next_room_candiates.append([])

        for i, runner_state in enumerate(runner_states):
            # getting all the possible next rooms for any runners that are ready
            if runner_state[1] is None or runner_state[2] <= 0:
                if runner_state[1] is not None:
                    opened_rooms += [runner_state[1]]
                    # print(f'Minute {minutes_left}: Opened valve {runner_state[1]}.')

                for next_room in remaining_rooms:
                    minutes_taken = len(self.cached_room_paths[(runner_state[0], next_room.id)]) + 1
                    minutes_left_after = minutes_left - minutes_taken

                    if minutes_left_after >= 0:
                        next_room_candiates[i].append(next_room.id)

        # getting the pressure released this step
        pressure_released = sum([r.rate for r in self.rooms.values() if r.id in opened_rooms])
        # print(f'Minute {minutes_left}: {points_so_far} total, {pressure_released} pressure released this turn. {opened_rooms}')

        # reached the end of this chain
        if minutes_left <= 0:
            print(f'{minutes_left} minutes left. Total pressure: {points_so_far + pressure_released}; Opened valves: {opened_rooms}')
            return points_so_far + pressure_released

        # turning the possible rooms into pairs if applicable
        candidate_pairs = []
        if len(next_room_candiates) == 1:
            candidate_pairs = [tuple([room]) for room in next_room_candiates[0]]
        elif len (next_room_candiates[0]) == 0:
            candidate_pairs = [(None, room) for room in next_room_candiates[1]]
        elif len (next_room_candiates[1]) == 0:
            candidate_pairs = [(room, None) for room in next_room_candiates[0]]
        else:
            for room_a in next_room_candiates[0]:
                for room_b in next_room_candiates[1]:
                    if room_a != room_b:
                        candidate_pairs.append((room_a, room_b))

        # finding the results of each candidate pair
        results = []
        for candidate_pair in candidate_pairs:
            new_states = list([list(s).copy() for s in runner_states]).copy()

            for i, runner_state in enumerate(new_states):
                if candidate_pair[i] is not None:
                    runner_state[0] = runner_state[1] if runner_state[1] is not None else runner_state[0]
                    runner_state[1] = candidate_pair[i]
                    runner_state[2] = len(self.cached_room_paths[runner_state[0], runner_state[1]]) + 1

            # advancing to whichever runner has their next state change
            minute_gap = min([s[2] for s in new_states])
            next_minute_point = minutes_left - minute_gap

            if next_minute_point < 0:
                print(
                    f'next_minute_point too large ({next_minute_point}). Total pressure: {points_so_far + pressure_released * minutes_left}; Opened valves: {opened_rooms}')
                return points_so_far + pressure_released * minutes_left

            for runner_state in new_states:
                runner_state[2] = runner_state[2] - minute_gap

            results.append(self.get_highest_subpath(tuple([tuple(s) for s in new_states]),
                                                    tuple(opened_rooms.copy()),
                                                    next_minute_point,
                                                    points_so_far + minute_gap * pressure_released))

        if len(results) == 0:
            # finishing any last traversals when all rooms are claimed or open
            final_points = points_so_far + pressure_released * minutes_left

            new_states = list([list(s).copy() for s in runner_states]).copy()

            minute_gap = min([s[2] for s in new_states if s[2] > 0] if any([s[2] > 0 for s in new_states]) else [0])
            next_minute_point = minutes_left - minute_gap

            for runner_state in new_states:
                if runner_state[2] <= 0:
                    runner_state[1] = None

            for runner_state in new_states:
                if runner_state[2] > 0:
                    runner_state[2] = 0

                    final_points = self.get_highest_subpath(tuple([tuple(s) for s in new_states]),
                                                            tuple(opened_rooms.copy()),
                                                            next_minute_point,
                                                            points_so_far + minute_gap * pressure_released)

            print(
                f'Finished final traversal. Total pressure: {final_points}; Opened valves: {opened_rooms}')
            return final_points

        return max(results)

    def get_part_1_answer(self, use_sample=False) -> str:
        self.precalculate_room_traversals()

        best_score = self.get_highest_subpath(tuple([('AA', None, 0)]), (), 30)
        self.get_highest_subpath.cache_clear()

        return str(best_score)

    def get_part_2_answer(self, use_sample=False) -> str:
        self.precalculate_room_traversals()

        best_score = self.get_highest_subpath(tuple([('AA', None, 0), ('AA', None, 0)]), (), 26)
        self.get_highest_subpath.cache_clear()

        return str(best_score)

    def to_mermaidjs_str(self):
        out_str = 'graph TD\n    Start --> AA\n'

        for room in self.rooms.values():
            for neighbor in room.neighbors:
                out_str += '    %s --> %s\n' % (room.id + ('{%s: %d}' % (room.id, room.rate) if room.rate > 0 else ''), neighbor)

        return out_str


puzzle = Puzzle()
print(puzzle.test_and_run(True))
