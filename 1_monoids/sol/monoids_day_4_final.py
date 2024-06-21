"""
The requests:

1) find the fastest and slowest IHMs (to fix up the connection/ bump up the hardware)
2) find the variance of the gradients and time taken to calculate the gradients
"""

from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np


@dataclass
class IHMResult:
    time_taken: np.float_
    gradients: np.ndarray

    def __post_init__(self):
        self.accumulated_gradient = self.gradients
        self.accumulated_sq_gradient = self.accumulated_gradient ** 2
        self.accumulated_time_taken = self.time_taken
        self.accumulated_sq_time_taken = self.time_taken ** 2

        self.total_houses_queried = 1
        self.num_failures = 0
        self.fastest_ihm = self.time_taken
        self.slowest_ihm = self.time_taken

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

    def as_str(self):
        return {
            "Accumulated Gradient": self.accumulated_gradient,
            "Average Time Taken": self.average_time,
            "Num IHMs Failed": self.num_failures,
            "Slowest time": self.slowest_ihm,
            "Fastest time": self.fastest_ihm,
            "Gradient Variance": self.variance_grad,
            "Time Variance": self.variance_time,
            "Num IHMs Success": self.num_succeeded
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
        to_return = cls(-1, 0)
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
        return self


def ihm_success(num_features) -> IHMResult:
    time_taken = np.random.rand()
    gradients = np.random.rand(num_features)
    return IHMResult(time_taken * 10, gradients)


def ihm_failure() -> IHMResult:
    to_return = IHMResult.make_empty()
    to_return.total_houses_queried = 1
    to_return.num_failures = 1
    return to_return


def tsp_processor(ihm_results: List[IHMResult]) -> Dict[str, Any]:
    if not ihm_results:
        return {"No successes :( Try running this again": None}
    reducer = IHMResult.make_empty()
    for i, single_ihm in enumerate(ihm_results):
        reducer += single_ihm
    return reducer.as_str()