from collections import namedtuple, defaultdict
    
class Type(object): pass
class AtomicType(Type, namedtuple('AtomicType', ['name'])): pass
class TypeVariable(Type, namedtuple('TypeVariable', ['name'])): pass

class FunctionType(Type):
    def __init__(self, arg_types, return_type, vararg_type=None, kwonly_arg_types=None, kwarg_type=None):
        self.arg_types = arg_types
        self.return_type = return_type
        self.vararg_type = vararg_type
        self.kwarg_type = kwarg_type
        self.kwonly_arg_types = kwonly_arg_types

    def __str__(self):
        comma_separated_bits = [unicode(v) for v in self.arg_types]
        
        if self.vararg_type:
            comma_separated_bits.append('*%s' % self.vararg_type)

        if self.kwonly_arg_types:
            comma_separated_bits += ['%s=%s' % (kwarg, ty) for (kwarg, ty) in self.kwonly_arg_types.items() ]

        if self.kwarg_type:
            comma_separated_bits.append('**%s' % self.kwarg_type)
        
        return '(%s) -> %s' % (', '.join(comma_separated_bits), self.return_type)

class TypeApplication(Type):
    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

class UnionType(Type):
    def __init__(self, types):
        self.types = types


used_vars = defaultdict(lambda: 0)
def fresh(prefix=None):
    global used_vars
    prefix = prefix or '?X'
    used_vars[prefix] = used_vars[prefix] + 1
    return prefix + str(used_vars[prefix])

