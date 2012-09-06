import ast
import sys
import copy
from collections import namedtuple

from typelanguage import types

class Constraint(object):
    def __init__(self, subtype, supertype):
        self.subtype = subtype
        self.supertype = supertype

class ConstrainedType(object):
    def __init__(self, type=None, constraints=None):
        self.type = type
        self.constraints = constraints or []

class ConstrainedEnv(object):
    def __init__(self, env=None, constraints=None, return_type=None):
        self.env = env or {}
        self.constraints = constraints or []
        self.return_type = return_type

    def pretty(self):
        return ("Env:\n\t%(bindings)s\n\nConstraints:\n\t%(constraints)s\n\nResult:\n\t%(result)s" % 
                dict(bindings    = '\n\t'.join(['%s: %s' % (var, ty) for var, ty in self.env.items()]),
                     constraints = '\n\t'.join(['%s <: %s' % (c.subtype, c.supertype) for c in self.constraints]),
                     result      = self.return_type))
    
def constraints(env, pyast):
    if isinstance(pyast, ast.Module) or isinstance(pyast, ast.Interactive):
        env = copy.copy(env)
        constraints = []
        for stmt in pyast.body:
            cs = constraints_stmt(env, stmt)
            env.update(cs.env)
            constraints += cs.constraints

        return ConstrainedEnv(env=env, constraints=constraints)

    elif isinstance(pyast, ast.Expression):
        expr_ty = constraints_expr(pyast.body)
        return Constrained_env(env=env, constraints=expr_ty.constraints)

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
        return types.UnionType(right, left)

def constraints_stmt(env, stmt):
    if isinstance(stmt, ast.FunctionDef):
        arg_env = fn_env(stmt.args)

        body_env = extended_env(env, arg_env)
        constraints = []
        return_type = None # TODO: should be fresh and constrained?
        for body_stmt in stmt.body:
            cs = constraints_stmt(body_env, body_stmt)
            body_env.update(cs.env)
            constraints += cs.constraints
            return_type = union(return_type, cs.return_type)

        env[stmt.name] = types.FunctionType(arg_types=[arg_env[arg.id] for arg in stmt.args.args],
                                            return_type=return_type)

        return ConstrainedEnv(env=env, constraints=constraints)
        
    elif isinstance(stmt, ast.Return):
        if stmt.value:
            expr_result = constraints_expr(env, stmt.value)
            return ConstrainedEnv(env=env, constraints=expr_result.constraints, return_type=expr_result.type)
        else:
            result = types.fresh()
            return ConstrainedEnv(env=env, constraints=[Constraint(subtype=result, supertype=types.AtomicType('NoneType'))])

    else:
        raise NotImplementedError('Constraint gen for stmt %s' % stmt)
    
def constraints_expr(env, expr):
    if isinstance(expr, ast.Name) and isinstance(expr.ctx, ast.Load):
        if expr.id in env:
            return ConstrainedType(type=env[expr.id])
        else:
            raise Exception('Variable not found in environment: %s' % expr.id)

    elif isinstance(expr, ast.Num):
        return ConstrainedType(type=types.AtomicType('int'))
        
    elif isinstance(expr, ast.BinOp):
        left = constraints_expr(env, expr.left)
        right = constraints_expr(env, expr.right)
        ty = types.fresh()
        
        if isinstance(expr.op, ast.Mult):
            # Really, it is whatever the left-hand type returns from __mult__!
            op_constraints = [Constraint(subtype=left.type, supertype=types.AtomicType('num')),
                              Constraint(subtype=right.type, supertype=types.AtomicType('num')),
                              Constraint(subtype=ty, supertype=types.AtomicType('num'))]
        else:
            raise NotImplementedError('BinOp') # TODO: just use function application constraint gen

        # TODO: return type should actually be fancier
        return ConstrainedType(type=ty, constraints=left.constraints+right.constraints+op_constraints)
    else:
        raise NotImplementedError('Constraint gen for %s' % expr)

if __name__ == '__main__':
    with open(sys.argv[1]) as fh:
        proggy = ast.parse(fh.read())
        
    print constraints({}, proggy).pretty()
