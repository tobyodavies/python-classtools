import functools
import weakref

def wraps(wrapped, check_docstring=True):
    """
    decorator-decorator for wrapper classes

    >>> class foo(object):
    ...     "Docstring"
    >>> @wraps(foo)
    ... class bar(object):
    ...     __doc__=foo.__doc__
    >>> bar.__name__ == 'foo'
    True
    >>> bar.__module__ == foo.__module__
    True
    """
    def decorator(wrapper):
        wrapper.__name__ = wrapped.__name__
        wrapper.__module__ = wrapped.__module__
        if check_docstring:
            assert wrapper.__doc__ == wrapped.__doc__, "You must include __doc__ = wrapped.__doc__ in your class definition (this is not writable)"
        return wrapper
    return decorator


def fdecorator(wrappeddecorator):
    """
    >>> @fdecorator
    ... def printsomethingfirst(func, string):
    ...     def wrappedfunc(*args, **kwargs):
    ...         print string
    ...         func(*args, **kwargs)
    ...     return wrappedfunc
    >>> @printsomethingfirst('foo')
    ... def donothing():
    ...     "Does nothing"
    ...     pass
    >>> print donothing
    <function donothing ...>
    >>> donothing()
    foo
    >>> donothing.__doc__ == "Does nothing"
    True
    >>> print donothing.__name__
    donothing
    """

    @functools.wraps(wrappeddecorator)
    def initialwrappeddecorator(*args, **kwargs):
        def finalwrappeddecorator(wrappedfunc):
            return functools.wraps(wrappedfunc)(wrappeddecorator(wrappedfunc, *args, **kwargs))
        return finalwrappeddecorator

    return initialwrappeddecorator
    

class beforeinit(object):
    """
    
    Run a function during __new__ before __init__

    >>> def printx(obj): print 'x'
    >>> @beforeinit(printx)
    ... class foo(object):
    ...     pass
    >>> foo()
    x
    <....foo object ...>
    """

    def __init__(self, func):
        self.func=func

    def __call__(self, klass):
        @wraps(klass)
        class wrapped(klass):
            __doc__ = klass.__doc__
            def __new__(*args,**kwargs):
                retval = klass.__new__(*args, **kwargs)
                self.func(retval)
                return retval                                       
        return wrapped

class innerclass(object):
    """
    A descriptor for instance-based inner classes
    
    >>> class foo(object):
    ...     @innerclass('parentinstance')
    ...     class bar(object):
    ...         "This is a Bar"
    ...         def __init__(self):
    ...             pass
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
    
    def __init__(self,propname='parent'):
        self.propname=propname
        self.klasscache = weakref.WeakKeyDictionary()
        self.nullklass = None

    def __call__(self, klass):
        self.klass = klass

        @wraps(klass)
        class baseklass(klass):
            __doc__ = klass.__doc__
            def __new__(*args,**kwargs):
                retval = klass.__new__(*args, **kwargs)
                setattr(retval, propname, None)
                return retval
        
        self.baseklass = baseklass
        return self

    def _mkklass(self, instance):
        klass = self.klass
        propname = self.propname
        
        @wraps(klass)
        class wrapped(self.baseklass):
            __doc__ = klass.__doc__
            def __new__(*args,**kwargs):
                retval = klass.__new__(*args, **kwargs)
                setattr(retval, propname, instance)
                return retval
        return wrapped

    def __get__(self, instance, owner):
        if instance is None:
            return self.baseklass
        
        if instance not in self.klasscache:
            self.klasscache[instance] = self._mkklass(instance)

        return self.klasscache[instance]

