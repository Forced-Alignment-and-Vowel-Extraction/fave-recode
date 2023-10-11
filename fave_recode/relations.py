from functools import wraps

def in_relation(lhs, rhs):
    return(lhs in rhs)

def equals_relation(lhs, rhs):
    return(lhs == rhs)

def contains_relation(rhs, lhs):
    return(lhs in rhs)

def negate(f):
    @wraps(f)
    def g(*args,**kwargs):
        return(not f(*args,**kwargs))
    g.__name__ = f'negate({f.__name__})'
    return g

relation = {
    "in": in_relation,
    "not in": negate(in_relation),
    "contains": contains_relation,
    "excludes": negate(contains_relation),
    "==": equals_relation,
    "!=": negate(equals_relation)
}