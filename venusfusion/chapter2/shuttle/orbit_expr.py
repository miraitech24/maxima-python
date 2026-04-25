import numpy as np

def get_travel_time(D, a):
    # Maxima derived: Time to cover distance D with constant acc/dec a
    return 2*sqrt(D/a)
