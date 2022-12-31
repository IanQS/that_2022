"""
Please read the entire file if possible
"""
from typing import List, Callable, Optional, Union, Tuple

import numpy as np
from dataclasses import dataclass
import uuid
from .avl_tree_0 import AVLTree, _TreeNode


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> Tuple[AVLTree, List]:
    avl_tree = AVLTree()
    failures = []
    for i in range(num_ihms):
        if np.random.random() < prob_ihm_crash:
            failures.append(ihm_failure())
        else:
            ihm = ihm_success(num_features)
            avl_tree.insert_node(key=ihm.loss, ihm_data=ihm)
    return avl_tree, failures


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
