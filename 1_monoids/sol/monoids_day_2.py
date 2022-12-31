"""
The requests:

1) find the fastest and slowest MDCs (to fix up the connection/ bump up the hardware)
2) find the variance of grads for both the IHMs and the MDCs
"""

from typing import List, Optional, TypeVar

import numpy as np

Result = TypeVar("Result")


def ihm_success(num_features) -> Result:
    time_taken = np.random.rand()
    gradients = np.random.rand(num_features)
    return gradients, time_taken * 10


def ihm_failure():
    return None


def mdc_failure():
    return None


def mdc_processor(ihm_results):
    if not ihm_results:
        return None
    accumulated_gradient = None
    accumulated_sq_gradient = None
    num_valids = 0
    ihm_time_tracker = []
    counter = 0

    for i, result in enumerate(ihm_results):
        if result is None:
            continue
        num_valids += 1
        counter += 1
        curr_grad, curr_time = result
        if accumulated_gradient is None:
            accumulated_gradient = curr_grad
            accumulated_sq_gradient = curr_grad ** 2
        else:
            accumulated_gradient += curr_grad
            accumulated_sq_gradient += (curr_grad ** 2)
        ihm_time_tracker.append(curr_time)
    num_houses_serviced = len(ihm_results)
    num_IHMs_failed = num_houses_serviced - num_valids
    return accumulated_gradient, accumulated_sq_gradient, \
        num_houses_serviced, num_IHMs_failed, \
        ihm_time_tracker


def npdc_processor(mdc_result_list: List[Optional[Result]]):
    accumulated_gradient = None
    all_ihm_times = []
    mdc_serivced = []
    max_mdc_time, min_mdc_time = 0, float('inf')
    ihm_variances = []
    if not mdc_result_list:
        return {}
    for mdc_result in mdc_result_list:
        if mdc_result is None:
            continue
        (curr_grad, curr_sq_grad,
         curr_tot_runs_for_mdc, curr_ihms_failed_for_mdc,
         curr_time_tracker) = mdc_result

        curr_num_valid_runs = curr_tot_runs_for_mdc - curr_ihms_failed_for_mdc
        mdc_serivced.append((curr_tot_runs_for_mdc, curr_ihms_failed_for_mdc))
        all_ihm_times.extend(curr_time_tracker)
        max_mdc_time = max(sum(curr_time_tracker), max_mdc_time)
        min_mdc_time = min(sum(curr_time_tracker), min_mdc_time)

        if accumulated_gradient is None:
            accumulated_gradient = curr_grad
        else:
            if curr_grad is None:  # Can happen in the case where the MDC receives all Nones
                continue
            else:
                ihm_variances.append(
                    (curr_sq_grad / curr_num_valid_runs) -
                    (curr_grad / curr_num_valid_runs)
                )
                accumulated_gradient += curr_grad

    to_return = {
        "accum_grad": accumulated_gradient,
        "per_mdc_successes_failures": mdc_serivced,
        "all_times": all_ihm_times,
        "min_mdc_time": min_mdc_time,
        "max_mdc_time": max_mdc_time
    }
    return to_return
