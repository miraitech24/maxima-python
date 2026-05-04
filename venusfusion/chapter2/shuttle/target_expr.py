import numpy as np

def get_temp_formula(P, e, s, A, Ts):
    return -(P/(A*e*s)+Ts**4)**(1/4)
