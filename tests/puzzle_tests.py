import unittest
from year_2023.day_12 import GearRow, get_fill_ranges


class PuzzleTests(unittest.TestCase):
    def test_2023_12_min_max_ranges(self):
        tests_and_results = [
            [
                '??###?????????? 1,3,2,1',
                '#.###.##.#.....',
                '#.###......##.#',
                [[0, 0], [2, 2], [6, 11], [9, 14]]
            ],
            [
                '?###?####??????? 3,4,1,1',
                '.###.####.#.#...',
                '.###.####....#.#',
                [[1, 1], [5, 5], [10, 13], [12, 15]]
            ],
            [
                '?####?###??????? 4,3,1,1',
                '.####.###.#.#...',
                '.####.###....#.#',
                [[1, 1], [6, 6], [10, 13], [12, 15]]
            ],
            [
                '?###???????##??? 3,1,3',
                '.###.#....###...',
                '.###.....#.###..',
                [[1, 1], [5, 9], [10, 11]]
            ],
            [
                '??##??????###??? 3,1,3',
                '.###.#....###...',
                '..###...#.###...',
                [[1, 2], [5, 8], [10, 10]]
            ],
            [
                '?###??????????###??????????###??????????###??????????###???????? 3,2,1,3,2,1,3,2,1,3,2,1,3,2,1',
                '.###.##.#.....###.##.#.....###.##.#.....###.##.#.....###.##.#...',
                '.###.....##.#.###.....##.#.###.....##.#.###.....##.#.###....##.#',
                [[1, 1], [5, 9], [8, 12], [14, 14], [18, 22], [21, 25], [27, 27], [31, 35],
                 [34, 38], [40, 40], [44, 48], [47, 51], [53, 53], [57, 60], [60, 63]]
            ],
        ]

        for test in tests_and_results:
            gears, broken_runs = test[0].split()
            gear_row = GearRow(
                [g for g in gears],
                [int(r) for r in broken_runs.split(',')]
            )

            fill_ranges, min_gears, max_gears = get_fill_ranges(gear_row)

            print(f'Row: {test[0]}\nMin: {"".join(min_gears)}\nMax: {"".join(max_gears)}\nRanges: {fill_ranges}\n')

            self.assertEqual(test[1], ''.join(min_gears).replace('?', '.'))
            self.assertEqual(test[2], ''.join(max_gears).replace('?', '.'))
            self.assertEqual(test[3], fill_ranges)


if __name__ == '__main__':
    unittest.main()
