import json
import os
import re
from os import path
from sys import argv


def prepare_year(year):
    sample_data = []

    if not path.isdir(year):
        os.mkdir(year)

    input_folder = path.join(year, "inputs")
    if not path.isdir(input_folder):
        os.mkdir(input_folder)

    with open("puzzle-sample.py", 'r') as sample_file:
        sample_text = sample_file.read()

    for i in range(1, 26):
        sample_data.append({
            "day": i,
            "input_data": "",
            "answer_1": "",
            "answer_2": ""
        })

        script_path = path.join(year, f"day-{i}.py")
        if not path.isfile(script_path):
            with open(script_path, 'w') as script_file:
                script_text = sample_text
                script_text = re.sub(r"year = \d+", f"year = {year}", script_text)
                script_text = re.sub(r"day = \d+",  f"day = {i}",     script_text)

                script_file.write(script_text)

        input_path = path.join(year, "inputs", f"day-{i}.txt")
        if not path.isfile(input_path):
            with open(input_path, 'w') as input_file:
                input_file.write("Copy input text from AdventOfCode here.")

    sample_data_path = path.join("sample_data", f"{year}_data.json")
    if not path.exists(sample_data_path):
        with open(sample_data_path, 'w') as sample_data_file:
            sample_data_file.write(json.dumps(sample_data, indent=2))


if __name__ == "__main__":
    prepare_year(argv[1])
