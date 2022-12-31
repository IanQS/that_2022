"""
Please read the entire file if possible
"""
from typing import List, Callable, Optional, Union

import numpy as np
from dataclasses import dataclass
import uuid
from .avl_tree_1 import AVLTree, _TreeNode


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> AVLTree:
    avl_tree = AVLTree()
    failure_count = 1
    for i in range(num_ihms):
        if np.random.random() < prob_ihm_crash:
            maybe_ihm = OptionalIHM(ihm_failure())
            loss = -failure_count
            failure_count+=1
        else:
            maybe_ihm = OptionalIHM(ihm_success(num_features))
            loss = maybe_ihm.ihm_data.loss
        avl_tree.insert_node(key=loss, ihm_data=maybe_ihm)
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

    def __repr__(self):
        return f"UUID: {self.ihm_uuid}\n\t-Gradient: {self.gradient}\n\t-Time Taken: {self.time_taken}\n\t-Loss: {self.loss}"


class OptionalIHM:
    def __init__(self, ihm_data: Optional[IHM] = None):
        self.ihm_data = ihm_data

    def bind(self, callable_func: Callable[[IHM], IHM]) -> "OptionalIHM":
        if self.ihm_data is None:
            return OptionalIHM(self.ihm_data)
        return OptionalIHM(callable_func(self.ihm_data))

    def __repr__(self):
        if self.ihm_data is None:
            return "None"
        return f"Some({self.ihm_data})"

    def __str__(self):
        return self.__repr__()


def ihm_success(num_features: int):
    time_taken = np.random.rand()
    gradient = np.random.rand(num_features)
    ihm_uuid = str(uuid.uuid4())
    loss = np.random.randint(1, 100) / 100
    return IHM(gradient, time_taken * 10, ihm_uuid, loss)


def ihm_failure():
    return None
