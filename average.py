class AverageCalculator:

    def calculateAverage(self, numbers: list[int]) -> float:
        if not numbers:
            return 0
        return sum(numbers) / len(numbers)


import unittest

class Test_BankAccount(unittest.TestCase):

    def test(self):
        ac = AverageCalculator()
        self.assertAlmostEqual(ac.calculateAverage([1, 2, 3, 4, 5]), 3)

    # без этого теста проходит код, который наивно предполагает,
    # что результат вычислений - тоже `int`
    def test_frac(self):
        ac = AverageCalculator()
        self.assertAlmostEqual(ac.calculateAverage([1, 2, 3, 4]), 2.5)

    # без этого теста проходит код, который не учитывает
    # случай пустого списка
    def test_zero(self):
        ac = AverageCalculator()
        self.assertAlmostEqual(ac.calculateAverage([]), 0)


if __name__ == '__main__':
    unittest.main()
