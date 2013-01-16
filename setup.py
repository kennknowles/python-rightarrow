import setuptools 
import os.path
import subprocess

# Build README.txt from README.md if not present
if not os.path.exists('README.txt'):
    subprocess.call(['pandoc', '--to=rst', '--smart', '--output=README.txt', 'README.md'])

setuptools.setup(
    name='typelanguage',
    version='0.1',
    description='A type language for Python, including parsing, pretty-printing, type inference, type checking, and run-time contract enforcement.',
    author='Kenneth Knowles',
    author_email='kenn.knowles@gmail.com',
    license='Apache 2.0',
    long_description=open('README.txt').read(),
    packages = ['typelanguage'],
    test_suite = 'tests',
    install_requires = [ 'ply', 'decorator' ],
)
