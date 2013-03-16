import unittest
import logging

from ply.lex import LexToken

from rightarrow.lexer import Lexer
from rightarrow.annotations import *

class TestLexer(unittest.TestCase):

    def token(self, value, ty=None):
        t = LexToken()
        t.type = ty if ty != None else value
        t.value = value
        t.lineno = -1
        t.lexpos = -1
        return t
    
    def assert_lex_equiv(self, s, stream2):
        # NOTE: lexer fails to reset after call?
        l = Lexer(debug=True)
        stream1 = list(l.tokenize(s)) # Save the stream for debug output when a test fails
        stream2 = list(stream2)
        assert len(stream1) == len(stream2)
        for token1, token2 in zip(stream1, stream2):
            print token1, token2
            assert token1.type  == token2.type
            assert token1.value == token2.value

    @classmethod
    def setup_class(cls):
        logging.basicConfig()

    def test_simple_inputs(self):
        self.assert_lex_equiv('int', [self.token('int', 'ID')])
        self.assert_lex_equiv('[int]', [self.token('['), self.token('int', 'ID'), self.token(']')])
        self.assert_lex_equiv('int -> int', [self.token('int', 'ID'), self.token('->', 'ARROW'), self.token('int', 'ID')])
        self.assert_lex_equiv('*a', [self.token('*'), self.token('a', 'ID')])
        self.assert_lex_equiv('**a', [self.token('**', 'KWARG'), self.token('a', 'ID')])
        self.assert_lex_equiv('*x, **a', [self.token('*'), self.token('x', 'ID'), self.token(','), self.token('**', 'KWARG'), self.token('a', 'ID')])
