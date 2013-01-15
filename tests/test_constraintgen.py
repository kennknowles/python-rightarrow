import unittest
import ast

from typelanguage import constraintgen 
from typelanguage.types import *

class TestConstraintGen(unittest.TestCase):

    def parse_expr(self, expr_string):
        return ast.parse(expr_string).body[0].value

    def parse_stmt(self, stmt_string):
        return ast.parse(stmt_string).body[0]

    def test_atomic_literals(self):
        assert constraintgen.constraints_expr(self.parse_expr('"hello"')).type == NamedType('str')
        assert constraintgen.constraints_expr(self.parse_expr('u"hello"')).type == NamedType('str')
        assert constraintgen.constraints_expr(self.parse_expr('3')).type == NamedType('int')
        assert constraintgen.constraints_expr(self.parse_expr('3L')).type == NamedType('long')
        assert constraintgen.constraints_expr(self.parse_expr('-2.5')).type == NamedType('float')
        assert constraintgen.constraints_expr(self.parse_expr('7.40J')).type == NamedType('complex')

    def test_list_literals(self):
        for expr in ['[]', '[3]', '["hello"]', '[[]]' ]:
            assert isinstance(constraintgen.constraints_expr(self.parse_expr(expr)).type, ListType)

    def test_statements(self):
        cenv = constraintgen.constraints_stmt(self.parse_stmt('x = 3'))
        assert len(cenv.constraints) == 1
        assert cenv.constraints[0].subtype == NamedType('int')
        assert isinstance(cenv.constraints[0].supertype, TypeVariable)
        assert cenv.return_type == None
        assert cenv.env['x'] == cenv.constraints[0].supertype
