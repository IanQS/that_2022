"""
Our starting code
"""
from typing import List, Optional, TypeVar, Dict, Any

import numpy as np

Result = TypeVar("Result")


def ihm_success(num_features) -> Result:
    return np.random.rand((num_features))


def ihm_failure():
    return None


def tsp_processor(ihm_results) -> Dict[str, Any]:
    accumulated_gradient = None
    if not ihm_results:
        return {"No successes :( Try running this again": None}
    num_houses_queried = 0
    for i, result in enumerate(ihm_results):
        num_houses_queried += 1
        if result is None:  # Our machine crashed (error calculating gradient, networking issue, etc.) We'll come back to this
            continue
        curr_grad = result
        if accumulated_gradient is None:
            accumulated_gradient = curr_grad
        else:
            accumulated_gradient += curr_grad
    return {
        "Accumulated Gradients": accumulated_gradient,
        "Num Houses Queried": num_houses_queried
    }

