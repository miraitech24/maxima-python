import numpy as np
from numpy import sin, cos

def get_accel(theta, m, l, g):
    return -(g*sin(theta))/l

def get_energy(theta_val, omega_val, m, l, g):
    return (l**2*m*omega_val**2)/2-g*l*m*cos(theta_val)
