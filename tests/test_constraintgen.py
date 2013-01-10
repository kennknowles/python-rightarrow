import unittest
import ast

from typelanguage import types, constraintgen 

class TestConstraintGen(unittest.TestCase):

    def parse_expr(self, expr_string):
        return ast.parse(expr_string).body[0].value

    def test_atomic_literals(self):
        assert constraintgen.constraints_expr(self.parse_expr('"hello"')).type == types.AtomicType('str')
        assert constraintgen.constraints_expr(self.parse_expr('u"hello"')).type == types.AtomicType('str')
        assert constraintgen.constraints_expr(self.parse_expr('3')).type == types.AtomicType('int')
        assert constraintgen.constraints_expr(self.parse_expr('3L')).type == types.AtomicType('long')
        assert constraintgen.constraints_expr(self.parse_expr('-2.5')).type == types.AtomicType('float')
        assert constraintgen.constraints_expr(self.parse_expr('7.40J')).type == types.AtomicType('complex')

    def test_list_literals(self):
        for expr in ['[]', '[3]', '["hello"]', '[[]]' ]:
            assert isinstance(constraintgen.constraints_expr(self.parse_expr(expr)).type, types.ListType)
