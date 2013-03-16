import unittest
import ast

from rightarrow.enforce import check
from rightarrow.annotations import *

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

            ('object(self)', Struct()),
            ('object(self)', 3),
            ('object(self)', [5]),
            ('object(self)', "hello"),

            ('object(self, foo:int)', Struct(foo=3)),
            ('object(self, foo:[int|str])', Struct(foo=["hello", 3])),
        ]

        for ty, val in cases:
            check(ty, val)

    def test_check_immediate_failing(self):
        cases = [
            ('int', "hello"),
            ('[int]', 5),
            ('[int]', ["hello"]),
            ('[str]', [[]]),
            ('[str]|int', [3]),
            ('object(self, foo:[int|complex])', Struct(foo=["hello", 3])),
        ]

        for ty, val in cases:
            try:
                check(ty, val)
            except TypeError:
                continue

    def test_single_arg_passing(self):
        cases = [
            ('int -> int', 3, lambda x: x),
            ('(str|float) -> int', "hello", lambda x: 3),
            ('(str|float) -> int', 2.5, lambda x: int(x)),
        ]

        for ty, arg, f in cases:
            check(ty, f)(arg)

    def test_single_arg_failing(self):
        cases = [
            ('int -> int', "hello", lambda x: x),
            ('[float] -> int', ["hello"], lambda x: x),
            ('(str|float) -> int', "hello", lambda x: x),
            ('(str|float) -> int', 2.5, lambda x: "boo"),
        ]

        for ty, arg, f in cases:
            try:
                check(ty, f)(arg)
            except TypeError:
                continue

