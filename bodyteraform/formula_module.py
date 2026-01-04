import numpy as np
def get_voltage(x, lambda_val, V0):
    return V0 * np.exp(-x / lambda_val)
