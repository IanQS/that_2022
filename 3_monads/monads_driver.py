"""
The same as the code from functor_driver.py, except we're no longer
in prototype mode. Now, our code can crash.
"""
import copy

import numpy as np
from typing import List, Any
from sol.monad_day_1 import simulate_ihm

if __name__ == '__main__':
    NUM_FEATURES = 5
    PROTOTYPE_MODE = True

    for prob_ihm_crash in [0.1, 0.5, 0.9]:
        num_ihms = np.random.randint(4, 20)
        print(f"Testing with IHM Crash proba: {prob_ihm_crash}")
        print("*" * 25)
        try:
            generated_tree = simulate_ihm(num_ihms, prob_ihm_crash, NUM_FEATURES)
        except TypeError as e:
            # Only in case of monad_day_0
            generated_tree, failures = simulate_ihm(num_ihms, prob_ihm_crash, NUM_FEATURES)
