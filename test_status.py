import unittest

from status import *

class A(Status):

    @status("OK", "ERROR")
    def normal(self, ok: bool):
        self._set_status("normal", "OK" if ok else "ERROR")

    @status("OK", "ERROR", name="other")
    def alter(self, ok: bool):
        self._set_status("other", "OK" if ok else "ERROR")


class B(A):
    
    @status()
    def normal(self, ok: bool):
        self._set_status("normal", "OK" if ok else "ERROR")

    @status(name="other")
    def alter(self, ok: bool):
        self._set_status("other", "OK" if ok else "ERROR")


class Test(unittest.TestCase):

    def test_self(self):
        a = A()
        self.assertEqual(a.get_status("normal"), "NIL")
        self.assertEqual(a.get_status("other"), "NIL")
        a.normal(True)
        self.assertEqual(a.get_status("normal"), "OK")
        self.assertEqual(a.get_status("other"), "NIL")
        a.normal(False)
        self.assertEqual(a.get_status("normal"), "ERROR")
        self.assertEqual(a.get_status("other"), "NIL")
        a.alter(True)
        self.assertEqual(a.get_status("normal"), "ERROR")
        self.assertEqual(a.get_status("other"), "OK")
        a.alter(False)
        self.assertEqual(a.get_status("normal"), "ERROR")
        self.assertEqual(a.get_status("other"), "ERROR")

    
    def test_inherited(self):
        b = B()
        self.assertEqual(b.get_status("normal"), "NIL")
        self.assertEqual(b.get_status("other"), "NIL")
        b.normal(True)
        self.assertEqual(b.get_status("normal"), "OK")
        self.assertEqual(b.get_status("other"), "NIL")
        b.normal(False)
        self.assertEqual(b.get_status("normal"), "ERROR")
        self.assertEqual(b.get_status("other"), "NIL")
        b.alter(True)
        self.assertEqual(b.get_status("normal"), "ERROR")
        self.assertEqual(b.get_status("other"), "OK")
        b.alter(False)
        self.assertEqual(b.get_status("normal"), "ERROR")
        self.assertEqual(b.get_status("other"), "ERROR")
