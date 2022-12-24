"""
Cleanup!!
"""
import time

import numpy as np
from typing import List, Optional, Tuple
from dataclasses import dataclass

Result = Tuple[np.ndarray, float]


################################################
# Trackers:
# Code to ensure we are keeping track of everything correctly
#   - part of the issue is that as requirements get changed, we are liable
#     to miss out or forget information, which would be disastrous
################################################

@dataclass
class MDC_Tracker():
    accum_grad: np.ndarray
    accum_sq_grad: np.ndarray
    num_houses_serviced: int
    num_IHMs_failed: int
    ihm_time_tracker: List[float]

    def release(self) -> Tuple:
        return self.accum_grad, self.accum_sq_grad, \
            self.num_houses_serviced, self.num_IHMs_failed, \
            self.ihm_time_tracker

@dataclass
class NPDC_Tracker():
    accum_grad: np.ndarray
    mdc_results: List[Tuple[int, int]]
    all_times: List[float]
    min_mdc_time: float
    max_mdc_time: float
    grad_variances: List[float]

    def __str__(self):
        return f"""Accumulated Gradients: {self.accum_grad}
        MDC Results: {self.mdc_results},
        All Times: {self.all_times},
        Min MDC Train Time: {self.min_mdc_time},
        Max MDC Train Time: {self.max_mdc_time},
        MDC Gradient Variances: {self.grad_variances}
        """

    def __repr__(self):
        return self.__str__()

################################################
# Actual code
################################################

def ihm_success(num_features) -> Result:
    time_taken = np.random.rand()
    gradients = np.random.rand(num_features)
    return gradients, time_taken * 10


def ihm_failure():
    return None


def mdc_failure():
    return None


def mdc_processor(
    ihm_results: Optional[Result]
) -> Optional[MDC_Tracker]:
    if not ihm_results:
        return None
    accumulated_gradient = None
    accumulated_sq_gradient = None
    num_valids = 0
    ihm_time_tracker = []
    counter = 0

    for i, result in enumerate(ihm_results):
        result: Optional[Tuple[np.ndarray, float]]
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
    return MDC_Tracker(
        accumulated_gradient,
        accumulated_sq_gradient,
        num_houses_serviced,
        num_IHMs_failed,
        ihm_time_tracker
    )


def npdc_processor(
    mdc_result_list: Optional[List[Optional[MDC_Tracker]]]
) -> Optional[NPDC_Tracker]:
    accum_grad = None
    all_ihm_times = []
    mdc_serviced = []
    max_mdc_time, min_mdc_time = 0, float('inf')
    ihm_variances = []
    if not mdc_result_list:
        return None
    for mdc_result in mdc_result_list:
        if mdc_result is None:
            continue
        (curr_grad, curr_sq_grad,
         curr_tot_runs, curr_ihms_failed,
         curr_time_tracker) = mdc_result.release()

        curr_num_valid_runs = curr_tot_runs - curr_ihms_failed
        mdc_serviced.append((curr_tot_runs, curr_ihms_failed))
        all_ihm_times.extend(curr_time_tracker)
        max_mdc_time = max(sum(curr_time_tracker), max_mdc_time)
        min_mdc_time = min(sum(curr_time_tracker), min_mdc_time)
        if accum_grad is None:
            accum_grad = curr_grad
        else:
            if curr_grad is None:  # Can happen in the case where the MDC receives all Nones
                continue
            else:
                ihm_variances.append(
                    (curr_sq_grad / curr_num_valid_runs) -
                    (curr_grad / curr_num_valid_runs)
                )
                accum_grad += curr_grad
    to_return = NPDC_Tracker(
        accum_grad,
        mdc_serviced,
        all_ihm_times,
        min_mdc_time,
        max_mdc_time,
        ihm_variances
    )
    return to_return
