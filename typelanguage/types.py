from collections import namedtuple, defaultdict

# Kinds

class Kind(object): pass

# The kind of types
class Type(Kind): pass

# The kind of record field names
class Label(Kind): pass

class FunctionKind(Kind):
    def __init__(self, dom, rng):
        self.dom = dom
        self.rng = rng

        
## Types proper

class Type(object): pass

class AtomicType(Type):
    def __init__(self, name):
        self.name = name

    def substitute(self, substitution):
        return self

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, AtomicType) and other.name == self.name


# TODO: Make into a higher-kinded type? Maybe that's just a headache?
class ListType(Type):
    def __init__(self, elem_ty):
        self.elem_ty = elem_ty

    def substitute(self, substitution):
        return ListType(self.elem_ty.substitue(substitution))

    def __str__(self):
        return '[%s]' % self.elem_ty

    def __eq__(self):
        return isinstance(other, ListType) and other.elem_ty == self.elem_ty
        
class TypeVariable(Type):
    def __init__(self, name):
        self.name = name

    def substitute(self, substitution):
        if self.name in substitution:
            return substitution[self.name]
        else:
            return self

    def __str__(self):
        return '?%s' % self.name

class FunctionType(Type):
    def __init__(self, arg_types, return_type, vararg_type=None, kwonly_arg_types=None, kwarg_type=None):
        self.arg_types = arg_types
        self.return_type = return_type
        self.vararg_type = vararg_type
        self.kwarg_type = kwarg_type
        self.kwonly_arg_types = kwonly_arg_types

    def substitute(self, substitution):
        return FunctionType(arg_types = [ty.substitute(substitution) for ty in self.arg_types],
                            return_type = self.return_type.substitute(substitution),
                            vararg_type = None if self.vararg_type is None else self.vararg_type.substitute(substitution),
                            kwonly_arg_types = None if self.kwonly_arg_types is None else [ty.substitute(substitution) for ty in self.kwonly_arg_types],
                            kwarg_type = None if self.kwarg_type is None else self.kwarg_type.substitute(substitution))

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

    def substitute(self, substitution):
        return TypeApplication(self.fn.substitute(substitution), [ty.substitute(substitution) for ty in self.args])

class UnionType(Type):
    def __init__(self, types):
        self.types = types

    def __str__(self):
        return '|'.join([str(ty) for ty in self.types])

# Fresh variable supply

used_vars = defaultdict(lambda: 0)
def fresh(prefix=None):
    global used_vars
    prefix = prefix or 'X'
    used_vars[prefix] = used_vars[prefix] + 1
    return TypeVariable(prefix + str(used_vars[prefix]))

# Shortcuts for common types

bool_t = AtomicType('bool')
int_t = AtomicType('int')
long_t = AtomicType('long')
float_t = AtomicType('float')
complex_t = AtomicType('complex')

str_t = AtomicType('str')
unicode_t = AtomicType('unicode')

numeric_t = UnionType([int_t, long_t, complex_t, float_t])

