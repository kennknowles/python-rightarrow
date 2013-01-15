A Type Language for Python
==========================

https://github.com/kennknowles/python-typelanguage

This package provides a type language for communicating about Python programs and values. 
Humans communicating to other humans, humans communicating to the computer, and even the computer
communicating to humans (via type inference and run-time contract checking).

This project has a "duck-typed" status: Whatever you can use it for, it is ready for :-)

Here is a more concrete list of implemented and intended features:

 - _yes_      - Definition of a type language.
 - _yes_      - Parsing and printing.
 - _yes_      - Monitoring of type adherence for monomorphic types.
 - _yes_      - "Any" type for easily saying exactly where things get really dynamic.
 - _upcoming_ - Monitoring of type adherence for polymorphic types.
 - _upcoming_ - Generation of constraints between types in a program.
 - _upcoming_ - Best-effort inference of suitable types.
 - _upcoming_ - Refinement types with hybrid type checking.


The Types
---------

This type language is built from the following concepts:

 - Named types: `int`, `long`, `float`, `complex`, `str`, `unicode`, `file`, `YourClassNameHere`, ...
 - List types: `[int]`, `[[long]]`, ...
 - Tuple types: `(int, long)`, `(float, (int, Regex))`, ...
 - Dictionary types: `{string: float}`, `{ (str, str) : [complex] }`, ...
 * Union types `int|long|float`, `str|file`, ...
 - The "any" type, `??`, for when a value is too complex to describe in this language. May be an indication that
   a piece of code is metaprogramming or should be treated with gradual typing.
 - Function types:
    - `str -> int`
    - `(int) -> int`
    - `(int, int) -> int`
    - `( (int, int) ) -> int`
    - `( str|file ) -> SomeClass`
    - `(int, *[str]) -> [(str, int)]`
    - `(int, *[int], **{int: str}) -> str`
 - Object types: `object(self_type, field1: int, field2: str, ...)`
 - Polymorphic types (where `~a`, `~b`, ~c` range over any other type)
    - `~a -> ~a`
    - `[~a] -> [~a]`
    - `( (~a, ~b) ) -> ~a`

(TODO: Since tilde is special to pandoc markdown and other markdowns in other ways, choose a better
way to write polymorphic types that also makes sense in Python)


Types as Contracts
------------------

The module `typelanguage.enforce` contains functions for using these types as
run-time monitors.

Applied directly:

```python
>>> check('{string: int}', {"hello" : "there"})
```

More interestingly, automatically protecting a function from bad input,
for example, putting better error checking on Python's `unicode`/`str`
interactions.

```python
>>> '\xa3'.encode('utf-8')
...
UnicodeDecodeError: 'ascii' codec can't decode byte 0xa3 in position 0: ordinal not in range(128)

>>> @guard('unicode -> str')
... def safe_encode(s):
...    return s.encode('utf-8')

>>> safe_encode(u'hello')
'hello'
>>> safe_encode('\xa3')
TypeError: Type check failed: ? does not have type unicode
```

Eventually, the notion of _blame_ may be usefully incorporated, for pointing
out which piece of code or agent in a distributed setting is responsible
for the undesirable value.


Type Inference
--------------

In the spirit of Python and dynamic languages, type inference is best-effort. It works like so:

1. By traversing the code, we can discover a bunch of constraints between types in
   different bits.
2. Some of these constraints are going to be very easy to solve, so we can just
   propagate the results.
3. Some of these constraints are not going to be practical to try to solve, so we
   can just drop them or insert some enforcement code if we like.


Further Reading:
----------------

There's no way to give enough great links for reading about types,
contracts, hybrid typing, gradual typing, type inference, etc, but
here are some key starting points that inspire specific parts of
this project.

(TODO: find hrefs)

 - The seminal work on dynamically-checked conttracts is Findler & Felleisen 2002. The
   core ideas of _blame_ and wrapping functions were here.
 - Flanagan combined that notion with types in Hybrid Type Checking 2006 (later expanded and corrected into Knowles-Flanagan 2010)
 - The term _gradual typing_ was created by Siek and Taha to describe a particular type
   of Hybrid Type Checking focused on the "Any" type.
 - Knowles-Flanagan 2007 showed that type inference is decidable even if type checking isn't,
   and it is that method of type reconstruction that inspires the constraint generation and 
   solving here.

There are many other projects that check contracts or types for Python in some way or
another, but they all focus on checking, not communicating. As such, they miss what
I like best about types.

 * RPython / PyPy
 * pySonar
 * typechecker
 * contracts
 * pyDBC

And since dynamic languages are much of a muchness, it is worthwhile seeing what is
happening elsewhere:

 * contracts.coffee
 * Racket
 * ...


Contributors
------------

 * [Kenn Knowles](https://github.com/kennknowles) ([@kennknowles](https://twitter.com/KennKnowles))


Copyright and License
---------------------

Copyright 2012- Kenneth Knowles

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
