input_path = "inputs/day-7.txt"


def get_cwd(fs, cwd_path):
    dir = fs
    for subdir in cwd_path:
        if subdir in dir:
            dir = dir[subdir]

    return dir


def build_fs():
    fs = {'/': {}}
    cwd_path = []
    cwd = get_cwd(fs, cwd_path)

    i = 0
    while i < len(commands):
        line = commands[i].strip().split(' ')

        if line[1] == 'cd':
            if line[2] == '/':
                cwd_path = ['/']
            elif line[2] == "..":
                cwd_path.pop()
            else:
                cwd_path.append(line[2])
                if not line[2] in cwd:
                    cwd[line[2]] = {}

            cwd = get_cwd(fs, cwd_path)
        elif line[1] == 'ls':
            for subline in commands[i+1:]:
                file = subline.strip().split(' ')

                if file[0] == '$':
                    break

                if file[0] == 'dir':
                    cwd[file[1]] = {}
                else:
                    cwd[file[1]] = int(file[0])

        i += 1

    return fs


dir_sizes = {}


def get_dir_size(dir, path):
    total = 0

    for entry in dir:
        if isinstance(dir[entry], int):
            total += dir[entry]
        else:
            total += get_dir_size(dir[entry], path + entry + '/')

    dir_sizes[path] = total
    return total


with open(input_path, 'r') as input_file:
    commands = input_file.readlines()

fs = build_fs()

get_dir_size(fs['/'], '/')

# part 1
print(sum([dir_sizes[d] for d in dir_sizes if dir_sizes[d] <= 100000]))

# part 2
free_space = 70000000 - dir_sizes['/']
candidate_folders = [(d, dir_sizes[d]) for d in dir_sizes if free_space + dir_sizes[d] >= 30000000]
candidate_folders = sorted(candidate_folders, key=lambda f: f[1])

print(candidate_folders[0][1])
