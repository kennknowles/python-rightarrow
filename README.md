A Type Language for Python
==========================

https://github.com/kennknowles/python-typelanguage

This module provides a type language for communicating about Python programs and values. 

Humans communicating to other humans, humans communicating to the computer, and even the computer
communicating to humans (via type inference and run-time contract checking).

Project progress: Currently basic types can be parsed and basic Python code can have basic types
inferred. Next steps are parsing "all" types so that test cases for enforcement and type
inference are easy to construct.


The Types
---------

This type language provides the following concepts:

 * Atomic types, written just like Python's run-time tags: `int`, `long`, `float`, `complex`, `str`, `unicode`
 * Compound types for tuples, lists, dictionaries, written with analogous syntax: `(int, str)`,  `[int]`, `{int: str}`
 * Function types like `int -> int`, `str` (they can get much more complex in Python, though - see below)
 
And these are obviously necessary and planned, but the concrete syntax and typing rules are not in place yet:

 * Object types `object(field1: int, field2: str) `
 * Polymorphic types like `~a -> ~a` (the identity function) or `[~a] -> [~a]` for map (really `(Iteratable ~a -> Iterable ~a)`)
 * "Any" type, written `any` or `??` perhaps. This is when a piece of code does a lot of reflection, and we want to communicate that it works for "anything".
   This is also a key component of a _gradual typing_ system, which would be useful.
 * Union types like `str | int | any -> any` which add another layer of flexibility so we can communicate if a rather flexible function
   still requires some particular restriction.

Function Types
--------------

The basic type of e.g. `str -> str` is pretty easy. But what about named args? `*args`? `**kwargs`?
We try to re-use the function call / declaration syntax also in the types, so they can look like this:

 * `str -> int`
 * `(int) -> int`
 * `(int, int) -> int`
 * `(int, *[str]) -> [(str, int)]`
 * `(int, *[int], **{int: str}) -> str`

I have not yet wrapped my head around what needs to happen for kwonly args. Also untouched
is Python 3 where the AST for argument lists has changed.


Types as Contracts
------------------

TBD. It would be very easy to use these as composable assertions, as in
lots of contract systems. Recent developments both in blame assignment
and "gradual" typing make this a good fit.

```python
@enforce('int -> int')
def f(x):
   return x * 2
```

(it is actually more complicated, because you will want to know whether
it is your code or the calling code that is responsible, but exactly
how that works can vary)

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
