# Structure

As mentioned in the [top-level-readme](../README.md), we've got a distributed ML framework. We have data centers all
over
the world, and to stay hidden, we have the following architecture:

> At each house in a city block, we use a single model to calculate the gradients. These gradients are
> propagated up to a **mini-data-center** (MDC), where they are accumulated before being sent up to our HQ in the
**North Pole data center**, (NPDC).

TL;DR our architecture looks like the following

![architecture](../assets/architecture.jpg)

> NPDC <- MDC <- in-home-model

## Foreword:

### Notes

We should keep as little data as possible in-memory because that would be far too memory-intensive; Even big tech would
have trouble storing information about all the people on earth ;)
We want to test across various failure probabilities. Due to some issues in the hardware department (supply chain issues
and silicon shortages), we haven't been able to update all our in-home-model hardware.

### Functions

- `ihm_success`: what the in-home model returns to the MDC in the event of a success
- `ihm_failure`: failure case of ^
- `mdc_processor`: what the MDC does upon receiving the in-home model results
- `npdc_processor`: what the NPDC does upon receiving the MDC results

## Scenario

You've inherited the old architecture and decided to throw out most of it, only keeping the good parts
in `sol/day_0.py`. You ask your new boss, Noel, to get you a list of the task requirements for the MVP. Like any good
Elfgineer, you pick out a small city to test your changes on, hence why you aren't getting overwhelmed with results and
errors.

## MVP: Dec 26th

Noel comes running in with the list of tasks that you asked for:

### Tasklist

1) how long does each IHM takes
2) How many houses are serviced by the MDC
3) how many IHMs failed in their gradient collection per-MDC and overall

The bosses are interested in identifying the critical areas first, which will give them an idea of how to improve the
stability of the systems.

### A Solution:

See `sol/monoids_day_1.py`

## MVP 2: Dec 27th MORE work?

Sleep-deprived, you stumble into work with a coffee in hand; all around, you see your bosses patting each other on the
back for
giving you the promotion. Surely, this isn't a good sign of things to come. Noel comes in looking sheepish with a
new list of tasks, and these look like a doozy:

### Tasklist

1) find the fastest and slowest MDCs (to fix up the connection/ bump up the hardware)
2) find the variance of the IHMs and the MDCs

You knew they would ask for these things but didn't account for them when you first started coding. You grumble about "
past" you and how you ended up giving yourself more work.

### A Solution:

See `sol/monoids_day_2.py`

## Day 3: Dec 28th The Cleanup

Completely exhausted, you stumble in. With bated breath, you stare at the door waiting for Noel to come bursting in
with more work, but it seems quiet. You hide under your desk and decide to clean up the code as best you can for future
maintainability.

### To the reader:

This is a cleanup day to make the code more modular, so we can more fairly compare it against the monoid
implementation.

### A Solution:

See `sol/monoids_day_3_cleanup.py`

## Day 4: Monoids?

You call up the previous Lead ML-Elfgineer, and chew him out for leaving you in such a mess. After your eggnog-fueled
rage has died down, he apologizes for the mess he left things in and the stress it is causing you. He shares that he has
been learning some category theory in his new role and that it might serve you well. After you remind him of the
distributed architecture, he advises you to
look up "Monoids".

Hmm, a `monoid`? You vaguely remember hearing your mathematician friends talking about it. Something about

> A monad is just a monoid in the category of endofunctors, what's the problem?

So, you decide to consult the ever-helpful [Wikipedia on Monoids](https://en.wikipedia.org/wiki/Monoid#Definition).
Well, a `monoid` in our context is a structure that obeys two basic properties:

```
1) has a "0" element
2) has a binary operation, ~,  that is associative i.e (a ~ b) ~ c == a ~ (b ~ c)
```

See [Monoids 101](monoids_101.md) for a further discussion, but knowing just those two properties should be enough.

### A Solution

See `sol/day_4_monoids.py`

# Discussion

We see that in `sol/monoids_day_3_cleanup.py`, most of the "pipeline-ing" logic is done in the `npdc_processor` and
the `mdc_processor`. However, in the
`sol/monoids_day_4_final.py`, most of the logic of "joining" the data exists in the `MDC` and `NPDC` objects themselves.

What is nice about this is that if we so wish, we can "swap" out our data - as long as our `NPDC_Monoid`
and `MDC_Monoid` obey the interface (accepted arguments, return values, etc.), we can simply swap things out. Contrast that
with how tightly intertwined the logic is in the `monoids_day_3_cleanup.py` code.

# Followups:

Some things to consider as we go into functors and monads:

- What if we wanted to efficiently find some information about an IHM? Instead of doing a simple linear search?
- What if we wanted to trace our operations through the distributed system to accumulate information?
- What if we wanted to stop worrying about
  the [billion dollar mistake](https://www.infoq.com/presentations/Null-References-The-Billion-Dollar-Mistake-Tony-Hoare/)