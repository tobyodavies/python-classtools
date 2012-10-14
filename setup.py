#!/usr/bin/env python

from distutils.core import setup, Command

class TestCommand(Command):
    """
    Run tests with `setup.py test`
    """
    user_options=[]
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import classtools.tests
        classtools.tests.runtests()

setup(name='classtools',
            version='0.1',
            description='Functools for classes',
            author='Toby Davies',
            author_email='tobyodavies@gmail.com',
            url='https://github.com/tobyodavies/python-classtools/',
            packages=['classtools', 'classtools.tests'],
            requires=['pytest (>=2.0)'],
            cmdclass={'test': TestCommand}
           )
