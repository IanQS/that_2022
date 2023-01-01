# Functors

## Requirements and Laws

### Requirements

As mentioned in the [README.md](README.md),

> A functor must support, [at the minimum, according to Haskell, ](https://wiki.haskell.org/Functor#Syntax), a `fmap`,
which describes applying an arbitrary function into the function encapsulated in our class.

### Laws:

[Lookin at the Haskell documentation once again](https://wiki.haskell.org/Functor#Functor_Laws), to be a functor, two
laws must be satisfied:

```
1) identity transformations must be preserved
2) fmap (f . g)  ==  fmap f . fmap g (composition must be respected)
```

## Definition

As in the Haskell documentation (we ignore the `<$` operation), we must define a `fmap.` Note: we modify the definition,
which typically uses `f` to denote the functor, which can be confusing if you're not used to the syntax.

```
class Functor AVLTree where
    fmap :: (a -> b) -> AVLTree a -> AVLTree b
```

And we see how we take in an arbitrary function (transforming some type `a' into type `b`) and apply it to the value
stored in our functor. Note how the function operates on the raw un-functor-ed value and outputs the same.

## Our Code Interface

Look at our `List` used in `sol/functor_day_1.py`: our `List` has an implementation of a `map` that we are familiar
with. Then, look at our `AVLTree` in `sol/functor_day_3_cleanup.py`; we can define a `map` for our `AVLTree`. By
describing how to
traverse our `AVLTree` and apply functions, we could `map` functions over our `AVLTree`, just like our `List`

## Who Gives a Functor?

And that's the power of a functor - it lets us abstract over containers of things; they let us "swap" out the
underlying "backend". As far as the end-user is concerned, the implementation could have been a list (or a
Red-Black-Tree, or some optimized list-like structure).

The end-user SHOULD NOT need to care
about underlying
implementations. As long as our end-user uses code that "obeys" our requirements (function signatures), they do not need
to care about how we do things in the background. For example, see how in `sol/functor_day_1.py`, our implementation
was "hardwired" to a `List` because of our `map_func` and our `simulate_ihm`?

```
def map_func(ihm_list: List[IHM], func_to_map: Callable):  # Task 2
    return list(map(func_to_map, ihm_list))

# AND

def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> List:
    ihm_results = []
    for i in range(num_ihms):
        if np.random.random() < prob_ihm_crash:
            ihm_results.append(ihm_failure())
        else:
            ihm_results.append(ihm_success(num_features))
    return ihm_results
```

## Our Implementation

In our `sol/avl_tree_functor.py` code, we defined an `fmap.`

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

We described traversing the nodes in the `AVLTree` and applying the function to its values. Based on our code
from `sol/functor_day_3_cleanup.py`, we restate our [earlier discussed class definition](#definition) in terms
of `AVLTree` and `IHM`

```
class Functor AVLTree where
    fmap :: (IHM -> IHM) -> AVLTree IHM -> AVLTree IHM

# But really our code should work with any `a` and `b`
```

If you open up your debugger and place your debugger on the appropriate line of `prototype`
in `sol/functor_day_3_cleanup.py` you'll see
that the composition is respected. 
