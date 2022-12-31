"""
Please read the entire file if possible
"""
import uuid
from dataclasses import dataclass
from typing import List, Callable

import numpy as np

from .avl_tree_starter import AVLTree, _TreeNode


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> AVLTree:
    """
    Original Code:

    ihm_results = []
    for i in range(num_ihms):
        if np.random.random() < prob_ihm_crash:
            ihm_results.append(ihm_failure())
        else:
            ihm_results.append(ihm_success(num_features))
    return ihm_results
    """

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
    horizon: List[_TreeNode] = [avl_tree._root]
    new_tree = AVLTree()
    while horizon:
        curr_node: _TreeNode = horizon.pop()
        if curr_node:
            modified_data: IHM = func_to_map(
                # We pass in the IHM data because we don't
                # want the user to have any notion of "What" our data container is i.e
                # if it's a Node in a tree structure, an index in a list, etc.
                # All the user needs to know is that they can map over IHM data
                curr_node.ihm_data
            )
            new_tree.insert_node(modified_data.loss, modified_data)
            horizon.append(curr_node.left)
            horizon.append(curr_node.right)

    return new_tree


def filter_by_func(avl_tree: AVLTree, func_to_filter_with: Callable):
    """
    Original Code:

    return list(filter(func_to_filter_with, ihm_list))
    """

    horizon: List[_TreeNode] = [avl_tree._root]
    new_tree = AVLTree()
    while horizon:
        curr_node: _TreeNode = horizon.pop()
        if curr_node:
            ihm_data: IHM = curr_node.ihm_data
            if func_to_filter_with(ihm_data):
                new_tree.insert_node(
                    ihm_data.loss,
                    ihm_data=ihm_data
                )
            horizon.append(curr_node.left)
            horizon.append(curr_node.right)

    return new_tree


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

    ihm_results = simulate_ihm(num_ihms, crash_proba, num_features)
    print(f"Length of original: {len(ihm_results)}")
    mapped_over = map_func(ihm_results, lambda x: func_to_map(x, "keep"))
    filtered_out = filter_by_func(mapped_over, lambda x: func_to_filter(x))
    print(f"Length of filtered: {len(filtered_out)}")
