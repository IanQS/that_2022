"""
The code to start all our iterations of our functor code
"""
from typing import List, Dict, Any
import numpy as np

from sol.functor_day_3_cleanup import (simulate_ihm,
                               IHMResult)
from sol.avl_tree_functor import AVLTree


def apply_functions_to_ihms(
        prob_ihm_crash: float,
        verbose=False
):
    """
    We simulate the in-home-models by randomly generating data
    :param crash_proba:
    :return:
    """
    num_ihms = np.random.randint(10)
    ihm_results = simulate_ihm(num_ihms, prob_ihm_crash, NUM_FEATURES)

    def add_random_proba(
        result: IHMResult,
    ) -> IHMResult:
        """
        We add a random probability of filtering out
        """
        result.proba_filter = np.random.random()
        return result

    def filter_func(
        result: IHMResult
    ) -> bool:
        if result.proba_filter < 0.5:
            return False
        return True

    ################################################
    # Apply the functions
    ################################################

    mapped_ihms = AVLTree.fmap(ihm_results, add_random_proba)
    filtered_ihms = AVLTree.filter(mapped_ihms, filter_func)

    if verbose:
        print(f"Original length: {len(ihm_results)}")
        print(f"Post-filter length: {len(filtered_ihms)}")

        print("*" * 10)
        print("Done")



if __name__ == '__main__':
    import pprint

    NUM_FEATURES = 5

    print("Testing across various failure probabilities of ih-home-models for robustness")
    for prob_ihm_crash in [0.1, 0.5, 0.9]:
        apply_functions_to_ihms(prob_ihm_crash)
    print("Passed sanity checks at 10% 50% and 90% failure probability")
    print("*" * 10)
    apply_functions_to_ihms(prob_ihm_crash=0.0, verbose=True)