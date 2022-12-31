"""
We simulate a distributed training architecture by doing multiprocessing. We train a distributed classifier
    neural network where each "node" computes the aggregate gradient of a specific city block
"""
from typing import List

import numpy as np

from sol.monoids_day_4_final import ihm_success, ihm_failure, mdc_processor, npdc_processor, mdc_failure


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float
) -> List:
    ihm_results = []
    for i in range(num_ihms):
        if np.random.random() <= prob_ihm_crash:
            ihm_results.append(ihm_failure())
        else:
            ihm_results.append(ihm_success(NUM_FEATURES))
    return ihm_results


def mdc_run(
    prob_mdc_crash: float,
    prob_ihm_crash: float
):
    """
    We simulate the in-home-models by randomly generating data
    :param crash_proba:
    :return:
    """
    if np.random.random() < prob_mdc_crash:
        return mdc_failure()
    num_ihms = np.random.randint(2, 5)
    ihm_results = simulate_ihm(num_ihms, prob_ihm_crash)
    return mdc_processor(ihm_results)


if __name__ == '__main__':
    import pprint

    # Run the northpole-data-center
    mdc_results = []

    NUM_MDCS = np.random.randint(2, 10)
    NUM_FEATURES = 5

    print("Testing across various failure probabilities for robustness")
    for prob_mdc_crash in [0.1, 0.5, 0.9]:
        for prob_ihm_crash in [0.1, 0.5, 0.9]:
            print("*" * 25)
            print(f"Testing with parameters: MDC Crash: {prob_mdc_crash} and IHM Crash: {prob_ihm_crash}")
            for mdc in range(NUM_MDCS):
                mdc_results.append(mdc_run(prob_mdc_crash, prob_ihm_crash))
            pprint.pprint(npdc_processor(mdc_results))
