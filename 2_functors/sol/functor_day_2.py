"""
Please read the entire file if possible

1) Modify the system to support a binary search tree. An implementation is provided in `avl_tree.py`, which was modified
   for our problem.
"""
import uuid
from dataclasses import dataclass
from typing import List, Callable, Any

import numpy as np

from .avl_tree_starter import AVLTree, _TreeNode


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> AVLTree:
    """
    NOTE: see how the original code is almost the same as in our modified form

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
    seen = []
    for i in range(num_ihms):
        if np.random.random() < prob_ihm_crash:
            failures.append(ihm_failure())
        else:
            ihm = ihm_success(num_features)
            seen.append(ihm.loss)
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
            modified_data: IHMResult = func_to_map(
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
            ihm_data: IHMResult = curr_node.ihm_data
            if func_to_filter_with(ihm_data):
                new_tree.insert_node(
                    ihm_data.loss,
                    ihm_data=ihm_data
                )
            horizon.append(curr_node.left)
            horizon.append(curr_node.right)

    return new_tree


################################################
# Unchanged below
################################################


@dataclass
class IHMResult:
    time_taken: np.float_
    gradients: np.ndarray
    loss: np.float_  # Requirement 4
    ihm_uuid: str = ""  # Requirement 1

    def __post_init__(self):
        self.accumulated_gradient = self.gradients
        self.accumulated_sq_gradient = self.accumulated_gradient ** 2
        self.accumulated_time_taken = self.time_taken
        self.accumulated_sq_time_taken = self.time_taken ** 2
        self.accumulated_loss = self.loss
        self.accumulated_sq_loss = self.accumulated_loss ** 2

        self.total_houses_queried = 1
        self.num_failures = 0
        self.fastest_ihm = self.time_taken
        self.slowest_ihm = self.time_taken
        if self.ihm_uuid:
            self.ihm_uuid = [self.ihm_uuid]
        else:
            self.ihm_uuid = []

    @property
    def num_succeeded(self):
        return self.total_houses_queried - self.num_failures

    @property
    def average_time(self) -> np.ndarray:
        if self.num_succeeded == 0:
            return np.nan
        num_valid_ihms = self.num_succeeded
        ave_time = self.accumulated_time_taken / num_valid_ihms
        return np.asarray(ave_time)

    @property
    def average_loss(self) -> np.ndarray:
        if self.num_succeeded == 0:
            return np.nan
        num_valid_ihms = self.num_succeeded
        ave_loss = self.accumulated_loss / num_valid_ihms
        return np.asarray(ave_loss)

    @property
    def variance_grad(self) -> np.ndarray:
        if self.num_succeeded == 0:
            return np.nan
        var_grad = (self.accumulated_sq_gradient / self.num_succeeded) - \
                   (self.accumulated_gradient / self.num_succeeded) ** 2
        return np.asarray(var_grad)

    @property
    def variance_time(self) -> np.ndarray:
        if self.num_succeeded == 0:
            return np.nan
        var_time = (self.accumulated_sq_time_taken / self.num_succeeded) - \
                   (self.accumulated_time_taken / self.num_succeeded) ** 2
        return np.asarray(var_time)

    @property
    def variance_loss(self) -> np.ndarray:
        if self.num_succeeded == 0:
            return np.nan
        var_loss = (self.accumulated_sq_loss / self.num_succeeded) - \
                   (self.accumulated_loss / self.num_succeeded) ** 2
        return np.asarray(var_loss)

    def as_str(self):
        return {
            "Accumulated Gradient": self.accumulated_gradient,
            "Average Time Taken": self.average_time,
            "Num IHMs Failed": self.num_failures,
            "Slowest time": self.slowest_ihm,
            "Fastest time": self.fastest_ihm,
            "Gradient Variance": self.variance_grad,
            "Time Variance": self.variance_time,
            "Num IHMs Success": self.num_succeeded,
            "UUID": self.ihm_uuid,
            "Average Loss": self.average_loss,
            "Loss Variance": self.variance_loss
        }

    ################################################
    # Monoid methods
    ################################################

    @classmethod
    def make_empty(cls):
        """
        For completeness, we set all the fields that were set in the
            __post_init__. Mostly so users don't need to scroll up
            to see what fields were set.
        """
        to_return = cls(-1, 0, 0)
        to_return.time_taken = np.inf
        to_return.gradients = 0  # Was set correctly already

        # Just for completeness
        to_return.accumulated_gradient = 0
        to_return.accumulated_sq_gradient = 0

        to_return.accumulated_time_taken = 0
        to_return.accumulated_sq_time_taken = 0

        to_return.total_houses_queried = 0
        to_return.num_failures = 0

        to_return.fastest_ihm = np.inf
        to_return.slowest_ihm = -np.inf
        to_return.ihm_uuid = []
        return to_return

    def __add__(self, other: Any):
        """
        Doing an in-place update. Because we are doing a reduce, we don't really care about
            maintaining the original data (which is presumably just GC-ed)
        """
        if not isinstance(other, IHMResult):
            raise Exception(f"Attempting to add IHMResult and {type(other)}")
        other: IHMResult
        self.total_houses_queried += other.total_houses_queried
        self.num_failures += other.num_failures

        self.accumulated_gradient += other.accumulated_gradient
        self.accumulated_sq_gradient += other.accumulated_sq_gradient

        self.fastest_ihm = min(self.fastest_ihm, other.fastest_ihm)
        self.slowest_ihm = max(self.slowest_ihm, other.slowest_ihm)

        self.accumulated_time_taken += other.accumulated_time_taken
        self.accumulated_sq_time_taken += other.accumulated_sq_time_taken
        self.ihm_uuid += other.ihm_uuid

        self.accumulated_loss += other.accumulated_loss
        self.accumulated_sq_loss += other.accumulated_sq_loss
        self.loss += other.loss
        return self


def ihm_success(num_features) -> IHMResult:
    time_taken = np.random.rand()
    gradients = np.random.rand(num_features)
    ihm_uuid = str(uuid.uuid4())  # TASK 1
    loss = np.random.randint(1, 100) / 100  # Task 4
    return IHMResult(time_taken * 10, gradients, loss, ihm_uuid)


def ihm_failure() -> IHMResult:
    to_return = IHMResult.make_empty()
    to_return.total_houses_queried = 1
    to_return.num_failures = 1
    return to_return
