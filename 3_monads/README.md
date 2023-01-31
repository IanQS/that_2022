# Welcome to Monads!

## Table of Contents

1) [Monads Primer](#monads-primer)
2) [Scenario](#scenario)
   - [Monads Day 1](#day-1--revisiting-an-old-friend)
   - [Monads Day 2]()
   - [Monads Day 3]
3) [Closing Out](#closing-out)

## Scenario

## Monads Primer

Please read through [monads_101](notes/monads_101.md)

## Scenario

Head to the [foreword](foreword.md) and then come back.

After a successful interview with the big man himself (this was mostly a formality at this point), you joined "The
Workshop", Santa's R&D branch. You stare out the window of your office, marveling at how quickly your career has
progressed. Just then Santa comes in saying "oh, when we last talked you mentioned you wanted to take on improving the
debugging? How's that going? The distributed systems team is running into a sack-load of issues".

![Sack of problems](../assets/big_sack_of_problems.jpg)

The question hangs in
the air before you turn around, point to your laptop and sit down to code. You really have to get this out ASAP


## Day 1: Revisiting An Old Friend

## Day 0: Catching up

You ping Noel again, begging to be put in touch with the current lead to find out what has been going wrong. The lead
comes in and shares
that their debugging process has been a nightmare. They've got functions calling functions and they need a way to pass
around logs. Your
`Monoids` and `Functors` have been extremely useful, but the team has ended up passing around lots of data and it is
difficult to maintain. Typically, they'd just overload the `__repr__` and `__str__` methods, but it's a little messy
visualizing
the tree-structure, and passing around the logs at every step is messy.

They tell you that they've used your final iteration of the code on functors and that it would be a fantastic starting
point.

## Day 1: Refactoring

You decide to tackle the issue of having the `None` values being stored in a separate data-structure. Ideally, they all
sit in the same place.

Task list

```
0) Modify the avl_tree class and IHM class to allow None-insertions
1) modify `map` to account for ^
```

### A solution

- `monad_day_1.py`

## Day 2: Logging



## Closing Out

And that's it all! Thank you for sticking it through to the end - I know it got dicey at times and you might have wanted
to bail. But you kept at it and I think that says a lot.

One thing I will leave you with is that it's important to remember that all of these are merely "suggestion"s i.e you
don't **need** to follow these instructions. In fact, python doesn't
have a strong typing, which means that implementing some of these will make your code more verbose.

However, I hope that it helps you appreciate abstraction over your thinking. One quote that I quite like is: 

> “Functional languages excel at wholemeal programming, a term coined by Geraint Jones. Wholemeal programming means to
think big: work with an entire list, rather than a sequence of elements; develop a solution space, rather than an
individual solution; imagine a graph, rather than a single path. The wholemeal approach often offers new insights or
provides new perspectives on a given problem. It is nicely complemented by the idea of projective programming: first
solve a more general problem, then extract the interesting bits and pieces by transforming the general program into more
specialised ones.”

aka why worry about the small stuff? One really cool idea about this style of programming is that if creating threads or 
new processes were free, our code could become [Embarrassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel).