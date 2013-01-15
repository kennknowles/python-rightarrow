
from typelanguage.parser import TypeParser
    
def check(ty, val):
    if isinstance(ty, basestring):
        ty = TypeParser().parse(ty)

    ty.enforce(val)

def as_type(ty):
    "A decorator that wraps a function so it the type passed is enforced via `check`"
    
    def as_type(f, *args, **kwargs):
        return ty.enforce(f)(*args, **kwargs)

    return decorator(as_type)
