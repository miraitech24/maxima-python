import numpy as np
def get_v(t, v0, ve, m0, thrust):
    dm = thrust / ve
    return v0 + ve * np.log(m0 / (m0 - dm * t))

def get_s(t, v0, ve, m0, thrust):
    dm = thrust / ve
    # Maxima積分解: integrate(v0 + ve*log(m0/(m0-dm*t)), t)
    term1 = (v0 + ve) * t
    term2 = (ve * (m0 - dm * t) / dm) * np.log((m0 - dm * t) / m0)
    return term1 + term2