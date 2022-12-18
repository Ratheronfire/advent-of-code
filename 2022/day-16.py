import itertools
import math
import operator
import re
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


class Puzzle(PuzzleBase):
    year = 2022
    day = 16

    minutes = 30
    pressure_released = 0
    rooms: dict[str, Room] = {}

    cached_room_paths = {}

    def reset(self):
        self.minutes = 30
        self.pressure_released = 0
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

        visited_rooms = [current_room]
        room_queue = [current_room]

        starting_room = current_room

        parents = {}

        # first, BFS to find the goal
        while len(room_queue):
            current_room = room_queue.pop()
            if current_room == goal_room:
                break

            for neighbor_id in current_room.neighbors:
                neighbor = self.rooms[neighbor_id]
                if neighbor in visited_rooms:
                    continue

                visited_rooms.append(neighbor)
                parents[neighbor] = current_room
                room_queue.append(neighbor)

        # now, backtrack
        path_to_room = []
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

    def calculate_ideal_score(self, rooms):
        score = 0
        for i in range(len(rooms)):
            room = rooms[i]

            if isinstance(room, str):
                room = self.rooms[room]

            score += room.rate * (28 - i * 2)

        return score

    def release_pressure(self):
        if self.minutes <= 0:
            return

        pressure = sum([r.rate for r in self.rooms.values() if r.open])
        # print('Minute %d: releasing %d pressure.' % (30 - self.minutes + 1, pressure))
        self.pressure_released += pressure

    def navigate_caves(self, room: Room, hardcoded_room_order: list[Room] = None):
        current_path: list[Room] = []

        self.minutes = 30
        self.pressure_released = 0

        for _room in self.rooms.values():
            _room.open = False

        while self.minutes > 0:
            if len(current_path) == 0:
                if hardcoded_room_order is None:
                    possible_targets = [(r, self.get_path_to_target(room, r))
                                        for r in self.rooms.values() if not r.open and r.rate > 0]
                    possible_targets = sorted(possible_targets, key=lambda r: r[0].rate / len(r[1]) ** 2, reverse=True)

                    current_path = possible_targets[0][1] if len(possible_targets) else []
                elif len(hardcoded_room_order):
                    next_room = hardcoded_room_order[0]
                    hardcoded_room_order = hardcoded_room_order[1:]

                    current_path = self.get_path_to_target(room, next_room)

            if len(current_path):
                # print('Going to room %s.' % current_path[0].id)
                room = current_path[0]
                current_path = current_path[1:]

                if len(current_path) == 0:
                    self.minutes -= 1

                    # print('Opening valve %s; %d minute(s) left.' % (room.id, self.minutes))
                    self.release_pressure()

                    room.open = True

            self.minutes -= 1

            self.release_pressure()

        return self.pressure_released

    def find_chained_nodes(self):
        chains = []

        #  Get all nodes that have only one neighbor
        dead_ends = [r for r in self.rooms.values() if r.rate > 0 and len(r.neighbors) == 1]
        for dead_end in dead_ends:
            chain = []

            current_node = dead_end

            #  Walking back to the last node in this one-way route
            while len(current_node.neighbors) <= 2:
                chain.append(current_node)
                neighbors = [n for n in current_node.neighbors if not self.rooms[n] in chain]
                current_node = self.rooms[neighbors[0]]

            #  Filtering out nodes that have 0 rate
            chain = [n for n in chain if n.rate > 0]

            if len(chain) > 1:
                #  Now finding the ideal permutation for this chain.
                best_permutation = self.find_highest_permutation(chain[-1], chain)

                chain = best_permutation[1]

            chains.append(chain)

        return chains

    def find_highest_permutation(self, starting_room: Room, room_ids: list[Union[Room, list[Room]]]):
        best_so_far = 0
        best_permutation = []

        total_runs = math.factorial(len(room_ids))
        i = 0
        for permutation in itertools.permutations(room_ids):
            if isinstance(permutation, Room):
                permutation = [permutation]

            #  flattening the list down, to preserve precalculated chains
            flat_permutation = []
            for item in permutation:
                if isinstance(item, Room):
                    flat_permutation.append(item)
                elif isinstance(item, list):
                    flat_permutation += item

            if best_so_far > self.calculate_ideal_score(flat_permutation):
                print('Skipping.')
                continue

            new_score = self.navigate_caves(starting_room, flat_permutation)

            if new_score > best_so_far:
                best_so_far = new_score
                best_permutation = flat_permutation
                print('New best score: %d (%s).' % (new_score, ', '.join([r.id for r in flat_permutation])))

            i += 1

            if i > 0 and i % 100000 == 0:
                print('%d/%d (%d%%).' % (i, total_runs, 100 * i / total_runs))

        return best_so_far, best_permutation

    def get_day_1_answer(self, use_sample=False) -> str:
        self.precalculate_room_traversals()

        starting_room = self.rooms['AA']

        all_scoring_rooms = sorted([r for r in self.rooms.values() if r.rate > 0], key=lambda r: r.rate)

        chains = self.find_chained_nodes()
        for chain in chains:
            for room in chain:
                all_scoring_rooms.remove(room)
            all_scoring_rooms.append(chain)

        best_so_far = self.find_highest_permutation(starting_room, all_scoring_rooms)

        return str(best_so_far[0])

    def get_day_2_answer(self, use_sample=False) -> str:
        return ''

    def to_mermaidjs_str(self):
        out_str = 'graph TD\n    Start --> AA\n'

        for room in self.rooms.values():
            for neighbor in room.neighbors:
                out_str += '    %s --> %s\n' % (room.id + ('{%s: %d}' % (room.id, room.rate) if room.rate > 0 else ''), neighbor)

        return out_str


puzzle = Puzzle()
print(puzzle.test_and_run())
