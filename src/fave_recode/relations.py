"""
Functions defining Boolean relations between 
`lhs` (the rule conditions `attribute`) and the 
`rhs` (the rule condition `set1`)
"""
from functools import wraps
from typing import Any
from collections.abc import Callable

import re

def negate(f:Callable) -> Callable:
    # """Negate a function

    # Given a function `f()` that returns a boolean, this will
    # return `g() = not f()`

    # ```{python}
    # from fave_recode.relations import negate

    # def f():
    #   return True

    # g = negate(f)
    # g()
    # ```

    # Args:
    #     f (Callable): A function that returns a boolean

    # Returns:
    #    (Callable): not f()
    # """
    @wraps(f)
    def g(*args,**kwargs):
        return(not f(*args,**kwargs))
    g.__name__ = f'negate({f.__name__})'
    return g


def in_relation(lhs:Any, rhs:Any) -> bool:
    """Is `lhs` in `rhs`?

    ```{python}
    from fave_recode.relations import in_relation
    in_relation('x', 'xyz')
    ```

    Args:
        lhs (Any): left hand side object
        rhs (Any): right hand side object (must work with `in`)

    Returns:
        (bool): `True` or `False`
    """
    return lhs in rhs

def not_in_relation(lhs: Any, rhs: Any) -> bool:
    """Is `lhs` *not* in `rhs`

    ```{python}
    from fave_recode.relations import not_in_relation

    not_in_relation('x', 'xyz')
    ```

    Args:
        lhs (Any): left hand side
        rhs (Any): right hand side (must work with `in`)

    Returns:
        (bool): `True` or `False`
    """
    return negate(in_relation)(lhs, rhs)

def contains_relation(lhs:Any, rhs:Any)->bool:
    """Does `lhs` contain `rhs`?

    ```{python}
    from fave_recode.relations import contains_relation

    contains_relation('xyz', 'x')
    ```

    Args:
        lhs (Any): left hand side (must work with `in`)
        rhs (Any): right hand side

    Returns:
        (bool):`True` or `False`
    """
    return rhs in lhs

def excludes_relation(lhs:Any, rhs:Any)->bool:
    """Does `lhs` *not* contain `rhs`

    Args:
        lhs (Any): left hand side (must work with `in`)
        rhs (Any): right handnside

    Returns:
        (bool): True or False
    """
    return negate(contains_relation)(lhs, rhs)

def equals_relation(lhs:Any, rhs:Any)->bool:
    """Is lhs `==` to `rhs`

    Args:
        lhs (Any): left hand side
        rhs (Any): right hand side

    Returns:
        (bool): True or False
    """
    return(lhs == rhs)

def not_equals_relation(lhs: Any, rhs: any)->bool:
    """is lhs *not* `==` rhs

    Args:
        lhs (Any): left hand side
        rhs (any): right hand side

    Returns:
        (bool): True or False
    """
    return negate(equals_relation)(lhs, rhs)


def rematches_relation(lhs:str, rhs:str) ->bool:
    """Does the lhs match a regex for rhs?

    Args:
        lhs (str): left hand side
        rhs (str): right hand side (must be valid regex.)

    Returns:
        (bool): True or False
    """
    if re.search(rhs, lhs):
        return(True)
    else:
        return(False)

def reunmatches_relation(lhs:str, rhs:str) -> bool:
    """Does the lhs *not* match a regex for the rhs

    Args:
        lhs (str): left hand side
        rhs (str): right hand side

    Returns:
        (bool): True or False
    """
    return negate(rematches_relation)(lhs, rhs)



relation_dict = {
    "in": in_relation,
    "not in": not_in_relation,
    "contains": contains_relation,
    "excludes": excludes_relation,
    "==": equals_relation,
    "!=": not_equals_relation,
    "rematches": rematches_relation,
    "reunmatches": reunmatches_relation
}