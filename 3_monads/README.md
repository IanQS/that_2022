# Welcome to Monads!

## Table of Contents

1) [Monads Primer](#monads-primer)
2) [Scenario](#scenario)
    - [Monads Day 0](#day-0--catching-up)
    - [Monads Day 1](#day-1--error-handling-is--optional)
    - [Monads Day 2](#day-2--logging)
3) [Closing Out](#closing-out)

## Monads Primer

Please read through [monads_101](notes/monads_101.md)

## Scenario

Head to the [foreword](foreword.md) and then come back.

After a successful interview with the big man himself (this was mostly a formality at this point), you joined "The
Workshop", Santa's R&D branch. You stare out the window of your office, marveling at how quickly your career has
progressed. Just then, Santa himself comes running in to the office.

> "The distributed ML team is running into a sackload of issues. I need you to talk to them and fix it ASAP.

![Sack of problems](../assets/big_sack_of_problems.jpg)

Maybe adding in some high concept stuff without educating the team about these ideas first was a bad idea.... You know
what? You should write
a tutorial and post it on LinkedIn to educate other people (just like [this guy](https://www.linkedin.com/in/ianq/))

## Day 0: Catching up

You ping Noel again, begging to be put in touch with the current lead to find out what has been going wrong. The lead
comes in and shares
that their debugging process has been a nightmare. They've got two main issues:

1) The lack of a unified data structure (we return a tuple in `simulate_ihm`)

2) logging has been a nightmare

Lets dig into these issues more

N.B.: we deal with a simplified `IHMResult` that was defined in the functor section. We don't use any of the implemented
functions,
and our code is just far cleaner this way.

### Unified Data Structure

Yes, they can map functions over both structures in a unified way thanks to your introduction of functors, but they'd
rather have a single structure and abstract things away.

NB: This might seem unrelated to monads, but I promise you that it sets up the problem quite nicely. To address this
portion, we'll need a way to wrap the `None` and the `Something`-ness.

### Logging Issues

Once we've got many functions being mapped over our data, depending on the "path" that the chunk of data flows down (
if-else's and all that),
various transformations happen. Using a `filter` isn't always the best idea because, as before, you don't want to end up
with different data (yes, the plural) floating around.

TL;DR things have been a nightmare, and you dug us into this hole now get us out ()

They've got functions calling functions, and they need a way to pass
around logs. Your
`Monoids` and `Functors` have been extremely useful, but the team has ended up passing around lots of data and it is
difficult to maintain. Typically, they'd just overload the `__repr__` and `__str__` methods, but it's a little messy
visualizing
the tree-structure, and passing around the logs at every step is messy.

They tell you that they've used your final iteration of the code on functors and that it would be a fantastic starting
point.

## Day 1: Error handling is ... Optional?

You decide to tackle the first issue: unifying the data structure to return a single object instead of a tuple. Your
goals:

```
0) Modify the avl_tree class and IHM class to allow None-insertions
1) modify `map` to account for ^
```

As mentioned before, we deal with a simplified `IHMResult` that was defined in the functor section. We don't use any of
the implemented functions, and our code is just far cleaner this way.

### A solution

Check out [monad_day_1.py](sol/monad_day_1.py) specifically

```python

class OptionalIHM:
    def __init__(self, ihm_data: Optional[IHM] = None):
        self.ihm_data = ihm_data

    def apply_function(self, callable_func: Callable[[IHM], Union[IHM, None]]) -> "OptionalIHM":
        if self.ihm_data is None:
            return OptionalIHM(self.ihm_data)
        return OptionalIHM(callable_func(self.ihm_data))

    def __repr__(self):
        if self.ihm_data is None:
            return "None"
        return f"Some({self.ihm_data})"

    def __str__(self):
        return self.__repr__()

    def _get_(self, attr_name):
        if attr_name == "__setstate__":
            raise AttributeError(attr_name)
        if hasattr(self, attr_name):
            return getattr(self, attr_name)
            # return self.property_name
        if hasattr(self.ihm_data, attr_name):
            return getattr(self.ihm_data, attr_name)
        return None
```

Hopefully you've already read through the [monads_101](notes/monads_101.md), which introduces the concept of an "
Optional". This is important BECAUSE we build off this for the next portion.

## Day 2: Logging

With that out of the way, you rush to fix up the logging issues. Since each datum **might** go through a different path
depending on the values, it's probably better to just attach
the logs onto each value to trace where exactly in the branches it goes.

```
0) Track the path each datum goes through
```

### A solution

Check out [monad_day_2.py](sol/monad_day_2.py) specifically

## Closing Out

That's all, folks! Thank you for sticking it through to the end - I know it got dicey at times and you might have wanted
to bail. But you kept at it and I think that says a lot.

One thing I will leave you with is that it's important to remember that all of these are merely "suggestion"s i.e you
don't **need** to follow these instructions. In fact, python doesn't
have a strong typing, which means that implementing some of these will make your code more verbose.

However, I hope that it helps you appreciate abstraction in how you think about your code. One quote that I quite like
is:

> “Functional languages excel at wholemeal programming, a term coined by Geraint Jones. Wholemeal programming means to
> think big: work with an entire list, rather than a sequence of elements; develop a solution space, rather than an
> individual solution; imagine a graph, rather than a single path. The wholemeal approach often offers new insights or
> provides new perspectives on a given problem. It is nicely complemented by the idea of projective programming: first
> solve a more general problem, then extract the interesting bits and pieces by transforming the general program into
> more
> specialised ones.”

aka why worry about the small stuff? One really cool idea about this style of programming is that if creating threads or
new processes were free, our code could
become [Embarrassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel).

### Extra Credit

Try and work out what exactly the differences are between functors and monads (look at their signatures). If you recall
from our earlier discussion on [monoids](../1_monoids/README.md#dec-29th--monoids), we mentioned

> A monad is just a monoid in the category of endofunctors, what's the problem?

so there's clearly SOME relation between them. Check it out and then work your way through our
discussion: [Functors v. Monads](notes/functors_monads.md)