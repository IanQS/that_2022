"""
Our driver code that we can use to run the various sol/monoids_day_x.py files
"""

from typing import List, Dict, Any

import numpy as np

# from sol.monoids_day_0 import ihm_success, ihm_failure, tsp_processor
# from sol.monoids_day_1 import ihm_success, ihm_failure, tsp_processor
# from sol.monoids_day_2 import ihm_success, ihm_failure, tsp_processor
# from sol.monoids_day_3_cleanup import ihm_success, ihm_failure, tsp_processor
from sol.monoids_day_4_final import ihm_success, ihm_failure, tsp_processor


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float
) -> List:
    """
    SDimulates the accumulation process on our central server
    """
    #
    ihm_results = []
    for i in range(num_ihms):
        if np.random.random() <= prob_ihm_crash:
            ihm_results.append(ihm_failure())
        else:
            ihm_results.append(ihm_success(NUM_FEATURES))
    return ihm_results


def tsp_run(
    prob_ihm_crash: float
) -> Dict[str, Any]:
    """
    We simulate the in-home-models by randomly generating data
    :param crash_proba:
    :return:
    """
    num_ihms = np.random.randint(2, 5)
    ihm_results: List = simulate_ihm(num_ihms, prob_ihm_crash)
    return tsp_processor(ihm_results)


if __name__ == '__main__':
    import pprint

    # Run the northpole-data-center
    mdc_results = []

    NUM_MDCS = np.random.randint(2, 10)
    NUM_FEATURES = 5

    print("Testing across various failure probabilities of ih-home-models for robustness")
    for prob_ihm_crash in [0.1, 0.5, 0.9]:
        print("*" * 25)
        print(f"Testing with probability of IHM Crash: {prob_ihm_crash * 100}%")
        result = tsp_run(prob_ihm_crash)
        pprint.pprint(result)
