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


def tsp_processor(ihm_results: List[IHMResult]) -> Dict[str, Any]:
    if not ihm_results:
        return {"No successes :( Try running this again": None}

    accumulated_gradient = None
    accumulated_sq_gradient = None
    accumulated_time_taken = 0
    accumulated_sq_time_taken = 0

    total_houses_queried = 0
    num_failures = 0
    total_time = 0

    fastest_ihm, fastest_ihm_idx = -float("inf"), None
    slowest_ihm, slowest_ihm_idx = float("inf"), None
    for i, single_ihm in enumerate(ihm_results):
        total_houses_queried += 1
        if single_ihm is None:
            num_failures += 1
            continue

        if accumulated_gradient is None:
            accumulated_gradient = single_ihm.gradients
            accumulated_sq_gradient = single_ihm.gradients ** 2
        else:
            accumulated_gradient += single_ihm.gradients
            accumulated_sq_gradient += (single_ihm.gradients ** 2)
        total_time += single_ihm.time_taken

        ################################################
        # Find the fastest and slowest IHM
        ################################################
        if single_ihm.time_taken > fastest_ihm:
            fastest_ihm = single_ihm.time_taken
            fastest_ihm_idx = i
        if single_ihm.time_taken < slowest_ihm:
            slowest_ihm = single_ihm.time_taken
            slowest_ihm_idx = i

        ################################################
        # Find the variance of the IHM times
        ################################################
        accumulated_time_taken += single_ihm.time_taken
        accumulated_sq_time_taken += (single_ihm.time_taken ** 2)

    ################################################
    # Prevent division by 0
    ################################################

    if (total_houses_queried - num_failures) == 0:
        ave_time = "NaN "
        variance_grad = None
        variance_time = None
    else:
        ave_time = total_time / (total_houses_queried - num_failures)
        num_valid_ihms = total_houses_queried - num_failures
        variance_grad = (accumulated_sq_gradient / num_valid_ihms) - \
                        (accumulated_gradient / num_valid_ihms) ** 2
        variance_time = (accumulated_sq_time_taken / num_valid_ihms) - \
                        (accumulated_time_taken / num_valid_ihms) ** 2

    return {
        "Accumulated Gradient": accumulated_gradient,
        "Average Time Taken": ave_time,
        "Num IHMs Failed": num_failures,
        "Slowest time and IHM idx": (slowest_ihm, slowest_ihm_idx),
        "Fastest time and IHM idx": (fastest_ihm, fastest_ihm_idx),
        "Gradient Variance": variance_grad,
        "Time Variance": variance_time,
        "Num IHMs Success": total_houses_queried - num_failures
    }
