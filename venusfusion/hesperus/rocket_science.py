import numpy as np

def get_v(t, v0, ve, m0, dm):
    # Maxima: v0 + ve * log(m0 / (m0 - dm*t))
    return v0 + ve * np.log(m0 / (m0 - dm * t))

def get_s(t, v0, ve, m0, dm):
    # Maxima: integrate(v0 + ve*log(m0/(m0-dm*t)), t)
    # Result: (v0+ve)*t + (ve*(m0-dm*t)/dm)*log((m0-dm*t)/m0)
    term1 = (v0 + ve) * t
    term2 = (ve * (m0 - dm * t) / dm) * np.log((m0 - dm * t) / m0)
    return term1 + term2