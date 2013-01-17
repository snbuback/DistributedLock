from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import os

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = '-s -v'.split() + [ 'tests/%s' % test for test in filter(lambda f: f.endswith('.py'), os.listdir('tests')) ]
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='DistributedLock',
    version='1.2',
    author='Silvano Buback',
    author_email='snbuback@gmail.com',
    packages=find_packages(),
#    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/snbuback/DistributedLock',
    license='LICENSE.txt',
    description='Python Distributed Lock with memcached support',
    long_description=open('README').read(),
    install_requires=[
        "python-memcached >= 1.40",
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    
)