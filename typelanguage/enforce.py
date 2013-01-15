from decorator import decorator

from typelanguage.parser import TypeParser
    
def check(ty, val):
    "Checks that `val` adheres to type `ty`"
    
    if isinstance(ty, basestring):
        ty = TypeParser().parse(ty)

    return ty.enforce(val)

def guard(ty):
    "A decorator that wraps a function so it the type passed is enforced via `check`"
    return check(ty, f)
