# Monads

## Table of Contents

1) [Intuition](#intuition)
2) [Class Declaration](#class-declaration)
    - [Disclaimer](#disclaimer)
3) [Laws and Properties](#laws-and-properties)
    - [Implementation Requirements](#implementation-requirements)
    - [Laws](#laws-)
4) [Examples](#examples)
    - [List](#over-a-list)
    - [Binary Search Tree](#a-binary-search-tree)
    - [A Custom Class](#a-custom-class)
5) [Closing Out](#closing-out)

## Intuition

Much like a `functor`, a `monad` can be thought of as a box. In fact, it can be thought of (in a reductionist manner) as
a functor, but with extra properties and requirements.

As in the case of functors, we describe how you can modify the contents of the box.

## Class Declaration

An intuition

### Haskell Class Declaration

```haskell
class Monad M where
    (>>=)  :: M T1 -> ( T1 -> M T2) -> M T2
    return ::   T1 -> M T1
```

where, as usual, `T1` and `T2` are abstract types. As usual, think of this as the abstract
base class that must be implemented to be considered a valid monad.

#### `>>=`

This line describes a monad (wrapping an instance of type `T1`), which takes in a function. That function takes a
type `T1` and
spits out a type `T2`. It then returns a type of M `T2`.

P.s this function is also known as `flatmap` or `bind` or any other number of names.
See [extra_credit.md - flatmap](extra_credit.md#flatmap) to
learn more about why it is called `flatmap`. In that we also discuss why the `(T1 -> M T2)` looks so familiar.

#### return

This operator is also known as `pure` or `unit`, depending on your language.

Think of this method as a way to "wrap up" your abstract thing into a monad. This allows you to then compose functions together willy-nilly without fear.

#### Disclaimer

**Note** We modified the types and the monad definition.

- We modified the types to be more in line with a templated type (as you might see in typed languages)

## Laws and Properties

### Implementation Requirements

As mentioned in the [README.md](README.md),

> A functor must support, [at the minimum, according to Haskell, ](https://wiki.haskell.org/Functor#Syntax), a `fmap`,
> which describes applying an arbitrary function into the data encapsulated in our class.

### Laws:

[Lookin at the Haskell documentation once again](https://wiki.haskell.org/Functor#Functor_Laws), to be a functor, two
laws must be satisfied:

```
1) identity transformations must be preserved
2) fmap (f . g)  ==  fmap f . fmap g (composition must be respected)
```

## Examples

### Over a list

As we can see, the  `fmap` for a list is basically the `map`

```python
from typing import Callable, List, TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2")


def our_list_map(
        incoming_list: List[T1],
        func: Callable[[T1], T2]
):
    return [func(el) for el in incoming_list]
# OR map(func, incoming_list)
```

### A Binary Search Tree

And here we use a binary-search-tree

```python

from typing import Callable, TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2")


class BinarySearchTree:
    def __init__(self):
        ...

    @staticmethod
    def fmap(
            func_to_apply: Callable[[T1], T2],
            bst_instance: "BinarySearchTree"
    ):
        horizon = [bst_instance.root]
        while horizon:
            curr_node = horizon.pop()
            if curr_node:
                curr_node.data = func_to_apply(curr_node.data)
                horizon.append(curr_node.left)
                horizon.append(curr_node.right)
        return bst_instance
```

### A Custom Class

However, the benefit of a functor is rather limited if all we can do is apply it
to built-in types. So, consider the following simple example:

```python
from typing import Callable, List, TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2")


class SomeCls():
    def __init__(self):
        self.d1 = "d1"
        self.d2 = "d2"
        self.c1 = "c1"
        self.c2 = "c2"

    @staticmethod
    def fmap_d(
            func_to_apply: Callable[[T1], T2],
            instance_of_SomeCls: "SomeCls"
    ):
        instance_of_SomeCls.d1 = func_to_apply(instance_of_SomeCls.d1)
        instance_of_SomeCls.d2 = func_to_apply(instance_of_SomeCls.d2)
        return instance_of_SomeCls

    @staticmethod
    def fmap_c(
            func_to_apply: Callable[[T1, T1], T2],
            instance_of_SomeCls: "SomeCls"
    ):
        """
        Calls our func_to_apply on (c1, c2) and alters c1
        """
        instance_of_SomeCls.c1 = func_to_apply(
            instance_of_SomeCls.c1,
        )
        return instance_of_SomeCls
```

See here how we provide two `fmap` definitions? Over the `d`s and the `c`s?

**Note** If you look online, you'll see the python examples break down a little. This is because
Python's type system isn't as well built for dynamic dispatch. Consider the following
from [Andrew Jarombek's Haskell Part VI: Functors
](https://jarombek.com/blog/may-28-2019-haskell-pt6):

```haskell
data Distance a = Miles a | Kilometers a | Meters a
                  deriving (Show, Read)
                  
instance Functor Distance where
  -- fmap :: (a -> b) -> Distance a -> Distance b
  fmap f (Miles x) = Miles (f x)
  fmap f (Kilometers x) = Kilometers (f x)
  fmap f (Meters x) = Meters (f x)
```

Notice how, depending on the "type" of distance, we can apply the `fmap` differently?

## Closing Out

And that's the power of a functor - it lets us abstract over containers of things. They let us "swap" out the
underlying "backend" (data structure) while still preserving a similar interface, as well as allowing our end user to
ignore the underlying implementation details.

As long as our end-user uses code that "obeys"
our requirements (function signatures), they do not need to care about how we do things in the background. For example,
see how in `sol/functor_day_1.py`, our implementation was "hardcoded" to a `List`? Not anymore!
