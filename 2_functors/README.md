# Welcome to Functors

## Table of Contents

1) [Functors Primer](#functors-primer)
2) [Scenario](#scenario)
    - [Functors Day 1](#mvp--feb-1st)
    - [Functors Day 2: Expanding the Requirements](#expanding-the-requirements)
    - [Functors Day 3: AVL Trees? Oh Noooo](#day-3--cleaning-up-our-avl-tree)
3) [Closing Out](#closing-out)

## Functors Primer

As in the section on monoids, see [notes/functors_101](notes/functors_101.md) for a quick and dirty introduction. It
would be useful to read that first before coming back, as
it should prime
your thinking and help you to reflect on what you are reading.

## Scenario

After your big project, you sneak off to Hawaii for a bit as you've been watching "White Lotus". You have always
wanted to go, so after the successful project launch from your monoid work, this was your opportunity. While in Hawaii,
you
run into Santa and Rudolph, and you all get to talking (while relaxing on the
beach, of course).

<img height="300" src="../assets/santa_elf_beach.jpg" width="300"/> 

(Art from Stable Diffusion)

Santa has some big ideas, and you pitched your own to the big guy. It turns out that in the past, Santa used to be a
lead engineer but put away his Engineering cap for the famous red one; his mind is still sharp as ever for these sorts
of problems, and he has some insights and ideas he asked to follow up on when you all get back from vacation.

On the sleigh ride back (first class, woo!), Santa says he'd like to eventually get the loss associated
with each IHM. Santa feels that
some children are trying to game the system where they'd act good at home but are bad outside; getting the IHM loss
would be a great first way to study this problem. You agree to spearhead this project and prototype it.

**Note** The code with [sol/functor_day_0.py](sol/functor_day_0.py) will not actually run. The goal was to just move it
over to act as a "starting" point for our development.

## MVP: Feb 1st

You step through your office door and just about get crushed by all the post-it notes and updates that have piled up.
You spot
two updates that catch your eye:

- **Data Elfgineers**: they have **finally** added the `UUID` to the IHM devices, which will make the lookups easy.
  Looks like we'll soon be able to determine which household all the gradients have come from. You shake your head in
  amazement that the compa... org has by for so long. Santa is touchy about people calling our organization a company...
  something about tax reasons?
    - **Request** the ability to add arbitrary data to the tracked objects and modify the existing data.

- **Data Scientists**: they want the ability to "bin" the UUIDs; this would make studying behavior easy: "we want all
  IHMs where the `key` is between `X` and `Y`".

We can assume that none of the IHMs will fail for the prototype. It's just easier to test it that way, but we will have
to come back to it later to fix it up.

### Tasklist

1) Get the UUIDs associated with each IHM
2) Expose a function, `map_func`, to add arbitrary data to the stored IHM data
3) Expose a function, `filter_on_key`, that allows you to filter arbitrary keys based on some bounds
4) Store the loss so that we can allow `filters`

### A Solution

See [sol/functor_day_1.py](sol/functor_day_1.py) for a possible solution. Note: our code here relies on probability
to show "correctness".

## Expanding the Requirements

So the data scientists are thrilled with the ability to look up the loss values, but they (rightfully) complained
that the lookup was far too slow, especially on large datasets. Sorting the data would be unbelievably painful, so could
you sort something out?

You kick back and think about how you could change it and realize that a quick binary-search tree where the key is the
loss. For the balancing, you decide to use an AVL tree implementation you found online
on [programiz](https://www.programiz.com/dsa/avl-tree).

### Tasklist

1) Modify the system to support a binary search tree. An implementation is provided
   in [sol/avl_tree_starter.py](sol/avl_tree_starter.py), which was modified
   for our problem.

#### Note For the Task

This is the most significant change we will see in this section on functors, so do try and follow along with the logic
in `day_2`. I'll mark out specific areas to note in the code.

### A solution

See [sol/functor_day_2.py](sol/functor_day_2.py) for a possible solution. Note: our code here relies on probability
to show "correctness".

## Day 3: Cleaning up our AVL tree

You managed to wrap up your code but weren't too happy with the results. The code looks messy, and your
pattern-matching spidey senses are going off. You decide to call the previous lead, the one who told you
about `monoids.`
and he says that he's been looking at `functors` lately, and they might help you. He said something about "abstracting
over containers," which you think would help.

### Functors

As I'm sure you already read in the [functors_101.md](notes/functors_101.md), a functor must
support, [at the minimum (according to Haskell)](https://wiki.haskell.org/Functor#Syntax), a `fmap`,
which describes how to apply an arbitrary function into the container in our class.

#### Further Discussion

See [functors_101.md](functors_101.md) for a more in-depth discussion on functors and their definition, but TL;DR, by
using functors, we can
abstract over "containers" or "structures". Functors and monads provide some tools to operate on a wrapped input.

Compare and contrast how easily we could use a `map` and `filter` on our original code from `sol/functor_day_1.py` and
our code from `sol/functor_day_3_cleanup.py`. The `list` structure
felt natural to think about lists where we can iterate. Still, we see that we could also define a way to map functions
over our `AVLTree` in a manner that makes sense.

### Tasklist

Clean up the code from `sol/functor_day_2.py` and `sol/avl_tree_starter.py` and transform them
into `sol/functor_day_3.py` and `sol/avl_tree_functor.py`

## Closing out

### Improvements: Data Structure

If you're looking to refresh your data-structure chops, you can take a look at
our [avl_tree_functor.py](sol/avl_tree_functor.py) implementation. Currently,
it crashes if we have multiple of the same key, but I see no reason why it should. After all, multiple `IHMResult`s can
have the same loss (even if it is unlikely). In fact, if you bump up `num_ihms = np.random.randint(10)` to be something like `1_000` you'll probably see what I mean.

### Additional work

We described a `functor` over the `ihm_results = simulate_ihm(num_ihms, prob_ihm_crash, NUM_FEATURES)` but we could have also defined it over
the individual `IHMResult`, which would allow for another level of abstraction (which is very cool).

### What IS and isn't a functor?

In theory, a functor is more than "just" a container, it just describes a structure of how to apply functions. Given Haskell's nature, a function 
is also a functor. Continuing that discussion, are the following functors?

- `Binary Search Tree`
- `Dictionary`
- `Set`
- `String`

See [notes/what is and isnt a functor solutions](notes/what_is_isnt_functor_solutions.md)