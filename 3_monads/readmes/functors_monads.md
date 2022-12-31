# Monads and Functors Discussion

## A Reminder

As has been said multiple timese, this [excellent answer](https://stackoverflow.com/a/56601178/3532564) describes, at a
very high level, `functors`
and `monads`

`functors` and `monads` both provide some tool to wrapped input, returning a wrapped output.

- `functor` = map (i.e. the tool)

- `monad` = unit + flatMap (or bind or chain)

---

Monads and functors look VERY similar. In fact, let's put them "side-by-side":

```
class Functor F where
    fmap :: (a -> b) -> F a -> F b
```

```
class Monad M where
  (>>=)  :: M a -> (  a -> M b) -> M b
  return ::   a                 -> M a
```

In the first "line" of both classes, we are "defining an interface" that describes how we "open" the structure and apply
the functions.

- `fmap`: means that we must specify a way to apply an arbitrary (valid) function to the internal contents (of type `a`)
  of our functor structure, `F`.

- `>>=` describes how for a given structure, `M`, we can take a function and operate on the internal contents of the
  type. Note that, unlike the `fmap`, our return value is the Monad, not the to-be-wrapped value.

If you squint enough, the two are more-or-less the same

**Note** we removed the `(>>)` from `Monads` and `(<$)` from `Functor` as they aren't as relevant for our discussion in
this tutorial.
