import numpy as np

def get_v_acc(M0, t, mdot, ve):
    return ve * np.log(M0 / (M0 - mdot * t))

def get_d_acc(M0, t, mdot, ve):
    return ((mdot*t*log(-M0/(mdot*t-M0))+M0*log(mdot*t-M0)+mdot*t-log(-M0)*M0)*ve)/mdot
