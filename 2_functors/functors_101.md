# Functors

As mentioned before, the power of functors is that it allows for abstraction; we do not and SHOULD NOT need to care
about underlying
implementations. Our code should work with a list of `IHM`s, or any other data structure that the devs swap it out for.
This way,
we, the end user, can squint and be sure that our code will always work.

## A Reminder

This [excellent answer](https://stackoverflow.com/a/56601178/3532564) describes, at a very high level, `functors`
and `monads`

`functors` and `monads` both provide some tool to wrapped input, returning a wrapped output.

- `functor` = map (i.e. the tool)

- `monad` = unit + flatMap (or bind or chain)

## Functor Syntax:

As Haskell is the best reference for these concepts, we introduce the two syntax requirements put forth there. The
following can be found from the [Haskell Functor Wiki](https://wiki.haskell.org/Functor) but I've restated it here in a
format that is more familiar to non-Haskellers

```haskel
class Functor Func where
    fmap :: (a -> b) -> Func a -> Func b
    (<$) :: a -> Func b -> Func a
```

### The fmap:

`fmap` is essentially what we did in our `avl_tree_functor.py` code

```python
def map(self, func_to_map: Callable):
    horizon: List[_TreeNode] = [self._root]
    new_tree = AVLTree()
    while horizon:
        curr_node: _TreeNode = horizon.pop()
        if curr_node:
            modified_data = func_to_map(
                curr_node.ihm_data
            )
            new_tree.insert_node(
                modified_data.loss,
                modified_data
            )
            horizon.append(curr_node.left)
            horizon.append(curr_node.right)

    return new_tree
```

where we exposed a `map` that described how to traverse the nodes in the `AVLTree` and apply the function to the values
within it. Restating the haskell rules in `AVLTree` and our code as is in `functor_dat_3_cleanup`

```haskell
class Functor AVLTree where
    fmap :: (IHM -> IHM) -> AVLTree IHM -> AVLTree IHM
```

Although it would be perfectly valid to change around the underlying type to be `(IHM -> X)`

### Syntax Req 2: `(<$)`

This syntax is less important as you're very unlikely to need it, but you can read
through [serokell.io](https://serokell.io/blog/whats-that-typeclass-functor#the-(<%24)-operator)the idea of it is the
following:

## Laws:

To be a functor, two laws must be satisfied:

```
1) identity transformations must be preserved
2) fmap (f . g)  ==  fmap f . fmap g (composition must be respected)
```

If you open up your debugger and place your debugger on the appropriate line of `functor_day_3_cleanup.py` you'll see
that the composition is respected. 