# Structure

As mentioned in the readme, our computing architecture is the following:

> We've got a distributed
> ML-framework where we've got datacenters all over the world! To remain innocuous, we have the following architecture:

> At each house in a city-block we have a single model which we use to calculate the gradients. These gradients are then
> propagated up to a **mini-data-center** (MDC) where they are accumulated before being sent up to our HQ in the
**North Pole data center**, (NPDC).

> NPDC <- MDC <- in-home-model

One thing that bears mentioning explicitly is that we should keep as little data as possible in-memory because that
would
be far too memory-intensive; Even big-tech would have a problem keeping data on all the people on earth ;)

Also, you want to test across various failure probabilities, so we consider that too. After all, we want to be sure that
our code is robust.

# Functions

- `ihm_success`: what the in-home model returns to the MDC in the event of a success
- `ihm_failure`: failure case of ^
- `mdc_processor`: what the MDC does upon receiving the in-home model results
- `npdc_processor`: what the NPDC does upon receiving the mdc results

# Scenario

You've inherited the old architecture and decided to remove most of it, only keeping the good parts. You also decide to
start from scratch and asked your new boss, Noel, to get you a list of the task requirements for the MVP.

In the process, you've picked out a small city to test your changes on.

## MVP: Dec 26th

Noel comes running in with the list of tasks that you asked for:

1) how long each IHM takes
2) How many houses are serviced by the MDC
3) how many IHMs failed in their gradient collection per-MDC and overall

Seems like the bosses are interested in improving the stability of the systems

**A solution:**

See `day_1.py`

## MVP 2: Dec 27th

Sleep-deprived, you stumble into work and all around you see your bosses patting each other on the back for
giving you the promotion you. Surely, this isn't a good sign of things to come. Noel comes in looking sheepish with a
new list of tasks and these look like a doozy:

1) find the fastest and slowest MDCs (to fix up the connection/ bump up the hardware)
2) find the variance of the IHMs and the MDCs

**A solution:**

See `day_2.py`

## Day 3: Dec 28th The Cleanup

Completely exhausted, you stumble in. With baited breath, you stare at the door waiting for Noel to come bursting in
with more work, but it seems to be quiet. You decide to clean up the code as best you can for future maintainability

**Note to reader**: This is a cleanup day to make the code more modular so we can compare it against the monoid
implementation. Also, note that the monoid implementation makes it MUCH more amenable to things further down the road,
so even if it looks more verbose now, just know that it is, in my opinion, worth it.

**A solution:**

See `day_2_cleanup.py`

## Day 4: Monoids?

You call up the previous Lead ML-Elfgineer and chew him out for leaving you in such a mess. After your eggnog-fueled
rage has died down, he apologizes for the mess he left things in and the stress that it caused you. He advised you to
look up "Monoids" as that would have saved him a lot of the headache that he had. He hoped that it would help you write
good code and help you as you add new capabilities to the system.

Hmm, a `monoid`? You vageuly remember hearing your mathematician friends talking about it. Something about

> A monad is just a monoid in the category of endofunctors, what's the problem?

So, you decide to consult the ever-helpful [Wikipedia on Monoids](https://en.wikipedia.org/wiki/Monoid#Definition).
Well, a `monoid` in our context is a structure that obeys two basic properties:

```
1) has a "0" element
2) has a binary operation, ~,  that is associative i.e (a ~ b) ~ c == a ~ (b ~ c)
```

See [Monoids 101](monoids_101.md) for a further discussion, but knowing just those two properties should be enough.

# Followups:

Some prompts for the future discussions on functors and monads:

- What if we wanted to efficiently find some information about an IHM? Instead of doing a simple linear-search?
- What if we wanted to trace our operations through the distributed system to accumulate information?
- What if we wanted to stop worrying about
  the [billion dollar mistake](https://www.infoq.com/presentations/Null-References-The-Billion-Dollar-Mistake-Tony-Hoare/)