import sys
import os.path
import logging

import ply.yacc

from typelanguage.types import *
from typelanguage.lexer import TypeLexer

logger = logging.getLogger(__name__)

class TypeParser(object):
    tokens = TypeLexer.tokens

    def __init__(self, debug=False, lexer_class=None):
        self.debug = debug
        self.lexer_class = lexer_class or TypeLexer # Crufty but works around statefulness in PLY

    def parse(self, string, lexer = None):
        lexer = lexer or self.lexer_class()
        return self.parse_token_stream(lexer.tokenize(string))

    def parse_token_stream(self, token_iterator, start_symbol='ty'):

        # Since PLY has some crufty aspects and dumps files, we try to keep them local
        # However, we need to derive the name of the output Python file :-/
        output_directory = os.path.dirname(__file__)
        try:
            module_name = os.path.splitext(os.path.split(__file__)[1])[0]
        except:
            module_name = __name__
        
        parsing_table_module = '_'.join([module_name, start_symbol, 'parsetab'])

        # And we regenerate the parse table every time; it doesn't actually take that long!
        new_parser = ply.yacc.yacc(module=self,
                                   debug=self.debug,
                                   tabmodule = parsing_table_module,
                                   outputdir = output_directory,
                                   write_tables=0,
                                   start = start_symbol,
                                   errorlog = logger)

        return new_parser.parse(lexer = IteratorToTokenStream(token_iterator))

    # ===================== PLY Parser specification =====================
    
    precedence = [
        ('right', 'ARROW'),
        ('left', '|'),
    ]

    def p_error(self, t):
        raise Exception('Parse error at %s:%s near token %s (%s)' % (t.lineno, t.col, t.value, t.type)) 

    def p_empty(self, p):
        'empty :'
        pass

    def p_ty_parens(self, p):
        "ty : '(' ty ')'"
        p[0] = p[2]

    def p_ty_var(self, p):
        "ty : TYVAR"
        p[0] = TypeVariable(p[1])

    def p_ty_union(self, p):
        "ty : ty '|' ty"
        p[0] = UnionType([p[1], p[3]])

    def p_ty_bare(self, p):
        "ty : bare_arg_ty"
        p[0] = p[1]

    def p_ty_funty_bare(self, p):
        "ty : ty ARROW ty"
        p[0] = FunctionType(arg_types=[p[1]], return_type=p[3])

    def p_ty_funty_complex(self, p):
        "ty : '(' maybe_arg_types ')' ARROW ty"
        argument_types=p[2]
        return_type=p[5]

        # Check here whether too many kwarg or vararg types are present
        # Each item in the list uses the dictionary encoding of tagged variants
        arg_types = [argty['arg_type'] for argty in argument_types if 'arg_type' in argty]
        vararg_types = [argty['vararg_type'] for argty in argument_types if 'vararg_type' in argty]
        kwarg_types = [argty['kwarg_type'] for argty in argument_types if 'kwarg_type' in argty]

        if len(vararg_types) > 1:
            raise Exception('Argument list with multiple vararg types: %s' % argument_types)

        if len(kwarg_types) > 1:
            raise Exception('Argument list with multiple kwarg types: %s' % argument_types)

        # All the arguments that are not special
        p[0] = FunctionType(arg_types=arg_types,
                            vararg_type=vararg_types[0] if len(vararg_types) > 0 else None,
                            kwarg_type=kwarg_types[0] if len(kwarg_types) > 0 else None,
                            kwonly_arg_types=None,
                            return_type=return_type)

    # Because a bare function type is equivalent to a single argument in parens, it is not
    # parsed by this rule
    def p_maybe_arg_types(self, p):
        '''
        maybe_arg_types : arg_types ',' arg_ty
                        | empty
        '''
        p[0] = [] if len(p) == 2 else p[1] + [p[3]]

    # Executive decision is this: kwargs and varargs get to be elements of this list ANYWHERE
    # and we check later, to avoid any parsing issues with commas
    def p_arg_types_single(self, p):
        '''
        arg_types : arg_types ',' arg_ty
                  | arg_ty
        '''
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

    def p_arg_ty_normal(self, p):
        "arg_ty : ty"
        p[0] = { 'arg_type' : p[1] }

    def p_arg_ty_vararg(self, p):
        "arg_ty : '*' ty"
        p[0] = { 'vararg_type' : p[2] }

    def p_arg_ty_kwarg(self, p):
        "arg_ty : KWARG ty"
        p[0] = { 'kwarg_type' : p[2] }

    # Special types that never require parenthesis
    def p_bare_arg_ty(self, p):
        """
        bare_arg_ty : identifier_ty
                    | dict_ty
                    | list_ty
                    | object_ty
                    | any_ty
        """
        p[0] = p[1]

    def p_identifier_ty(self, p):
        "identifier_ty : ID"
        p[0] = NamedType(p[1])

    def p_list_ty(self, p):
        "list_ty : '[' ty ']'"
        p[0] = ListType(elem_ty=p[2])

    def p_dict_ty(self, p):
        "dict_ty : '{' ty ':' ty '}'"
        p[0] = DictType(key_ty=p[2], value_ty=p[4])

    def p_any_ty(self, p):
        "any_ty : ANY"
        p[0] = AnyType()

    def p_object_ty(self, p):
        """
        object_ty : OBJECT '(' ')'
                  | OBJECT '(' obj_fields ')'
        """
        p[0] = ObjectType(**({} if len(p) == 4 else p[3]))

    def p_obj_fields(self, p):
        """
        obj_fields : obj_fields ',' obj_field
                   | obj_field
        """
        p[0] = dict([p[1]] if len(p) == 2 else p[1] + [p[3]]) # Note: no checking for dupe fields at the moment

    def p_obj_field(self, p):
        "obj_field : ID ':' ty"
        p[0] = (p[1], p[3])
        

class IteratorToTokenStream(object):
    def __init__(self, iterator):
        self.iterator = iterator

    def token(self):
        try:
            return self.iterator.next()
        except StopIteration:
            return None


if __name__ == '__main__':
    logging.basicConfig()
    parser = TypeParser(debug=True)
    print parser.parse(sys.stdin.read())
