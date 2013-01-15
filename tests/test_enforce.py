import unittest
import ast

from typelanguage.enforce import check
from typelanguage.types import *

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class TestEnforce(unittest.TestCase):

    def test_check_immediate_passing(self):
        cases = [
            ('int', 3),
            ('[int]', []),
            ('[str]', []),
            ('[int]', [1, 2, 3]),
            ('[str]', ["foo", "baz", "bar"]),

            ('str|int', 3),
            ('str|int', "hello"),
            ('[str]|int', ["hello"]),

            ('object()', Struct()),
            ('object()', 3),
            ('object()', [5]),
            ('object()', "hello"),

            ('object(foo:int)', Struct(foo=3)),
            ('object(foo:[int|str])', Struct(foo=["hello", 3])),
        ]

        for ty, val in cases:
            check(ty, val)

    def test_check_immediatee_failing(self):
        cases = [
            ('int', "hello"),
            ('[int]', 5),
            ('[int]', ["hello"]),
            ('[str]', [[]]),
            ('[str]|int', [3]),
            ('object(foo:[int|complex])', Struct(foo=["hello", 3])),
        ]

        for ty, val in cases:
            try:
                check(ty, val)
            except TypeError:
                continue
