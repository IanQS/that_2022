"""
The requests:

1) the average gradient calculation time of the IHMs (each one now reports the time taken)
2) how many IHMs failed in their gradient collection
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
    total_houses_queried = 0
    num_failures = 0
    total_time = 0
    for i, single_ihm in enumerate(ihm_results):
        total_houses_queried += 1
        if single_ihm is None:
            num_failures += 1
            continue
        if accumulated_gradient is None:
            accumulated_gradient = single_ihm.gradients
        else:
            accumulated_gradient += single_ihm.gradients
        total_time += single_ihm.time_taken

    ################################################
    # Prevent division by 0
    ################################################

    if (total_houses_queried - num_failures) == 0:
        ave_time = "NaN "
    else:
        ave_time = total_time / (total_houses_queried - num_failures)
    return {
        "Accumulated Gradient": accumulated_gradient,
        "Average Time Taken": ave_time,
        "Num IHMs Failed": num_failures,
        "Num IHMs Success": total_houses_queried - num_failures
    }
