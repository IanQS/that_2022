# Monads and Functors Discussion

I'd recommend only reading this section after reading the rest of the material. Here, we highlight the
similarities and differences between monads and functors two.

## What's the diff?

This [excellent answer](https://stackoverflow.com/a/56601178/3532564) describes, at a
very high level, `functors`
and `monads`

> `functors` and `monads` both provide some tool to wrapped input, returning a wrapped output.

- `functor` = map (i.e., the tool)

- `Monad` = unit + flatMap (or bind or chain)

### Recap: Functor

An abstract class definition is like the following:

```
class Functor F where
    fmap :: (a -> b) -> F a -> F b
    (<$) :: a -> F b -> F a
```

> `fmap`

The fmap describes how you can apply a function, `func`, to the contents of the `functor`.

> `<$`

Describes how you can take an initial value and replace the contents of an existing functor with it (we do not cover this)

### Recap: Monad

An abstract class definition is like the following:

```
class Monad M where
  (>>=)  :: M a -> (  a -> M b) -> M b
  return ::   a                 -> M a
  (>>)   :: m a ->  m b         -> m b
  ^ we don't actually cover this
```

> `>>=`

describes how for a given structure, `M`, we can take a function and operate on the internal contents of the type. Note
that, unlike the `fmap`, our return value is the Monad, not the to-be-wrapped value.

> `return`

create an instance of the monad from an initial value

## Differences

We see that both structures offer an abstract way to "apply" the internal function to the instances. Both also offer
a way to create an instance from existing values, albeit in different ways.

Something worth noting is that a monad is a more "powerful" (and restricted) functor, because all monads are functors.

# Closing out

A monad is "just" a functor with more requirements