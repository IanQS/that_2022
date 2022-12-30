"""
Please read the entire file if possible
"""
from typing import List, Callable, Optional, Union

import numpy as np
from dataclasses import dataclass
import uuid
from .avl_tree_functor import AVLTree, _TreeNode


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> AVLTree:
    failures = []
    avl_tree = AVLTree()
    for i in range(num_ihms):
        if np.random.random() < prob_ihm_crash:
            failures.append(ihm_failure())
        else:
            ihm = ihm_success(num_features)
            avl_tree.insert_node(key=ihm.loss, ihm_data=ihm)
    return avl_tree


def map_func(avl_tree: AVLTree, func_to_map: Callable):
    """
    Original Code:
    return list(map(func_to_map, ihm_list))
    """
    return avl_tree.map(func_to_map)

def filter_by_func(avl_tree: AVLTree, func_to_filter_with: Callable):
    """
    Original Code:
    return list(filter(func_to_map, ihm_list))
    """
    return avl_tree.filter(func_to_filter_with)

################################################
# Ignore below
################################################

@dataclass
class IHM:
    gradient: np.ndarray
    time_taken: np.ndarray
    ihm_uuid: str
    loss: np.ndarray


def ihm_success(num_features: int):
    time_taken = np.random.rand()
    gradient = np.random.rand(num_features)
    ihm_uuid = str(uuid.uuid4())
    loss = np.random.randint(1, 100) / 100
    return IHM(gradient, time_taken * 10, ihm_uuid, loss)


def ihm_failure():
    return None


def prototype(num_ihms: int, crash_proba: float, num_features: int):
    import copy
    def func_to_map(ihm: IHM, key: str) -> IHM:
        new_x = copy.deepcopy(ihm)
        setattr(new_x, key, np.random.choice([True, False]))
        return new_x

    def func_to_filter(ihm: IHM) -> bool:
        return ihm.keep

    avl_tree_res = simulate_ihm(num_ihms, crash_proba, num_features)
    print(f"Length of original: {len(avl_tree_res)}")
    mapped_over = map_func(avl_tree_res, lambda x: func_to_map(x, "keep"))
    filtered_out = filter_by_func(mapped_over, lambda x: func_to_filter(x))
    print(f"Length of filtered: {len(filtered_out)}")

    print("Testing Composition")

    def f(ihm: IHM):
        print("Called f")
        ihm.gradient = 0
        return ihm
    def g(ihm: IHM):
        print("Called g")
        ihm.loss += 100
        return ihm

    def f_of_g(ihm: IHM):
        print("Called fog")
        return f(g(ihm))

    avl_tree_res = simulate_ihm(2, crash_proba, num_features)
    r1 = avl_tree_res.map(g)
    r2 = r1.map(f)
    r3 = avl_tree_res.map(f_of_g)
    print("Place debugger at this line")