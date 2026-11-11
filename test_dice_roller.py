import unittest

from dice import parse, roll


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def randint(self, low, high):
        value = self.values.pop(0)
        assert low <= value <= high
        return value


class DiceTests(unittest.TestCase):
    def test_parse_defaults(self):
        self.assertEqual(parse("d6"), (1, 6, 0))
        self.assertEqual(parse("2D20+3"), (2, 20, 3))
        self.assertEqual(parse("1d8-1"), (1, 8, -1))

    def test_parse_rejects_invalid(self):
        for expression in ("d", "2x6", "0d6", "2d1", "101d6"):
            with self.assertRaises(ValueError):
                parse(expression)

    def test_roll_with_fixed_rng(self):
        result = roll("2d6+3", FixedRng([2, 5]))
        self.assertEqual(result["rolls"], [2, 5])
        self.assertEqual(result["total"], 10)

    def test_roll_respects_sides(self):
        result = roll("3d4", FixedRng([1, 4, 3]))
        self.assertEqual(result["total"], 8)


class RollManyTests(unittest.TestCase):
    def test_roll_many_statistics(self):
        from dice import roll_many

        result = roll_many("1d6", 3, FixedRng([2, 6, 4]))
        self.assertEqual(result["totals"], [2, 6, 4])
        self.assertEqual(result["minimum"], 2)
        self.assertEqual(result["maximum"], 6)
        self.assertEqual(result["average"], 4.0)

    def test_roll_many_validates_times(self):
        from dice import roll_many

        with self.assertRaises(ValueError):
            roll_many("1d6", 0)


if __name__ == "__main__":
    unittest.main()
