# Monoids

Coming off the brief discussion in [README - day 4 monoids](README.md#day-4--monoids), a Monoid is a structure that
satisfies three properties:

1) binary associative operation: (A + B) + C == A + (B + C)
2) Has an identity element such that (A + id) = A

and we see that this makes the monoid structure useful for many problems, particularly in scenarios such as map-reduces.
What makes them so nice
in programming is that they are a nice way to encapsulate the idea of computation. It lets us abstract away a lot of the
underlying structure and tell the other end to "just handle it" and this can be extremely freeing. We have a reduced
cognitive load, which is nice.