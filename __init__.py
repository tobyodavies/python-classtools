"""
This library aims to be a simple set of decorators and tools for use with classes.

Functools works remarkably well for a lot of things
but there are some things that ought to be easier to do.
"""

import functools

class innerclass(object):
    """
    A descriptor for instance-based inner classes
    
    >>> class foo(object):
    ...     @innerclass
    ...     class bar(object):
    ...         "This is a Bar"
    ...         def __init__(self, outer):
    ...             self.parentinstance = outer
    ...
    >>> f = foo()
    >>> b = f.bar()
    >>> b.__class__.__name__
    'bar'
    >>> b.__doc__
    'This is a Bar'
    >>> b.__module__ == f.__module__
    True
    >>> b.parentinstance is f
    True
    >>> b2 = f.bar()
    >>> b2.__class__ == b.__class__
    True
    >>> f2 = foo()
    >>> b3 = f2.bar()
    >>> b3.parentinstance == b.parentinstance
    False
    """
    
    def __init__(self, klass):
        self.klass = klass

    def __get__(self, instance, owner):
        return functools.partial(self.klass, outer=instance)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
