class BankAccount:
    __balance: float

    def __init__(self, balance: float) -> None:
       self.__balance = balance

    def deposit(self, amount: float) -> None:
        self.__balance += amount
    
    def withdraw(self, amount: float) -> None:
        self.__balance -= amount

    def getBalance(self) -> float:
        return self.__balance


import unittest

class Test_BankAccount(unittest.TestCase):

    def assertEqualMoney(self, first: float, second: float):
        self.assertAlmostEqual(first, second, delta=1e-5)

    def test(self):
        account = BankAccount(1000)
        self.assertEqualMoney(account.getBalance(), 1000)
        account.deposit(500)
        self.assertEqualMoney(account.getBalance(), 1500)
        account.withdraw(300)
        self.assertEqualMoney(account.getBalance(), 1200)

    def test_negative(self):
        account = BankAccount(-1000)
        self.assertEqualMoney(account.getBalance(), -1000)
        account.deposit(-500)
        self.assertEqualMoney(account.getBalance(), -1500)
        account.withdraw(-300)
        self.assertEqualMoney(account.getBalance(), -1200)

    def test_debt(self):
        account = BankAccount(1000)
        account.withdraw(1500)
        self.assertEqualMoney(account.getBalance(), -500)
