import importlib.util
import sys
from argparse import ArgumentParser


class Tester(object):
    year: int
    day: int
    part: int

    test_input: str

    def __init__(self):
        parser = ArgumentParser(
            description="Manual Tester",
            usage="year day part:(1|2) test_input"
        )

        parser.add_argument('year')
        parser.add_argument('day')
        parser.add_argument('part')
        parser.add_argument('test_input')

        self.args = parser.parse_args(sys.argv[1:])

    def run(self):
        spec = importlib.util.spec_from_file_location("Puzzle", f"{self.args.year}/day-{self.args.day}.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules["Puzzle"] = module
        spec.loader.exec_module(module)

        puzzle = module.Puzzle()
        puzzle.input_data = self.args.test_input.split('\\n')

        puzzle.reset()
        puzzle.prepare_data(puzzle.input_data, self.args.part)

        if self.args.part == "1":
            print(puzzle.get_part_1_answer())
        else:
            print(puzzle.get_part_2_answer())


if __name__ == "__main__":
    main = Tester()
    main.run()
