input_path = "inputs/day-2.txt"

inputs = ["A", "B", "C"]
outputs = ["X", "Y", "Z"]

score = 0
correct_score = 0

with open(input_path, 'r') as input_file:
    for line in input_file.readlines():
        plays = line.strip().split(' ')

        input_score = inputs.index(plays[0])
        output_score = outputs.index(plays[1])

        winning_play = input_score + 1 if input_score < 2 else 0
        losing_play = input_score - 1 if input_score > 0 else 2

        score += output_score + 1  # base score

        part_1_result = 'Lose'
        if input_score == output_score:  # draw
            part_1_result = 'Draw'
            score += 3
        elif output_score == winning_play:
            part_1_result = 'Win'
            score += 6

        # print('%s vs. %s; %s (+%d)' % (plays[0], plays[1], part_1_result, output_score + 1))

        # part 2
        part_2_score = 0
        if output_score == 0:  # lose
            part_2_score = losing_play + 1
        elif output_score == 1:  # draw
            part_2_score = 3 + input_score + 1
        elif output_score == 2:  # win
            part_2_score = 6 + winning_play + 1

        # print('%s - %s; %d' % (plays[0], ['Lose', 'Draw', 'Win'][output_score], part_2_score))
        correct_score += part_2_score

print(score)
print(correct_score)
