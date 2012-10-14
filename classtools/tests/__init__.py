import sys
import pytest

def runtests(args=sys.argv):
    return pytest.main(['--doctest-modules', '--pyargs', 'classtools']+args) == 0

