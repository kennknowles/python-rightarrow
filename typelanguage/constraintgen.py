import ast
import sys
import copy
from collections import namedtuple

from typelanguage import types

class Constraint(object):
    def __init__(self, subtype, supertype):
        self.subtype = subtype
        self.supertype = supertype

    def __str__(self):
        return '%s <: %s' % (self.subtype, self.supertype)

    def substitute(self, substitution):
        return Constraint(subtype = self.subtype.substitute(substitution),
                          supertype = self.supertype.substitute(substitution))

class ConstrainedType(object):
    def __init__(self, type=None, constraints=None):
        self.type = type
        self.constraints = constraints or []

class ConstrainedEnv(object):
    def __init__(self, env=None, constraints=None, return_type=None):
        self.env = env or {}
        self.constraints = constraints or []
        self.return_type = return_type

    def substitute(self, substitution):
        return ConstrainedEnv(env = dict([(key, ty.substitute(substitution)) for key, ty in self.env.items()]),
                              constraints = [constraint.substitute(substitution) for constraint in self.constraints],
                              return_type = None if self.return_type is None else self.return_type.substitute(substitution))

    def pretty(self):
        return ("Env:\n\t%(bindings)s\n\nConstraints:\n\t%(constraints)s\n\nResult:\n\t%(result)s" % 
                dict(bindings    = '\n\t'.join(['%s: %s' % (var, ty) for var, ty in self.env.items()]),
                     constraints = '\n\t'.join([str(c) for c in self.constraints]),
                     result      = self.return_type))
    
def constraints(pyast, env=None):
    env = env or {}
    
    if isinstance(pyast, ast.Module) or isinstance(pyast, ast.Interactive):
        env = copy.copy(env)
        constraints = []
        for stmt in pyast.body:
            cs = constraints_stmt(stmt, env=env)
            env.update(cs.env)
            constraints += cs.constraints

        return ConstrainedEnv(env=env, constraints=constraints)

    elif isinstance(pyast, ast.Expression):
        expr_ty = constraints_expr(pyast.body, env=env)
        return ConstrainedEnv(env=env, constraints=expr_ty.constraints)

    else:
        raise Exception('Unknown ast node: %s' % pyast)

def extended_env(env, more_env):
    new_env = copy.copy(env)
    new_env.update(more_env)
    return new_env

# Note that this is rather different in Python 3 - and better!
def fn_env(arguments):
    new_env = {}

    for arg in arguments.args:
        if isinstance(arg, ast.Name) and isinstance(arg.ctx, ast.Param):
            new_env[arg.id] = types.fresh() # TODO: ??
        else:
            raise Exception('Arg is not a name in Param context!? %s' % arg) 

    if arguments.vararg:
        new_env[arguments.vararg] = types.fresh() # TODO: sub/superty of list

    if arguments.kwarg:
        new_env[arguments.kwarg] = types.fresh() # TODO: sub/superty of dict
    
    return new_env

def union(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return types.UnionType([right, left])

def constraints_stmt(stmt, env=None):
    env = env or {}
    
    if isinstance(stmt, ast.FunctionDef):
        arg_env = fn_env(stmt.args)

        body_env = extended_env(env, arg_env)
        constraints = []
        return_type = None # TODO: should be fresh and constrained?
        for body_stmt in stmt.body:
            cs = constraints_stmt(body_stmt, env=body_env)
            body_env.update(cs.env)
            constraints += cs.constraints
            return_type = union(return_type, cs.return_type)

        env[stmt.name] = types.FunctionType(arg_types=[arg_env[arg.id] for arg in stmt.args.args],
                                            return_type=return_type)

        return ConstrainedEnv(env=env, constraints=constraints)

    elif isinstance(stmt, ast.Expr):
        constrained_ty = constraints_expr(stmt.value, env=env)
        return ConstrainedEnv(env=env, constraints=constrained_ty.constraints)
        
    elif isinstance(stmt, ast.Return):
        if stmt.value:
            expr_result = constraints_expr(stmt.value, env=env)
            return ConstrainedEnv(env=env, constraints=expr_result.constraints, return_type=expr_result.type)
        else:
            result = types.fresh()
            return ConstrainedEnv(env=env, constraints=[Constraint(subtype=result, supertype=types.AtomicType('NoneType'))])

    else:
        raise NotImplementedError('Constraint gen for stmt %s' % stmt)
    
def constraints_expr(expr, env=None):
    env = env or {}
    
    if isinstance(expr, ast.Name) and isinstance(expr.ctx, ast.Load):
        if expr.id in ['False', 'True']: # Unlike other literals, these are actually just global identifiers
            return ConstrainedType(type=types.bool_t)
        elif expr.id in env:
            return ConstrainedType(type=env[expr.id])
        else:
            raise Exception('Variable not found in environment: %s' % expr.id)

    elif isinstance(expr, ast.Num):
        # The python ast module already chose the type of the num
        if isinstance(expr.n, int):
            return ConstrainedType(type=types.int_t)
        elif isinstance(expr.n, long):
            return ConstrainedType(type=types.long_t)
        elif isinstance(expr.n, float):
            return ConstrainedType(type=types.float_t)
        elif isinstance(expr.n, complex):
            return ConstrainedType(type=types.complex_t)

    elif isinstance(expr, ast.Str):
        return ConstrainedType(type=types.str_t)

    elif isinstance(expr, ast.List):
        return ConstrainedType(type=types.ListType(elem_ty=types.fresh()))
        
    elif isinstance(expr, ast.BinOp):
        left = constraints_expr(expr.left, env=env)
        right = constraints_expr(expr.right, env=env)
        ty = types.fresh()
        
        if isinstance(expr.op, ast.Mult):
            # TODO: consider whether all types should match (forces coercions to be explicit; a good thing)
            # Note: though strings and bools can be used in mult, forget it!
            op_constraints = [Constraint(subtype=left.type, supertype=types.numeric_t),
                              Constraint(subtype=right.type, supertype=types.numeric_t),
                              Constraint(subtype=ty, supertype=types.numeric_t)]
        else:
            raise NotImplementedError('BinOp') # TODO: just use function application constraint gen

        # TODO: return type should actually be fancier
        return ConstrainedType(type=ty, constraints=left.constraints+right.constraints+op_constraints)
    else:
        raise NotImplementedError('Constraint gen for %s' % expr)

if __name__ == '__main__':
    with open(sys.argv[1]) as fh:
        proggy = ast.parse(fh.read())

    print ast.dump(proggy)
        
    print constraints(proggy).pretty()
