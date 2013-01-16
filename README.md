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
 - Polymorphic types (where `~a`, `~b`, `~c` range over any other type)
    - `~a -> ~a`
    - `[~a] -> [~a]`
    - `( (~a, ~b) ) -> ~a`


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


More to explore
---------------

There are many other projects that check contracts or types for Python in some way or
another, but none makes communication their primary goal, with the possible exception 
of pySonar. As such, they make different design choices. Some are research projects
or prototypes -- this is not. This is a library meant for use. 

 * [PEP 316](http://www.python.org/dev/peps/pep-0316/) (deferred)
 * [RPython](http://doc.pypy.org/en/latest/translation.html) and [PyPy](http://pypy.org/) (compilation-oriented)
 * [pySonar](http://yinwang0.wordpress.com/2010/09/12/pysonar/) and [mini-pysonar](https://github.com/yinwang0/mini-pysonar)
   (way cool)
 * [Pyntch](http://www.unixuser.org/~euske/python/pyntch/index.html)
 * [typechecker](https://github.com/shomah4a/typechecker)
 * [pycontract](http://www.wayforward.net/pycontract/)
 * [python-dbc](http://code.google.com/p/python-dbc/) 
   and [pyDBC](http://www.nongnu.org/pydbc/) 
   are another cool-looking approach to typing Python.
   and another [pydbc](https://github.com/cadrian/pydbc) and another [pyDBC](https://github.com/Ceasar/pyDbC)
 * [python-type-inference](http://code.google.com/p/python-type-inference/wiki/Resources) (no code, but has a great list of papers and even more tools)

And since dynamic languages are much of a muchness, it is worthwhile seeing what is
happening elsewhere, though again very few projects emphasize the types themselves as
fun, interesting and useful, only that the code has them.

 * [Contracts in Racket](http://docs.racket-lang.org/guide/contracts.html) and [Typed Racket](http://docs.racket-lang.org/ts-guide/)
 * [Typescript](http://www.typescriptlang.org/) 
   aka [a slightly gradually-typed Javascript](http://siek.blogspot.com/2012/10/is-typescript-gradually-typed-part-1.html)
   and [Javascript++](http://jspp.javascript.am/) (sort of gradually-typed Javascript)
   and [javascript-contracts](https://github.com/brownplt/javascript-contracts)
   and [cerny](http://www.cerny-online.com/cerny.js/)
 * [Este](https://github.com/Steida/este) (statically-typed coffeescript) 
   and [Uberscript](https://github.com/jstrachan/coffee-script/blob/master/TypeAnnotations.md) (gradually-typed coffeescript)
   and [contracts.coffee](http://disnetdev.com/contracts.coffee/)
 * [Contracts.ruby](https://github.com/egonSchiele/contracts.ruby)

I'm omitting the billion typed languages that compile to Javascript because those are just typed languages compiler to the assembly
language of the web.

Finally, if you want to actually grok types, then contracts, then types and contracts
together, then types and dynamic types together, then _polymorphic_ type as contracts
and dynamic types together, then type inference for such systems,
try this chronological series of reading.

 - [_Types and Programming Languages_](http://www.cis.upenn.edu/~bcpierce/tapl/) by Benjamin Pierce.
 - [Contracts for higher-order functions](http://www.eecs.northwestern.edu/~robby/pubs/papers/ho-contracts-icfp2002.pdf)
   by Robert Bruce Findler & Matthias Felleisen. ICFP 2002.
 - [Hybrid type checking](http://users.soe.ucsc.edu/~cormac/papers/toplas09.pdf)
   by Kenneth Knowles & Cormac Flanagan. TOPLAS 2010. (expanded and corrected from POPL 2006)
 - [Gradual typing for functional languages](http://ecee.colorado.edu/~siek/pubs/pubs/2006/siek06_gradual.pdf)
   by Jeremy Siek & Walid Taha. Scheme workshop 2006.
 - [Gradual Typing for Objects](http://ecee.colorado.edu/~siek/gradual-obj.pdf)
   by Jeremy Siek and Walid Taha. ECOOP 2007.
 - [Type reconstruction for general refinement types](http://users.soe.ucsc.edu/~cormac/papers/esop07.pdf)
   by Kenneth Knowles & Cormac Flanagan. ESOP 2007.
 - [Relationally-parametric polymorphic contracts](http://cs.brown.edu/~sk/Publications/Papers/Published/gmfk-rel-par-poly-cont/paper.pdf)
   by Arjun Guha, Jacob Matthews, Robert Bruce Findler, and Shriram Krishnamurthi. DLS 2007.
 - [Gradual typing with unification based inference](http://ecee.colorado.edu/~siek/dls08igtlc.pdf)
   by Jeremy Siek and Manish Vachharajani. DLS 2008.
 - [Blame for all](http://homepages.inf.ed.ac.uk/wadler/papers/blame-for-all/blame-for-all.pdf)
   by Amal Ahmed, Robert Bruce Findler, Jacob Matthews, and Philip Wadler. STOP 2009.
 - [Always available static and dynamic feedback](http://homes.cs.washington.edu/~mernst/pubs/ductile-icse2011.pdf)
   by Michael Bayne, Richard Cook, and Michael D. Ernst. ICSE 2011.
 - [The ins and outs of of gradual type inference](http://www.cs.umd.edu/~avik/papers/iogti.pdf)
   by Aseem Rastogi, Avik Chaudhuri, and Basil Hosmer. POPL 2012.



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
