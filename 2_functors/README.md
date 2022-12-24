# Scenario

After your big project, you manage to sneak off to Hawaii for a bit. You've been watching "White Lotus" and have always
wanted to go so after the successful project launch from your monoid work, this was your opportunity. While there you
run into Santa and Rudolph and you all get to talking (while relaxing on the
beach, of course).

<img height="300" src="../assets/santa_elf_beach.jpg" width="300"/>

Santa has some big ideas and you pitched your own to the big guy. It turns out that in the past, Santa used to be a
lead engineer but put away his Engineering cap for the famous red one; his mind is still sharp as ever for these sorts
of problems and he has some insights and ideas he asked to follow up on when back from vacation.

On the sleigh ride back (first class, woo!), Santa says that he'd like to eventually be able to get the loss associated
with each IHM - he's got a feeling that
some children are trying to game the system where they'd act good at home, but are bad outside; getting the IHM loss
would be a great first way to study this problem. You agree to spearhead this project and prototype it.

## Day 1

You decide to start with a small problem - your goal is to "intercept" the data at the `MPDC` level and accumulate the
results there. You decide to gather requirements and talk to the various teams:

- **Data Elfgineers**: they have **finally** added the `uuid` to the IHM results, which will make the lookups easy. They
  asked for the ability to add arbitrary data to the tracked objects, as well as modify the existing data.

- **Data Scientists**: they want the ability to "bin" the UUIDs, which would make studying behavior useful down the
  road. "we want all IHMs where the `key` is between `X` and `Y`".

For the prototype, we can assume that none of the IHMs will fail. It's just easier to test it that way, but we will have
to come back to it later to fix it up.

### Tasklist

1) Get the UUIDs associated with each IHM
2) Expose a function, `map_func`, to add arbitrary data to the stored IHM data
3) Expose a function, `filter_on_key`, that allows you to filter arbitrary keys based on some bounds

### A Solution

`functors_day_1.py` and `functor_driver.py` where we changed the code to include a sample

## Day 2

So the data scientists are really happy with the ability to look up the loss values but they (rightfully) complained
that the lookup was far too slow especially on large datasets. Sorting the data would be unbelievably painful so could
you sort something out?

You kick back and think about how you could change it and realize that a quick binary-search tree where the key is the
loss. For the balancing you decide to use an AVL tree implementation you found online
on [programiz](https://www.programiz.com/dsa/avl-tree).

### Tasklist

1) Modify the system to support a binary search tree. An implementation is provided in `avl_tree.py` which was modified
   for our problem.

**Note** This is the biggest change we will see in this section on functors so do try and follow along with the logic
in `day_2`. I'll mark out specific areas to take note of in the code itself.

### A solution

`functors_day_2.py`

We create a new data-structure that will accompany our MDC_Monoid. Thankfully, we can use this to quickly look up the
appropriate values. Please read the comments at the top of the file and just the entire file overall.

## Day 3: Cleaning up our AVL tree

You managed to wrap up your code, but you weren't too happy with the results. The code looks messy and your
patter-matching spidey-senses are going off. You decide to call the previous lead, the one who told you about `monoids`
and he says that he's been looking at `functors` lately, and they might help you. He said something about "abstracting
over containers" and you sort of zoned out.

### Discussion

See [functors_101.md](functors_101.md) for a more in-depth discussion on functors and their definition but TL;DR by
using functors, we can
abstract over "containers" or "structures".

Compare and constrast how easily we could use a `map` and `filter` on our original code from `day_1.py`. The structure
felt very natural to how we think about lists where we can iterate through them.

When it came to our `AVLTree`, we see that there is a valid implementation of `map` and `filter` too. By defining how to
traverse our structure and apply functions, we were able to implement an abstract `map` and `filter` ignoring the
underlying data-structure. As far as the end-user is concerned, the implementation might as well have been a list.

And that's really the power of a functor - it lets us abstract over containers of **things**.

### Tasklist

Clean up the code from `day_2` and `avl_tree_starter.py` and transform them into `day_3` and `avl_tree_functor.py`

## Closing out

Earlier we mentioned that we were prototyping

> For the prototype, we can assume that none of the IHMs will fail. It's just easier to test it that way, but we will
> have
> to come back to it later to fix it up.

but now that we're past that hurdle, we've reached a point where we need to handle the `None` values that might get
returned. Although Python has nice syntax for handling `None`, I'll introduce the following idea: `Maybe` where it
encapsulates the idea of a "This-might-be-something" and if it is not, then it is "Nothing". See
how [Rust](https://doc.rust-lang.org/std/option/) handles optional values.