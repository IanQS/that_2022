"""
The starting point for our future experimental work. Note that this is
more or less what we had in our section on monoids
"""
from typing import List

import numpy as np


################################################
# Unnecessary for our setup
################################################


def ihm_success(num_features):
    time_taken = np.random.rand()
    gradient = np.random.rand(num_features)
    loss = np.random.rand(1, 100) / 100
    return gradient, time_taken * 10, loss


def ihm_failure():
    return None


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> List:
    ihm_results = []
    for i in range(num_ihms):
        if np.random.random() <= prob_ihm_crash:
            ihm_results.append(ihm_failure())
        else:
            ihm_results.append(ihm_success(num_features))
    return ihm_results
