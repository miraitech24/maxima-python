
import numpy as np
def velocity_logic(t, v0, ve, m0, dm):
    # Maxima解: v(t) = v0 + ve * ln(m0 / (m0 - dm*t))
    mass_ratio = m0 / (m0 - dm * t)
    return v0 + ve * np.log(mass_ratio)

def distance_logic(t, v0, ve, m0, dm):
    # Maxima解: s(t) = integrate(v(t), t)
    # 燃料切れ(dm*t >= m0)の判定を内包させる
    if dm * t >= m0: return np.nan
    term1 = (v0 + ve) * t
    term2 = (ve * (m0 - dm * t) / dm) * np.log((m0 - dm * t) / m0)
    return term1 + term2
