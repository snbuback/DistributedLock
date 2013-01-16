from setuptools import setup, find_packages

setup(
    name='DistributedLock',
    version='1.1',
    author='Silvano Buback',
    author_email='snbuback@gmail.com',
    packages=find_packages(),
#    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/snbuback/DistributedLock',
    license='LICENSE.txt',
    description='Python Distributed Lock with memcached support',
    long_description=open('README.md').read(),
    install_requires=[
        "python-memcached >= 1.40",
    ],
)