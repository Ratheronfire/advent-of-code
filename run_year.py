import importlib.util
import sys
import time
from argparse import ArgumentParser

from func_timeout import func_timeout, FunctionTimedOut


class Tester(object):
    year: int

    def __init__(self):
        parser = ArgumentParser(
            description="Year Runner",
            usage="year"
        )

        parser.add_argument('year')

        self.args = parser.parse_args(sys.argv[1:])

    def format_run_time(self, delta):
        if delta < 1:
            return f'{delta * 1000:.6f} ms'
        elif delta < 60:
            return f'{delta:.2f} sec'
        elif delta < 3600:
            return f'{delta / 60:.2f} min'
        else:
            return f'{delta / 3600:.2f} hours'

    def run(self):
        start_time = time.time()

        grid_width = 20
        print(f'{"":<{grid_width}} | {"Part 1":<{grid_width}} | {"Part 2":<{grid_width}}')

        for day in range(1, 26):
            spec = importlib.util.spec_from_file_location("Puzzle", f"year_{self.args.year}/day-{day}.py")
            module = importlib.util.module_from_spec(spec)
            sys.modules["Puzzle"] = module
            spec.loader.exec_module(module)

            puzzle = module.Puzzle()

            try:
                print('=' * ((grid_width * 3) + 6))

                answer_1, answer_2, part_1_timespan, part_2_timespan = func_timeout(10, puzzle.run, args=(True, True))

                print(f'{"Day " + str(day) + " Result":<{grid_width}} | {answer_1:<{grid_width}} | {answer_2:<{grid_width}}')
                print(f'{"Day " + str(day) + " Time":<{grid_width}} | { self.format_run_time(part_1_timespan):<{grid_width}} | {self.format_run_time(part_2_timespan):<{grid_width}}')
            except FunctionTimedOut:
                print(f'{"Day " + str(day) + " Result":<{grid_width}} | {"Timed Out":<{grid_width}} | {"Timed Out":<{grid_width}}')
                print(f'{"Day " + str(day) + " Time":<{grid_width}} | {"N/A":<{grid_width}} | {"N/A":<{grid_width}}')

            except AttributeError:
                print(f'{"Day " + str(day) + " Result":<{grid_width}} | {"N/A":<{grid_width}} | {"N/A":<{grid_width}}')
                print(f'{"Day " + str(day) + " Time":<{grid_width}} | {"N/A":<{grid_width}} | {"N/A":<{grid_width}}')

        print(f'Total runtime: {self.format_run_time(time.time() - start_time)}')


if __name__ == "__main__":
    main = Tester()
    main.run()
