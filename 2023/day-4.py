import re
from typing import List

from puzzle_base import PuzzleBase


class Card:
    id: int

    winning_numbers: list[int]
    found_numbers: list[int]

    def __init__(self, id: int, winning_numbers, found_numbers):
        self.id = id

        self.winning_numbers = winning_numbers
        self.found_numbers = found_numbers


class Puzzle(PuzzleBase):
    year = 2023
    day = 4

    cards: list[Card]

    def reset(self):
        self.cards = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            number_str = re.split(': +', line)[1]

            winners, found = number_str.split(' | ')

            self.cards.append(Card(
                len(self.cards) + 1,
                [int(n.strip()) for n in re.split(' +', winners.strip())],
                [int(n.strip()) for n in re.split(' +', found.strip())]
            ))

    def get_win_count(self, card: Card):
        return len([n for n in card.found_numbers if n in card.winning_numbers])

    def get_day_1_answer(self, use_sample=False) -> str:
        total = 0

        for card in self.cards:
            win_count = self.get_win_count(card)

            if win_count:
                total += 2 ** (win_count - 1)

        return str(total)

    def get_day_2_answer(self, use_sample=False) -> str:
        cards_owned = {card.id: 1 for card in self.cards}

        current_card = self.cards[0]
        card_score = self.get_win_count(current_card)
        cards_owned[current_card.id] = 1

        while current_card is not None:
            for i in range(current_card.id + 1, current_card.id + 1 + card_score):
                if i in cards_owned:
                    cards_owned[i] = cards_owned[i] + cards_owned[current_card.id]
                else:
                    cards_owned[i] = cards_owned[current_card.id]

            if current_card.id < len(self.cards):
                current_card = self.cards[current_card.id]
                card_score = self.get_win_count(current_card)
            else:
                current_card = None

        return str(sum(cards_owned.values()))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
