import numpy as np
from numpy import sin, cos

def get_accel(theta, m, l, g):
    return 'subst([theta = theta,theta(t) = theta],0)

def get_energy(theta_val, omega_val, m, l, g):
    return 'subst(['diff(theta,t,1) = omega_val,theta = theta_val],(l**2*m*diff(theta,t)**2)/2-g*l*m*cos(theta))
