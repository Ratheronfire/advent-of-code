import json
import os
import time
from abc import abstractmethod
from typing import List

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def format_input(input_str: str, should_strip_data=True):
    return [line.strip() if should_strip_data else line for line in input_str.split('\n')]


class SampleData:
    day: int

    input_data: List[str]
    input_data_2: List[str]

    answer_1: str
    answer_2: str

    def __init__(self, day: int, input_str: str, input_str_2: str, answer_1: str, answer_2: str, should_strip_data=True):
        self.day = day

        self.input_data = format_input(input_str, should_strip_data)
        self.input_data_2 = format_input(input_str_2, should_strip_data)
        self.answer_1 = answer_1
        self.answer_2 = answer_2


class PuzzleBase(object):
    year: int
    day: int

    should_strip_data = True

    input_data: List[str]
    sample_data: SampleData

    def __init__(self):
        input_path = os.path.join(ROOT_DIR, str(self.year), 'inputs', 'day-%d.txt' % self.day)
        with open(input_path, 'r') as input_file:
            self.input_data = format_input(input_file.read(), self.should_strip_data)

        sample_path = os.path.join(ROOT_DIR, 'sample_data', '%d_data.json' % self.year)
        with open(sample_path, 'r') as sample_file:
            sample_json = json.loads(sample_file.read())

            day_data = sample_json[self.day - 1]
            self.sample_data = SampleData(
                day_data['day'],
                day_data['input_data'],
                day_data['input_data_2'] if 'input_data_2' in day_data else day_data['input_data'],
                day_data['answer_1'],
                day_data['answer_2'],
                self.should_strip_data
            )

    def format_run_time(self, start_time: time, end_time: time):
        delta = end_time - start_time

        if delta < 1:
            return f'{delta * 1000} milliseconds'
        elif delta < 60:
            return f'{delta} sec'
        elif delta < 3600:
            return f'{delta / 60} min'
        else:
            return f'{delta / 3600} hours'

    def test_answers(self, both_parts=True, silent=False) -> (bool, str, str):
        answer_1 = ''
        answer_2 = ''

        part_1_correct = True
        part_2_correct = True

        time_before = time.time()

        self.reset()
        self.prepare_data(self.sample_data.input_data, 1)
        answer_1 = self.get_day_1_answer(True)
        part_1_correct = answer_1 == self.sample_data.answer_1

        time_after = time.time()
        part_1_timespan = time_after - time_before

        if not silent:
            print(f'Part 1 test ran in {self.format_run_time(time_before, time_after)}.')

        if both_parts:
            time_before = time.time()

            self.reset()
            self.prepare_data(self.sample_data.input_data_2, 2)
            answer_2 = self.get_day_2_answer(True)
            part_2_correct = answer_2 == self.sample_data.answer_2

            time_after = time.time()
            part_2_timespan = time_after - time_before

            if not silent:
                print(f'Part 2 test ran in {self.format_run_time(time_before, time_after)}.')
        else:
            part_2_timespan = -1

        return part_1_correct and part_2_correct, answer_1, answer_2, part_1_timespan, part_2_timespan

    def run(self, both_parts=True, silent=False) -> (str, str):
        answer_1 = ''
        answer_2 = ''

        time_before = time.time()

        self.reset()
        self.prepare_data(self.input_data, 1)
        answer_1 = self.get_day_1_answer(False)

        time_after = time.time()
        part_1_timespan = time_after - time_before

        if not silent:
            print(f'Part 1 ran in {self.format_run_time(time_before, time_after)}.')

        if both_parts:
            time_before = time.time()

            self.reset()
            self.prepare_data(self.input_data, 2)
            answer_2 = self.get_day_2_answer(False)

            time_after = time.time()
            part_2_timespan = time_after - time_before

            if not silent:
                print(f'Part 2 ran in {self.format_run_time(time_before, time_after)}.')
        else:
            part_2_timespan = -1

        return answer_1, answer_2, part_1_timespan, part_2_timespan

    def test_and_run(self, both_parts=True) -> str:
        test_results = self.test_answers(both_parts)
        if not test_results[0]:
            results = 'Test run%s failed.\n\n' \
                      '=== Part 1 ===\n' \
                      'Expected:\n' \
                      '%s\n\n' \
                      'Actual:\n' \
                      '%s' % ('s' if both_parts else '', self.sample_data.answer_1, test_results[1])

            if both_parts:
                results += '\n\n=== Part 2===\n' \
                           'Expected:\n' \
                           '%s\n\n' \
                           'Actual:\n' \
                           '%s' % (self.sample_data.answer_2, test_results[2])
        else:
            answers = self.run(both_parts)
            results = '=== Part 1===\n%s' % answers[0]

            if both_parts:
                results += '\n\n=== Part 2===\n%s' % answers[1]

        return results

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def prepare_data(self, input_data: List[str], current_part: int):
        pass

    @abstractmethod
    def get_day_1_answer(self, use_sample=False) -> str:
        pass

    @abstractmethod
    def get_day_2_answer(self, use_sample=False) -> str:
        pass
