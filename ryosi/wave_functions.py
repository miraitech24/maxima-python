import numpy as np
from numpy import sqrt, pi

def psi_0(x):
    return np.e**-(x**2/2)/pi**(1/4)

def psi_1(x):
    return (sqrt(2)*x*np.e**-(x**2/2))/pi**(1/4)

def psi_2(x):
    return ((2*x**2-1)*np.e**-(x**2/2))/(sqrt(2)*pi**(1/4))

def psi_3(x):
    return ((2*sqrt(3)*x**3-3**(3/2)*x)*np.e**-(x**2/2))/(3*pi**(1/4))

