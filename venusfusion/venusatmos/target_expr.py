import numpy as np

def get_tesla_power(d, P_surf, Q, k_0):
    return (P_surf*Q*k_0**2)/d**4

def get_export_surplus(d, P_surf, Q, k_0, P_engine):
    return (P_surf*Q*k_0**2)/d**4-P_engine
