import numpy as np
def get_temp(r, T0, R0, w, k):
    return (R0*T0*np.exp(-(((r-R0)*np.sqrt(w))/np.sqrt(k)))/r)
