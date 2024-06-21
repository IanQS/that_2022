- `Binary Search Tree` Yes! It is a functor. Look at the type signature
- `Dictionary`: Yes, it is!
- `Set`: No, they are not! The reason is
  that [a set must be order-able](https://www.reddit.com/r/haskell/comments/2090x3/ask_rhaskell_why_is_there_no_functor_instance_for/).
  Having said that, we don't actually need to care for most practical purposes and we can define a map over the
  structure.
- `String`: No, it is not! This is because a functor has the following structure

```haskell
class Functor Func where
    fmap :: (T1 -> T2) -> Func T1 -> Func T2
    (<$) :: T1 -> Func T2 -> Func T1
```

However, a `String` imposes the requirement that `T1` be a type of `List[char]`, thus it cannot be an "abstract" type.
However, as in the case of a `Set`, just because it is theoretically NOT a functor (depending on the language), it
doesn't stop us from defining an `fmap` over it.

[Back to the main readme](../README.md)