"""

"""

import numpy as np

from sol.functor_day_3_cleanup import simulate_ihm, prototype

if __name__ == '__main__':
    NUM_FEATURES = 5
    PROTOTYPE_MODE = True

    num_ihms = np.random.randint(4, 20)
    if PROTOTYPE_MODE:
        print("In prototype mode, where crash-probability is 0")
        prototype(num_ihms, 0, NUM_FEATURES)
    else:
        for prob_ihm_crash in [0.1, 0.5, 0.9]:
            num_ihms = np.random.randint(4, 20)
            print(f"Testing with IHM Crash proba: {prob_ihm_crash}")
            print("*" * 25)
            simulate_ihm(num_ihms, prob_ihm_crash, NUM_FEATURES)
