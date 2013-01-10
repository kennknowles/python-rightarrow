A Type Language for Python
==========================

https://github.com/kennknowles/python-typelanguage

This module provides a type language for communicating about Python programs and values. 

Humans communicating to other humans, humans communicating to the computer, and even the computer
communicating to humans (via type inference and run-time contract checking).


The Types
---------

This type language provides the following concepts:

 * Atomic types `int`, `long`, `float`, `complex`, `str`, `unicode`
 * Compound types for tuples, lists, dictionaries, written `(int, str)`,  `[int]`, {int: str}
 * Object types `object(field1: int, field2: string) `
 * Function types like `int -> int`, `str` (they can get much more complex in Python, though - see below)
 * Polymorphic types like `forall a. [a] -> [a]`

Function Types
--------------

The basic type of e.g. `str -> str` is pretty easy. But what about named args? `*args`? `**kwargs`?
We try to re-use the function call / declaration syntax also in the types, so they can look like this:

(int, *[int], **{int: str}) -> str 

Type Inference
--------------

In the spirit of Python and dynamic languages, type inference is best-effort. Based
on the program, this module can discover constraints between types present at different
parts of the program. This constraint set may well be undecidable, especially if your
program gets crazy. In most sane code, types will be almost entirely inferrable.


Further Reading:
----------------

There are many projects that check contracts or types for Python in some way or
another, but they all focus on checking, not communicating. As such, they miss what
I like best about types.

 * RPython / PyPy
 * pySonar
 * typechecker
 * contracts
 * pyDBC


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
