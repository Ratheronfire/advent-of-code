def get_message_start_point(input, unique_char_count):
    recent_chars = []
    index = 0

    for char in input:
        if len(recent_chars) >= unique_char_count:
            recent_chars = recent_chars[1:]

        recent_chars += char

        if len(set(recent_chars)) == unique_char_count:
            return index + 1

        index += 1


input_path = "inputs/day-6.txt"

with open(input_path, 'r') as input_file:
    input_line = input_file.read()

print(get_message_start_point(input_line, 4))
print(get_message_start_point(input_line, 14))
