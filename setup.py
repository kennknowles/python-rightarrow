import setuptools 
import sys
import os.path
import subprocess

# Build README.txt from README.md if not present
if not os.path.exists('README.txt') and 'sdist' in sys.argv:
    subprocess.call(['pandoc', '--to=rst', '--smart', '--output=README.txt', 'README.md'])

# But use the best README around
readme = 'README.txt' if os.path.exists('README.txt') else 'README.md'

setuptools.setup(
    name='rightarrow',
    version='0.4',
    description='A language for describing Python programs with concise higher-order annotations like "(a -> a) -> [a] -> [a]" but don\'t you dare call them "types"',
    author='Kenneth Knowles',
    author_email='kenn.knowles@gmail.com',
    url='https://github.com/kennknowles/python-rightarrow',
    license='Apache 2.0',
    long_description=open(readme).read(),
    packages = ['rightarrow'],
    test_suite = 'tests',
    install_requires = [ 'ply', 'decorator' ],
)
