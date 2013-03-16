import sys
import logging

import ply.lex

logger = logging.getLogger(__name__)

class Lexer(object):
    '''
    A Lexical analyzer for Python Typelanguage.
    '''
    
    def __init__(self, debug=False):
        self.debug = debug

    def tokenize(self, string):
        '''
        Maps a string to an iterator over tokens. In other words: [char] -> [token]
        '''
        
        new_lexer = ply.lex.lex(module=self, debug=self.debug, errorlog=logger)
        new_lexer.latest_newline = 0
        new_lexer.input(string)

        while True:
            t = new_lexer.token()
            if t is None: break
            t.col = t.lexpos - new_lexer.latest_newline
            yield t

    # ============== PLY Lexer specification ==================
    #
    # This probably should be private but:
    #   - the parser requires access to `tokens` (perhaps they should be defined in a third, shared dependency)
    #   - things like `literals` might be a legitimate part of the public interface.
    #
    # Anyhow, it is pythonic to give some rope to hang oneself with :-)

    literals = ['|', '(', ')', '{', '}', '[', ']', ':', '*', ',', ';']
    
    reserved_words = { 'object': 'OBJECT' }

    tokens = ['ID', 'TYVAR', 'ARROW', 'KWARG', 'ANY'] + reserved_words.values()

    t_ARROW = r'->'
    t_KWARG = r'\*\*'
    t_ANY = r'\?\?'
    t_ignore = ' \t'

    def t_ID(self, t):
        r'~?[a-zA-Z_][a-zA-Z0-9_]*'

        if t.value[0] == '~':
            t.type = 'TYVAR'
            t.value = t.value[1:]
        elif t.value in self.reserved_words:
            t.type = self.reserved_words[t.value]
        else:
            t.type = 'ID'

        return t

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.latest_newline = t.lexpos

    def t_error(self, t):
        raise Exception('Error on line %s, col %s: Unexpected character: %s ' % (t.lexer.lineno, t.lexpos - t.latest_newline, t.value[0]))

if __name__ == '__main__':
    logging.basicConfig()
    lexer = Lexer(debug=True)
    for token in lexer.tokenize(sys.stdin.read()):
        print '%-20s%s' % (token.value, token.type)
