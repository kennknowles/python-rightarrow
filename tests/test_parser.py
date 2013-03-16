import unittest
import ast

from rightarrow.lexer import Lexer
from rightarrow.parser import Parser
from rightarrow.annotations import *

class TestParser(unittest.TestCase):

    def test_base_cases(self):
        parser = Parser(debug=True, lexer_class=lambda:Lexer(debug=False)) # Note that just manually passing token streams avoie this dep, but that sucks

        # Some of these types are not semantically valid, such as those with non-list varargs and non-dict kwargs, but I do not
        # reject these in the parsing phase

        test_cases = [
            ('int', int_t),
            ('long', long_t),
            ('float', float_t),
            ('complex', complex_t),
            ('str', str_t),
            ('unicode', unicode_t),
            ('??', any_t),

            ('[int]', List(elem_ty = int_t)),
            ('[str]', List(elem_ty = str_t)),

            ('{str:int}', Dict(key_ty=str_t, value_ty=int_t)),
            ('{str:[complex]}', Dict(key_ty=str_t, value_ty=List(complex_t))),

            ('int -> int', Function(arg_types=[int_t], return_type = int_t)),
            ('(int) -> int', Function(arg_types=[int_t], return_type = int_t)),
            ('(int, int) -> int', Function(arg_types=[int_t, int_t], return_type = int_t)),
            ('(int, *int) -> int', Function(arg_types=[int_t], vararg_type=int_t, return_type = int_t)),
            ('(int, **int) -> int', Function(arg_types=[int_t], kwarg_type=int_t, return_type = int_t)),
            ('(int, *int, **int) -> int', Function(arg_types=[int_t], vararg_type=int_t, kwarg_type=int_t, return_type = int_t)),

            ('int|str', Union([int_t, str_t])),
            ('int|str|unicode', Union([Union([int_t, str_t]), unicode_t])),

            ('~a', Variable('a')),
            ('~foo', Variable('foo')),

            ('~a -> ~a', Function([Variable('a')], Variable('a'))),

            ('object(self)', Object('self')),
            ('object(self, foo:int)', Object('self', foo=NamedType('int')))
        ]

        for string, parsed in test_cases:
            print string, '=?=', parsed # pytest captures this and we see it only on a failure, for debugging
            assert parser.parse(string) == parsed
