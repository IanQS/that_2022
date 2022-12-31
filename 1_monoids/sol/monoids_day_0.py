"""
Our starting code
"""
from typing import List, Optional, TypeVar

import numpy as np

Result = TypeVar("Result")


def ihm_success(num_features) -> Result:
    return np.random.rand((num_features))


def ihm_failure():
    return None


def mdc_failure():
    return None


def mdc_processor(ihm_results):
    accumulated_gradient = None
    if not ihm_results:
        return None
    for i, result in enumerate(ihm_results):
        if result is None:  # Our machine crashed (error calculating gradient, networking issue, etc.) We'll come back to this
            continue
        curr_grad = result
        if accumulated_gradient is None:
            accumulated_gradient = curr_grad
        else:
            accumulated_gradient += curr_grad
    return accumulated_gradient


def npdc_processor(mdc_result_list: List[Optional[Result]]):
    accumulated_gradient = None
    if not mdc_result_list:
        return None
    for mdc_result in mdc_result_list:
        if mdc_result is None:
            continue
        curr_grad = mdc_result
        if accumulated_gradient is None:
            accumulated_gradient = curr_grad
        else:
            accumulated_gradient += curr_grad

    to_return = {
        "accum_grad": accumulated_gradient,
    }
    return to_return
