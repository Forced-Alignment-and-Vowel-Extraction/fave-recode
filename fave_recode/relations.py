from functools import wraps
from typing import Any
from collections.abc import Callable

import re

def in_relation(lhs:Any, rhs:Any) -> bool:
    return(lhs in rhs)

def equals_relation(lhs:Any, rhs:Any)->bool:
    return(lhs == rhs)

def contains_relation(rhs:Any, lhs:Any)->bool:
    return(lhs in rhs)

def rematches_relation(lhs:str, rhs:str) ->bool:
    if re.search(rhs, lhs):
        return(True)
    else:
        return(False)

def negate(f:Callable) -> bool:
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
    "!=": negate(equals_relation),
    "rematches": rematches_relation,
    "reunmatches": negate(rematches_relation)
}