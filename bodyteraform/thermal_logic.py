import numpy as np
def get_temperature(r, T0, R0, w, k):
    # Maxima derived solution
    return T0 * (R0/r) * np.exp(-np.sqrt(w/k)*(r-R0))
