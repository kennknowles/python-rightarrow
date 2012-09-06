import sys
import ast
import logging
import copy

from typelanguage import constraintgen
from typelanguage.types import *

logger = logging.getLogger(__name__)

class Refutation(object):
    def __init__(self, reason):
        self.reason = reason

    def __bool__(self):
        return False

    def __str__(self):
        return 'Refutation(reason="%s")' % self.reason

def reconcile(constraint):
    '''
    Returns an assignment of type variable names to
    types that makes this constraint satisfiable, or a Refutation
    '''
    
    if isinstance(constraint.subtype, AtomicType):
        if isinstance(constraint.supertype, AtomicType):
            if constraint.subtype.name == constraint.supertype.name:
                return {}
            else:
                return Refutation('Cannot reconcile different atomic types: %s' % constraint)
        elif isinstance(constraint.supertype, TypeVariable):
            return {constraint.supertype.name: contraint.subtype}
        else:
            return Refutation('Cannot reconcile atomic type with non-atomic type: %s' % constraint)

    elif isinstance(constraint.supertype, AtomicType):
        if isinstance(constraint.subtype, AtomicType):
            if constraint.subtype.name == constraint.supertype.name:
                return {}
            else:
                return Refutation('Cannot reconcile different atomic types: %s' % constraint)
        elif isinstance(constraint.subtype, TypeVariable):
            return {constraint.subtype.name: constraint.supertype}
        else:
            return Refutation('Cannot reconcile non-atomic type with atomic type: %s' % constraint)
    else:
        raise NotImplementedError('Reconciliation of %s' % constraint)

def solve(constraints):
    remaining_constraints = copy.copy(constraints)
    substitution = {}
    
    while len(remaining_constraints) > 0:
        constraint = remaining_constraints.pop()
        additional_substitution = reconcile(constraint)

        logger.info('reconcile(%s) ==> %s', constraint, additional_substitution)
    

        if isinstance(additional_substitution, Refutation):
            return additional_substitution
        else:
            substitution.update(additional_substitution)

        remaining_constraints = [c.substitute(additional_substitution) for c in remaining_constraints]
        
    return substitution

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('').setLevel(logging.DEBUG)
    
    with open(sys.argv[1]) as fh:
        proggy = ast.parse(fh.read())

    cs = constraintgen.constraints({}, proggy)
    print cs.pretty()

    substitution = solve(cs.constraints)
    print substitution

    print cs.substitute(substitution).pretty()
