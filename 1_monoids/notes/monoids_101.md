# Monoids Introduction

## Table of Contents:

1) [Class Declaration](#class-declaration)
    - [Haskell Class Declaration](#haskell-class-declaration)
    - [Python Class Declaration](#python-class-declaration)
2) [Laws and Properties](#laws-and-properties)
3) [Usecases](#usecases)
4) [Closing out](#closing-out)

## Class Declaration

Think of a class declaration as a "contract" between you, the developer and the programming language. If you declare a
class that
obeys these laws, you are guaranteed various properties. We use a Frankenstein's monster version of Python and Haskell
to introduce
this concept.

### Haskell Class Declaration

[Source: Haskell Monoid](https://wiki.haskell.org/Monoid), but note that we have actually deviated from this. The
documentation is an amazing resource,
but it involves a number of additional concepts that we feel detracts from the core concept we are trying to cover.

```haskell
class Monoid M where
    empty :: M
    binary :: M -> M -> M
```

The first line tells us that we must define an "empty" element i.e what happens in the default case.

The second line tells us that we must define some binary operation which takes two instances of monoid `M` and returns a
single instance
of monoid `M`.

### Python Class Declaration

```python
from abc import ABC, abstractmethod


class Monoid(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def empty(self):
        return

    @abstractmethod
    def __add__(self, other):
        return


class MyMonoid(Monoid):
    def __init__(self):
        ...

    def empty(self):
        ...

    def __add__(self, other):
        ...
```

## Laws and Properties

Monoids have two properties that must hold:

1) Has an “identity” object i.e there is an “empty”

    - Consider the natural numbers, $\mathbb{N}$. When considering the operation:
        - +: the identity element is 0
        - *: the identity element is 1

2) Associative:

- Order doesn’t matter
- E.g. 0 + 1 == 1 + 0

## Usecases

### Map Reduce

```python
# Given

some_list = [0, 1, 2]
func_to_map = lambda x: x + 1
reduction_func = lambda x, y: x + y
identity = 0

# Our Map-reduce would look like
from functools import reduce

reduce(identity,
       map(func_to_map, some_list),  # Result = [1, 2, 3],
       reduction_func
       )  # 6 from identity_element + 1 + 2 + 3
```

### Federated Learning

- as we'll see when we return to our tutorial ;) 

### Distributed ML

- instead of just sending the gradients, this may send more data e.g the models themselves.

# Closing out

Now that you've got a rough feel for monoids in some simplified scenarios, return to
the [1_monoids/README.md](../README.md) and start reading through
the scenario and code to see how your problems might (rapidly) grow, and how monoids can come in to help.
