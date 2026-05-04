import numpy as np
from numpy import sqrt

def get_eta_formula(k, Q1, Q2):
    return (Q1*Q2*k**2)/(sqrt(Q1*Q2*k**2+1)+1)**2
