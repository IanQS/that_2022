# Extra Credit

Here I list an assortment of random bits and bobs that I've come across and think that you might find interesting.

## Flatmap

aka `>>=` or bind

Recall the definition:

    M T1 -> ( T1 -> M T2) -> M T2

and let us apply the function to the monad. We immediately notice that we get

    M M T2

i.e we have a nested `M`. The "flat" comes from the fact that we "extra" out the inner `M T2` and only return that.

## Functor and Monad

Take a look at the `>>=`, specifically at the function it accepts

    T1 -> M T2

and notice how it looks very much like how an `fmap` (from functors, as I'm sure you remember) looks.

    T1 -> T2

. In fact, it looks like a composition of functions! It is basically a


    return fmap

in that it first applies a transformation and then wraps the value.