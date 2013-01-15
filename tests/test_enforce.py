import unittest
import ast

from typelanguage.enforce import check
from typelanguage.types import *

class TestEnforce(unittest.TestCase):

    def test_check_immediate_passing(self):
        cases = [
            ('int', 3),
            ('[int]', []),
            ('[str]', []),
            ('[int]', [1, 2, 3]),
            ('[str]', ["foo", "baz", "bar"]),
        ]

        for ty, val in cases:
            check(ty, val)

    def test_check_immediatee_failing(self):
        cases = [
            ('int', "hello"),
            ('[int]', 5),
            ('[int]', ["hello"]),
            ('[str]', [[]]),
        ]

        for ty, val in cases:
            try:
                check(ty, val)
            except TypeError:
                continue
