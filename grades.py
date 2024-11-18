from status import *

class GradeCalculator(Status):

    def calculateAverage(self, numbers: list[int]) -> int:
        ...


import unittest

class Test_BankAccount(unittest.TestCase):

    def test(self):
        gc = GradeCalculator()
        self.assertAlmostEqual(gc.calculateAverage([4, 5, 3, 2, 4, 5, 5]), 4)
        self.assertEqual(gc.get_status("calculateAverage"), "OK")

    def test_approx(self):
        gc = GradeCalculator()
        self.assertAlmostEqual(gc.calculateAverage([4, 5, 5]), 5)
        self.assertEqual(gc.get_status("calculateAverage"), "OK")
        self.assertAlmostEqual(gc.calculateAverage([4, 4, 5]), 4)
        self.assertEqual(gc.get_status("calculateAverage"), "OK")

    def test_middle(self):
        gc = GradeCalculator()
        self.assertAlmostEqual(gc.calculateAverage([4, 5]), 5)
        self.assertAlmostEqual(gc.calculateAverage([3, 4]), 4)
        self.assertEqual(gc.get_status("calculateAverage"), "OK")

    def test_empty(self):
        gc = GradeCalculator()
        self.assertAlmostEqual(gc.calculateAverage([]), 0)
        self.assertEqual(gc.get_status("calculateAverage"), "EMPTY")

    def test_invalid(self):
        gc = GradeCalculator()
        self.assertAlmostEqual(gc.calculateAverage([2, 1, 3]), 0)
        self.assertEqual(gc.get_status("calculateAverage"), "INVALID")
        self.assertAlmostEqual(gc.calculateAverage([2, 6, 3]), 0)
        self.assertEqual(gc.get_status("calculateAverage"), "INVALID")



if __name__ == '__main__':
    unittest.main()
