import unittest

from helpers.grid import Grid


class MyTestCase(unittest.TestCase):
    def test_gridfromtext(self):
        grid = Grid.from_number_strings(['123', '456', '789'])

        assert grid.extents == (2, 2)

        assert grid[(0, 0)] == 1
        assert grid[(1, 1)] == 5
        assert grid[(2, 2)] == 9

    def test_gridfromdict(self):
        grid = Grid.from_dict({
            (0, 0): 1,
            (1, 0): 2,
            (0, 1): 3,
            (1, 1): 4,
        })

        assert grid.extents == (1, 1)

        assert grid[(0, 0)] == 1
        assert grid[(1, 0)] == 2
        assert grid[(0, 1)] == 3
        assert grid[(1, 1)] == 4

    def test_gridempty(self):
        grid = Grid.create_empty(10, 10, ' ')

        assert grid.extents == (9, 9)

        assert grid[(5, 5)] == ' '

    def test_modify(self):
        grid = Grid.from_number_strings(['123', '456', '789'])

        assert grid.extents == (2, 2)

        assert grid[(1, 1)] == 5

        grid[(1, 1)] = 'a'

        assert grid[(1, 1)] == 'a'

    def test_getslice(self):
        grid = Grid.from_number_strings(['123', '456', '789'])
        assert grid.extents == (2, 2)

        subgrid = grid[(0, 0):(1, 1)]
        assert subgrid.extents == (1, 1)
        assert str(subgrid) == '12\n45'

        subgrid = grid[(2, 2):(1, 1)]
        assert subgrid.extents == (1, 1)
        assert str(subgrid) == '98\n65'

    def test_setslice(self):
        grid = Grid.from_number_strings(['123', '456', '789'])
        assert grid.extents == (2, 2)
        assert str(grid) == '123\n456\n789'

        grid[(0, 0):(1, 1)] = [['a', 'b'], ['c', 'd']]
        assert str(grid) == 'ab3\ncd6\n789'

        grid[(0, 0):(1, 1)] = 0
        assert str(grid) == '003\n006\n789'


if __name__ == '__main__':
    unittest.main()
