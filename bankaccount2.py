from status import *

class BankAccount(Status):
    __balance: float

    @status("OK", "INVALID", name="init")
    def __init__(self, balance: float) -> None:
        super().__init__()
        if balance < 0:
            self._set_status("init", "INVALID")
            self.__balance = 0
            return
        self.__balance = balance
        self._set_status("init", "OK")

    @status("OK", "INVALID")
    def deposit(self, amount: float) -> None:
        if amount < 0:
            self._set_status("deposit", "INVALID")
            return
        self.__balance += amount
        self._set_status("deposit", "OK")

    @status("OK", "INVALID", "INSUFFICIENT")
    def withdraw(self, amount: float) -> None:
        if amount < 0:
            self._set_status("withdraw", "INVALID")
            return
        if amount > self.__balance:
            self._set_status("withdraw", "INSUFFICIENT")
            return
        self.__balance -= amount
        self._set_status("withdraw", "OK")

    def getBalance(self) -> float:
        return self.__balance


import unittest

class Test_BankAccount(unittest.TestCase):

    def assertEqualMoney(self, first: float, second: float):
        self.assertAlmostEqual(first, second, delta=1e-5)

    def test(self):
        account = BankAccount(1000)
        self.assertEqual(account.get_status("init"), "OK")
        self.assertEqualMoney(account.getBalance(), 1000)
        account.deposit(500)
        self.assertEqual(account.get_status("deposit"), "OK")
        self.assertEqualMoney(account.getBalance(), 1500)
        account.withdraw(300)
        self.assertEqual(account.get_status("withdraw"), "OK")
        self.assertEqualMoney(account.getBalance(), 1200)

    def test_negative_init(self):
        account = BankAccount(-1000)
        self.assertEqual(account.get_status("init"), "INVALID")
        self.assertEqualMoney(account.getBalance(), 0)

    def test_negative_deposit(self):
        account = BankAccount(1000)
        account.deposit(-500)
        self.assertEqual(account.get_status("deposit"), "INVALID")
        self.assertEqualMoney(account.getBalance(), 1000)

    def test_negative_withdraw(self):
        account = BankAccount(1000)
        account.withdraw(-500)
        self.assertEqual(account.get_status("withdraw"), "INVALID")
        self.assertEqualMoney(account.getBalance(), 1000)

    def test_debt(self):
        account = BankAccount(1000)
        account.withdraw(1500)
        self.assertEqual(account.get_status("withdraw"), "INSUFFICIENT")
        self.assertEqualMoney(account.getBalance(), 1000)
