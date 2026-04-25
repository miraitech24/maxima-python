import numpy as np
def velocity_func(t, v0, ve, m0, dm):
    return v0 + ve * np.log(m0 / (m0 - dm * t))

def distance_func(t, v0, ve, m0, dm):
    # Maxima 厳密解: (v0+ve)*t + (ve*(m0-dm*t)/dm)*log((m0-dm*t)/m0)
    term1 = (v0 + ve) * t
    term2 = (ve * (m0 - dm * t) / dm) * np.log((m0 - dm * t) / m0)
    return term1 + term2