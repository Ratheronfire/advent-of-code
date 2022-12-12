from typing import List

from puzzle_base import PuzzleBase


class Puzzle(PuzzleBase):
    year = 2022
    day = 7

    fs = {}
    dir_sizes = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        self.build_fs(input_data)
        self.calc_dir_size(self.fs['/'], '/')

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(sum([self.dir_sizes[d] for d in self.dir_sizes if self.dir_sizes[d] <= 100000]))

    def get_day_2_answer(self, use_sample=False) -> str:
        free_space = 70000000 - self.dir_sizes['/']
        candidate_folders = [(d, self.dir_sizes[d]) for d in self.dir_sizes if free_space + self.dir_sizes[d] >= 30000000]
        candidate_folders = sorted(candidate_folders, key=lambda f: f[1])

        return str(candidate_folders[0][1])

    def build_fs(self, commands: List[str]):
        self.fs = {'/': {}}
        cwd_path = []
        cwd = self.get_cwd(cwd_path)

        i = 0
        while i < len(commands):
            line = commands[i].strip().split(' ')

            if len(line) == 1 and line[0] == '':
                break

            if line[1] == 'cd':
                if line[2] == '/':
                    cwd_path = ['/']
                elif line[2] == "..":
                    cwd_path.pop()
                else:
                    cwd_path.append(line[2])
                    if not line[2] in cwd:
                        cwd[line[2]] = {}

                cwd = self.get_cwd(cwd_path)
            elif line[1] == 'ls':
                for subline in commands[i+1:]:
                    file = subline.strip().split(' ')

                    if subline == '':
                        continue

                    if file[0] == '$':
                        break

                    if file[0] == 'dir':
                        cwd[file[1]] = {}
                    else:
                        cwd[file[1]] = int(file[0])

            i += 1

    def get_cwd(self, cwd_path):
        directory = self.fs
        for subdir in cwd_path:
            if subdir in directory:
                directory = directory[subdir]

        return directory

    def calc_dir_size(self, directory, path):
        total = 0

        for entry in directory:
            if isinstance(directory[entry], int):
                total += directory[entry]
            else:
                total += self.calc_dir_size(directory[entry], path + entry + '/')

        self.dir_sizes[path] = total
        return total


puzzle = Puzzle()
print(puzzle.test_and_run())
