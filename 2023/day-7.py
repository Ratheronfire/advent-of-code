from functools import cmp_to_key
from typing import List

from puzzle_base import PuzzleBase

CARD_VALUES = [
    '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'
]

CARD_VALUES_P2 = [
    'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'
]

HAND_VALUES = [
    'High card', 'One pair', 'Two pair', 'Three of a kind', 'Full house', 'Four of a kind', 'Five of a kind', 'No hand'
]


class Hand:
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid

    def get_numeric_value(self, is_part_2=False):
        val = 0

        for card in self.cards:
            val += CARD_VALUES_P2.index(card) if is_part_2 else CARD_VALUES.index(card)
            val *= len(CARD_VALUES) + 1  # val will be a number in base 14

        return val

    def get_hand_type(self):
        unique_cards = set(self.cards)

        if len(unique_cards) == 1:
            return 6
        elif len(unique_cards) == 2 and any([self.cards.count(c) == 4 for c in unique_cards]):
            return 5
        elif len(unique_cards) == 2 and any([self.cards.count(c) == 3 for c in unique_cards]):
            return 4
        elif len(unique_cards) == 3 and any([self.cards.count(c) == 3 for c in unique_cards]):
            return 3
        elif len(unique_cards) == 3 and len([c for c in unique_cards if self.cards.count(c) == 2]) == 2:
            return 2
        elif len(unique_cards) == 4 and any([self.cards.count(c) == 2 for c in unique_cards]):
            return 1
        elif len(unique_cards) == 5:
            return 0

        return -1

    def get_hand_type_p2(self):
        j_count = self.cards.count('J')
        unique_cards = set([c for c in self.cards if c != 'J'])

        if j_count == 0:
            return self.get_hand_type()
        elif j_count > 3 or len(unique_cards) == 1:
            return 6
        elif j_count == 3:
            return 5
        elif j_count == 2:
            return 5 if len(unique_cards) == 2 else 3
        else:
            if len(unique_cards) == 2:
                return 5 if any([self.cards.count(c) == 3 for c in unique_cards]) else 4
            else:
                return 3 if len(unique_cards) == 3 else 1

    def __str__(self):
        return f'{self.cards} ({HAND_VALUES[self.get_hand_type()]}; numeric value={self.get_numeric_value()})'


class Puzzle(PuzzleBase):
    year = 2023
    day = 7

    hands: list[Hand]

    def reset(self):
        self.hands = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line != '':
                self.hands.append(Hand(line.split()[0], int(line.split()[1])))

    def compare_hands(self, left: Hand, right: Hand):
        a_hand = left.get_hand_type()
        b_hand = right.get_hand_type()

        if a_hand > b_hand:
            return -1
        elif b_hand > a_hand:
            return 1
        else:
            return -1 if left.get_numeric_value() > right.get_numeric_value() else 1

    def compare_hands_p2(self, left: Hand, right: Hand):
        a_hand = left.get_hand_type_p2()
        b_hand = right.get_hand_type_p2()

        if a_hand > b_hand:
            return -1
        elif b_hand > a_hand:
            return 1
        else:
            return -1 if left.get_numeric_value(True) > right.get_numeric_value(True) else 1

    def get_part_1_answer(self, use_sample=False) -> str:
        self.hands = sorted(self.hands, key=cmp_to_key(self.compare_hands), reverse=True)

        return str(sum([(i + 1) * h.bid for i, h in enumerate(self.hands)]))

    def get_part_2_answer(self, use_sample=False) -> str:
        self.hands = sorted(self.hands, key=cmp_to_key(self.compare_hands_p2), reverse=True)

        return str(sum([(i + 1) * h.bid for i, h in enumerate(self.hands)]))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
