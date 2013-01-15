import unittest
import ast

from typelanguage.lexer import TypeLexer
from typelanguage.parser import TypeParser
from typelanguage.types import *

class TestParser(unittest.TestCase):

    def test_base_cases(self):
        parser = TypeParser(debug=True, lexer_class=lambda:TypeLexer(debug=False)) # Note that just manually passing token streams avoie this dep, but that sucks

        # Some of these types are not semantically valid, such as those with non-list varargs and non-dict kwargs, but I do not
        # reject these in the parsing phase

        test_cases = [
            ('int', int_t),
            ('long', long_t),
            ('float', float_t),
            ('complex', complex_t),
            ('str', str_t),
            ('unicode', unicode_t),

            ('[int]', ListType(elem_ty = int_t)),
            ('[str]', ListType(elem_ty = str_t)),

            ('{str:int}', DictType(key_ty=str_t, value_ty=int_t)),
            ('{str:[complex]}', DictType(key_ty=str_t, value_ty=ListType(complex_t))),

            ('int -> int', FunctionType(arg_types=[int_t], return_type = int_t)),
            ('(int) -> int', FunctionType(arg_types=[int_t], return_type = int_t)),
            ('(int, int) -> int', FunctionType(arg_types=[int_t, int_t], return_type = int_t)),
            ('(int, *int) -> int', FunctionType(arg_types=[int_t], vararg_type=int_t, return_type = int_t)),
            ('(int, **int) -> int', FunctionType(arg_types=[int_t], kwarg_type=int_t, return_type = int_t)),
            ('(int, *int, **int) -> int', FunctionType(arg_types=[int_t], vararg_type=int_t, kwarg_type=int_t, return_type = int_t)),

            ('int|str', UnionType([int_t, str_t])),
            ('int|str|unicode', UnionType([UnionType([int_t, str_t]), unicode_t])),

            ('~a', TypeVariable('a')),
            ('~foo', TypeVariable('foo')),

            ('~a -> ~a', FunctionType([TypeVariable('a')], TypeVariable('a'))),

            ('object()', ObjectType()),
            ('object(foo:int)', ObjectType(foo=AtomicType('int')))
        ]

        for string, parsed in test_cases:
            print string, '=?=', parsed # pytest captures this and we see it only on a failure, for debugging
            assert parser.parse(string) == parsed
