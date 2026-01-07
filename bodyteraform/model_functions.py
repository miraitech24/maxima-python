import numpy as np
def calculate_yield(S, A, DeltaE, k, sigma):
    return A*np.e**((-S*sigma)-DeltaE/(S*k))
