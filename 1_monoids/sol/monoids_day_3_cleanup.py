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


def ihm_success(num_features) -> IHMResult:
    time_taken = np.random.rand()
    gradients = np.random.rand(num_features)
    return IHMResult(time_taken * 10, gradients)


def ihm_failure():
    return None

class ReduceTracker():
    def __init__(self):
        self.accumulated_gradient = None
        self.accumulated_sq_gradient = None
        self.accumulated_time_taken = 0
        self.accumulated_sq_time_taken = 0

        self.total_houses_queried = 0
        self.num_failures = 0

        self.fastest_ihm, self.fastest_ihm_idx = float("inf"), None
        self.slowest_ihm, self.slowest_ihm_idx = -float("inf"), None

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

    ################################################
    # Prevent division by 0
    ################################################

    def as_str(self):

        return {
            "Accumulated Gradient": self.accumulated_gradient,
            "Average Time Taken": self.average_time,
            "Num IHMs Failed": self.num_failures,
            "Slowest time and IHM idx": (self.slowest_ihm, self.slowest_ihm_idx),
            "Fastest time and IHM idx": (self.fastest_ihm, self.fastest_ihm_idx),
            "Gradient Variance": self.variance_grad,
            "Time Variance": self.variance_time,
            "Num IHMs Success": self.num_succeeded
        }


def tsp_processor(ihm_results: List[IHMResult]) -> Dict[str, Any]:
    if not ihm_results:
        return {"No successes :( Try running this again": None}
    tracker = ReduceTracker()
    for i, single_ihm in enumerate(ihm_results):
        tracker.total_houses_queried += 1
        if single_ihm is None:
            tracker.num_failures += 1
            continue

        if tracker.accumulated_gradient is None:
            tracker.accumulated_gradient = single_ihm.gradients
            tracker.accumulated_sq_gradient = single_ihm.gradients ** 2
        else:
            tracker.accumulated_gradient += single_ihm.gradients
            tracker.accumulated_sq_gradient += (single_ihm.gradients ** 2)

        ################################################
        # Find the fastest and slowest IHM
        ################################################
        if single_ihm.time_taken < tracker.fastest_ihm:
            tracker.fastest_ihm = single_ihm.time_taken
            tracker.fastest_ihm_idx = i
        if single_ihm.time_taken > tracker.slowest_ihm:
            tracker.slowest_ihm = single_ihm.time_taken
            tracker.slowest_ihm_idx = i

        ################################################
        # Find the variance of the IHM times
        ################################################
        tracker.accumulated_time_taken += single_ihm.time_taken
        tracker.accumulated_sq_time_taken += (single_ihm.time_taken ** 2)

    return tracker.as_str()