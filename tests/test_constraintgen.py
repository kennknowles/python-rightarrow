import unittest
import ast

from typelanguage import types, constraintgen 

class TestConstraintGen(unittest.TestCase):

    def parse_expr(self, expr_string):
        return ast.parse(expr_string).body[0].value

    def test_literals(self):
        assert constraintgen.constraints_expr(self.parse_expr('"hello"')).type == types.AtomicType('str')
