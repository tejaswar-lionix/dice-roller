import unittest

from dice import parse, parse_keep, roll


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


class KeepDropTests(unittest.TestCase):
    def test_parse_keep(self):
        self.assertEqual(parse_keep("4d6kh3"), (4, 6, 0, "kh", 3))
        self.assertEqual(parse_keep("4d6kl1+2"), (4, 6, 2, "kl", 1))

    def test_parse_keep_returns_none_for_normal_expressions(self):
        self.assertIsNone(parse_keep("2d6+3"))

    def test_parse_keep_rejects_out_of_range(self):
        for expression in ("4d6kh0", "4d6kh5", "4d6kl0", "101d6kh1"):
            with self.assertRaises(ValueError):
                parse_keep(expression)

    def test_roll_keeps_highest_dice(self):
        result = roll("4d6kh3", FixedRng([2, 6, 3, 5]))
        self.assertEqual(result["rolls"], [2, 6, 3, 5])
        self.assertEqual(result["kept"], [6, 5, 3])
        self.assertEqual(result["total"], 14)

    def test_roll_keeps_lowest_die(self):
        result = roll("4d6kl1+2", FixedRng([2, 6, 3, 5]))
        self.assertEqual(result["kept"], [2])
        self.assertEqual(result["total"], 4)

    def test_normal_roll_has_no_kept_key(self):
        result = roll("2d6+3", FixedRng([2, 5]))
        self.assertNotIn("kept", result)


class AdvantageTests(unittest.TestCase):
    def test_roll_advantage_keeps_highest(self):
        from dice import roll_advantage

        result = roll_advantage(20, FixedRng([5, 17]))
        self.assertEqual(result["rolls"], [5, 17])
        self.assertEqual(result["kept"], 17)
        self.assertEqual(result["total"], 17)

    def test_roll_disadvantage_keeps_lowest(self):
        from dice import roll_disadvantage

        result = roll_disadvantage(20, FixedRng([5, 17]))
        self.assertEqual(result["rolls"], [5, 17])
        self.assertEqual(result["kept"], 5)
        self.assertEqual(result["total"], 5)

    def test_advantage_validates_sides(self):
        from dice import roll_advantage, roll_disadvantage

        for sides in (1, 1001):
            with self.assertRaises(ValueError):
                roll_advantage(sides)
            with self.assertRaises(ValueError):
                roll_disadvantage(sides)


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
