"""
The requests:

1) find the fastest and slowest MDCs (to fix up the connection/ bump up the hardware)
2) find the variance of grads for both the IHMs and the MDCs

See the accompanying
"""

from dataclasses import dataclass, field
from typing import List, Optional, TypeVar, Tuple

import numpy as np

Result = TypeVar("Result")


################################################
# Trackers:
# Code to ensure we are keeping track of everything correctly
#   - part of the issue is that as requirements get changed, we are liable
#     to miss out or forget information, which would be disastrous
################################################

@dataclass
class MDC_Monoid():
    accum_grad: np.ndarray = np.empty(())
    accum_sq_grad: np.ndarray = np.empty(())
    num_houses_serviced: int = 0
    num_IHMs_failed: int = 0
    ihm_time_tracker: List[float] = field(default_factory=list)

    @classmethod
    def make(cls,
             maybe_val: Optional[Result]
             ):
        """
        To make our maybe val which tracks IHM accumulations
            whether those IHMs failed, or not
        :param maybe_val:
        :return:
        """
        if maybe_val is None:
            to_ret = cls()
            to_ret.num_houses_serviced += 1
            to_ret.num_IHMs_failed += 1
            return to_ret
        accum_grad, ihm_time = maybe_val
        return cls(
            accum_grad=accum_grad,
            accum_sq_grad=accum_grad ** 2,
            num_houses_serviced=1,
            num_IHMs_failed=0,
            ihm_time_tracker=[ihm_time]
        )

    def __add__(self, other: Optional["MDC_Monoid"]) -> "MDC_Monoid":
        if other is None:
            return self
        return MDC_Monoid(
            accum_grad=self.accum_grad + other.accum_grad,
            accum_sq_grad=self.accum_sq_grad + other.accum_sq_grad,
            num_houses_serviced=self.num_houses_serviced + other.num_houses_serviced,
            num_IHMs_failed=self.num_IHMs_failed + other.num_IHMs_failed,
            ihm_time_tracker=self.ihm_time_tracker + other.ihm_time_tracker
        )


@dataclass
class NPDC_Monoid():
    accum_grad: np.ndarray = np.empty(())
    mdc_results: List[Tuple[int, int]] = field(default_factory=list)
    all_times: List[float] = field(default_factory=list)
    min_mdc_time: float = float('inf')
    max_mdc_time: float = 0
    grad_variances: List[float] = field(default_factory=list)

    @classmethod
    def make(cls,
             maybe_MDC_monoid: Optional[MDC_Monoid]
             ):
        """
        To make our maybe val which tracks IHM accumulations
            whether those IHMs failed, or not
        :param maybe_MDC_monoid:
        :return:
        """
        if maybe_MDC_monoid is None:
            return cls()
        mdc_monoid = maybe_MDC_monoid
        valid_runs = mdc_monoid.num_houses_serviced - mdc_monoid.num_IHMs_failed
        if valid_runs == 0:
            variance = np.nan
        else:
            variance = (mdc_monoid.accum_sq_grad / valid_runs) - \
                       (mdc_monoid.accum_grad / valid_runs)

        time_tracker = mdc_monoid.ihm_time_tracker
        if len(time_tracker) == 0:
            # Use the default
            min_time = cls.min_mdc_time
            max_time = cls.max_mdc_time
        else:
            min_time = min(time_tracker)
            max_time = max(time_tracker)

        return cls(
            accum_grad=mdc_monoid.accum_grad,
            mdc_results=[(valid_runs, mdc_monoid.num_IHMs_failed)],
            all_times=mdc_monoid.ihm_time_tracker,
            min_mdc_time=min_time,
            max_mdc_time=max_time,
            grad_variances=[variance]
        )

    def __add__(self, other: Optional["NPDC_Monoid"]) -> "NPDC_Monoid":
        if other is None:
            return self
        return NPDC_Monoid(
            accum_grad=self.accum_grad + other.accum_grad,
            mdc_results=self.mdc_results + other.mdc_results,
            all_times=self.all_times + other.all_times,
            min_mdc_time=min(self.min_mdc_time, other.min_mdc_time),
            max_mdc_time=max(self.max_mdc_time, other.max_mdc_time),
            grad_variances=self.grad_variances + other.grad_variances
        )

    def __str__(self):
        successes = 0
        failures = 0
        for el in self.mdc_results:
            successes += el[0]
            failures += el[1]
        to_ret = f"Across {len(self.mdc_results)} MDCs with {successes} successes and {failures} failures\n"
        to_ret += f"\tAccumulated Gradients: {self.accum_grad}\n"
        to_ret += f"\tMDC Results: {self.mdc_results}\n"
        to_ret += f"\tAll Times: {self.all_times}\n"
        to_ret += f"\tMin MDC Train Time: {self.min_mdc_time}\n"
        to_ret += f"\tMax MDC Train Time: {self.max_mdc_time}\n"
        to_ret += f"\tMDC Gradient Variances: {self.grad_variances}"
        return to_ret

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


def mdc_processor(ihm_results: List[Optional[Result]]) -> MDC_Monoid:
    mdc_tracker = MDC_Monoid()
    if not ihm_results:
        return mdc_tracker
    for i, result in enumerate(ihm_results):
        mdc_tracker += MDC_Monoid.make(result)
    return mdc_tracker


def npdc_processor(mdc_result_list: List[Optional[Result]]):
    npdc_tracker = NPDC_Monoid()
    if not mdc_result_list:
        return npdc_tracker
    for mdc_result in mdc_result_list:
        npdc_tracker += NPDC_Monoid.make(mdc_result)

    return npdc_tracker
