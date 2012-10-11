# classtools v 0.1 https://github.com/tobyodavies/python-classtools/
#
# Copyright (c) 2012, Toby Davies
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
             

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
