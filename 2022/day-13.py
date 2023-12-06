from copy import deepcopy
from functools import cmp_to_key
from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 13

    packets = []

    def reset(self):
        self.packets = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i].strip()

            if line == '':
                continue

            self.packets.append(self.parse_packet(line)[0])

    def parse_packet(self, line):
        packet = []

        curr_num_str = ''

        i = 1
        while i < len(line):
            char = line[i]

            if char == '[':
                subarray = line[i:]

                sub_packet, sub_i = self.parse_packet(subarray)
                packet.append(sub_packet)

                i += sub_i + 1
            elif char in '0123456789':
                curr_num_str += char

                i += 1
            elif char in '],':
                if curr_num_str != '':
                    packet.append(int(curr_num_str))
                    curr_num_str = ''

                if char == ']':
                    break

                i += 1

        return packet, i

    # -1 = False, 1 = True, 0 = Indeterminate
    def are_values_sorted(self, left, right):
        left = deepcopy(left)
        right = deepcopy(right)

        left_is_num = isinstance(left, int)
        right_is_num = isinstance(right, int)

        if left_is_num and not right_is_num:
            left = [left]
        elif not left_is_num and right_is_num:
            right = [right]

        if isinstance(left, int):

            if left == right:
                return 0
            return 1 if left < right else -1
        else:
            while len(left) > 0 and len(right) > 0:
                inner_left = left[0]
                inner_right = right[0]

                left.remove(inner_left)
                right.remove(inner_right)

                inner_sort_state = self.are_values_sorted(inner_left, inner_right)
                if inner_sort_state == -1:
                    return -1
                elif inner_sort_state == 1:
                    return 1

            if len(left) == 0 and len(right) == 0:
                return 0
            elif len(left) == 0:
                return 1
            elif len(right) == 0:
                return -1

        return 1

    def get_part_1_answer(self, use_sample=False) -> str:
        good_packets = []

        for i in range(0, len(self.packets), 2):
            left_packet = self.packets[i]
            right_packet = self.packets[i + 1]

            if self.are_values_sorted(left_packet, right_packet) == 1:
                good_packets.append(i // 2 + 1)

        return str(sum(good_packets))

    def get_part_2_answer(self, use_sample=False) -> str:
        decoder_keys = ([[2]], [[6]])

        self.packets.append(decoder_keys[0])
        self.packets.append(decoder_keys[1])

        self.packets = sorted(self.packets, key=cmp_to_key(self.are_values_sorted), reverse=True)

        decoder_indices = (self.packets.index(decoder_keys[0]) + 1, self.packets.index(decoder_keys[1]) + 1)

        return str(decoder_indices[0] * decoder_indices[1])


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
