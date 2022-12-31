# Foreword

## How I started

Start here because this is important. Back when I was first learning about `Monads`, I found
the [Haskell Wiki about Monads](https://wiki.haskell.org/Monad)
and [The Absolute Best Intro to Monads For Software Engineers by Studying with Alex](https://www.youtube.com/watch?v=C2w45qRc3aU)
which were invaluable (and I **highly** recommend you check them out after this tutorial). Additionally, I recommend
reading
through [adit.io - Functors, Applicatives, And Monads In Pictures](https://adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html)

Unless you've had some experience with functional programming and the notion of "impure" and "
pure" functions, I'd recommend reading this tutorial first.

**Note**: functional programming just means a programming that deals in the style of "functions" in math. See the below
for more. I know some people who aren't familiar with FP mistake it for meaning "better" than non-FP - that non-FP is
code that just doesn't "work" or "function" (but I know some
FP-ers who think that way too)

## Purity and Impurity

See [preface_purity_impurity](preface_purity_impurity.py) for some code examples (looking at our previously developed
code) showcasing `purity` and `impurity`. To make a long story short, a pure function is more-or-less one that does NOT
mutate its input i.e the value is "fixed". Think of this like how we might do in math, where once we have defined a
variable, we do not "change" it, instead we just define a new one and "assign" to it.

The TL;DR programming notion of this is "if we run our code N-times with the same input, we always get the same result."

Now, why is this important? It is important because it helps us reason about our code. Proceed to the code example for a
better idea.

## Motivation for `Monads`

So, knowing that, we now realize that we have a problem. Although languages like `Haskell` (and other FPs) are made to
be pure, they are only "pure" in insofar as their language constructs. This would make them useless in real-world
scenarios e.g in ML where we deal with datasets, where we accept some user input, or where we have `IO`. So, that's
where `Monad`s come into play.

TL;DR `Monads` allow us to "wrap" the "impure" into a "pure" object via a container (not unlike our `functor`s) from
earlier.

[Back to main](README.md)