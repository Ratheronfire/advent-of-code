from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 2

    inputs = ["A", "B", "C"]
    outputs = ["X", "Y", "Z"]

    score = 0

    def reset(self):
        self.score = 0

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            if line == '':
                continue

            plays = line.strip().split(' ')

            input_score = self.inputs.index(plays[0])
            output_score = self.outputs.index(plays[1])

            winning_play = input_score + 1 if input_score < 2 else 0
            losing_play = input_score - 1 if input_score > 0 else 2

            if current_part == 1:
                self.score += output_score + 1  # base score

                if input_score == output_score:  # draw
                    self.score += 3
                elif output_score == winning_play:
                    self.score += 6
            elif current_part == 2:
                if output_score == 0:  # lose
                    self.score += losing_play + 1
                elif output_score == 1:  # draw
                    self.score += 3 + input_score + 1
                elif output_score == 2:  # win
                    self.score += 6 + winning_play + 1

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.score)

    def get_day_2_answer(self, use_sample=False) -> str:
        return str(self.score)


puzzle = Puzzle()
print(puzzle.test_and_run())
