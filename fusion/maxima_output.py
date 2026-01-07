import numpy as np

def get_eta_formula(k, Q1, Q2):
    # Maxima derived formula
    from numpy import sqrt
    return (Q1*Q2*k**2)/(sqrt(Q1*Q2*k**2+1)+1)**2
