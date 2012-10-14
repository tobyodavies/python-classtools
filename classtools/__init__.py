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

from core import wraps, innerclass




def singleton(klass):
    """
    Prevents the creation of multiple instances of a class

    >>> @singleton
    ... class foo(object):
    ...     def __init__(self, x):
    ...         self.x=x
    >>> f = foo(1)
    >>> f == foo.getinstance(1)
    True
    >>> f2 = foo.getinstance(2)
    >>> f is f2
    True
    >>> f2.x
    1
    
    """
    
    @wraps(klass)
    class wrapper(klass):
        __doc__ = klass.__doc__
        
        instance = None

        def __new__(cls, *args, **kwargs):
            if wrapper.instance is None:
                # avoid deprication warnings!
                if klass.__new__ is object.__new__:
                    wrapper.instance = klass.__new__(cls)
                else:
                    wrapper.instance = klass.__new__(cls, *args, **kwargs)
            else:
                raise RuntimeError()
            return wrapper.instance

        @staticmethod
        def getinstance(*args, **kwargs):
            if wrapper.instance is None:
                return wrapper(*args, **kwargs)
            return wrapper.instance

    return wrapper





if __name__ == "__main__":
    import tests
    test.runtests()
