# Monoids

Coming off the brief discussion in [README - day 4 monoids](README.md#day-4--monoids), a Monoid is a structure that
satisfies two properties:

1) binary associative operation: (A + B) + C == A + (B + C)
2) Has an identity element such that (A + id) = A

These monoids form what is known as a semigroup and are extremely useful in both mathematics and programming. In
particular, monoids provide us, programmers, with a way of cleanly abstracting the coding logic; we can hide all the
details of what happens when we do `A operator B` from our end-users while providing them an easy interface to extend
the code. This ability to hide the details makes the monoid
a valuable structure for many problems, particularly in scenarios such as map-reduces. All this is to say that we have a
reduced
cognitive load, which is nice.
