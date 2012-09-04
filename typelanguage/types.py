from collections import namedtuple, defaultdict
    
class Type(object): pass
class AtomicType(Type, namedtuple('AtomicType', ['name'])): pass
class TypeVariable(Type, namedtuple('TypeVariable', ['name'])): pass

class FunctionType(Type):
    def __init__(self, anon_types, return_type, args_type=None, kwargs_type=None):
        self.anon_types = anon_types
        self.return_type = return_type
        self.args_type = args_type
        self.kwargs_type = kwargs_type

    def __str__(self):
        return ('(%(anon_types)s) -> %(return_type)s' %
                dict(anon_types=self.anon_types,
                     return_type=self.return_type))

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

