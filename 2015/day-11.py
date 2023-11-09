from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2015
    day = 11

    start_password = ''

    def reset(self):
        self.start_password = ''

    def prepare_data(self, input_data: List[str], current_part: int):
        self.start_password = input_data[0]

    def increment(self, password: str) -> str:
        letter_ords = [ord(c) for c in password]
        letter_ords[-1] = letter_ords[-1] + 1

        for i in range(len(letter_ords) - 1, -1, -1):
            if letter_ords[i] > ord('z'):
                letter_ords[i] = ord('a')

                if i > 0:
                    letter_ords[i - 1] += 1
                else:
                    letter_ords.insert(0, ord('a'))

        return ''.join([chr(o) for o in letter_ords])

    def is_valid(self, password: str) -> bool:
        if 'i' in password or 'o' in password or 'l' in password:
            return False

        has_straight = False
        pairs = []

        for i in range(len(password)):
            if i < len(password) - 2 and \
                    ord(password[i + 1]) == ord(password[i]) + 1 and \
                    ord(password[i + 2]) == ord(password[i + 1]) + 1:
                has_straight = True

            if i < len(password) - 1 and password[i] == password[i + 1] and i not in pairs and i+1 not in pairs:
                pairs.append(i)
                pairs.append(i + 1)

        return has_straight and len(pairs) >= 4

    def get_next_password(self, password: str) -> str:
        while not self.is_valid(password):
            password = self.increment(password)

        return password

    def get_day_1_answer(self, use_sample=False) -> str:
        return self.get_next_password(self.start_password)

    def get_day_2_answer(self, use_sample=False) -> str:
        password = self.get_next_password(self.start_password)
        password = self.increment(password)

        return self.get_next_password(password)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
