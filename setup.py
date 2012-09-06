import setuptools 
import datetime

setuptools.setup(
    name='typelanguage',
    version='0.1pre%s' % datetime.datetime.utcnow().isoformat(),
    description='A type language for Python, including parsing, pretty-printing, type inference, type checking, and run-time contract enforcement.',
    author='Kenneth Knowles',
    author_email='kenn.knowles@gmail.com',
    license='Apache 2.0',
    long_description='''\
    A type language is a higher-level language for describing
    and discussion programming ideas. Python does not have
    a standard type language, so it is difficult to precisely
    and concisely describe the input and output of functions
    and the methods on objects.''',

    packages = ['typelanguage'],
    test_suite = 'tests'
)
