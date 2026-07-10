#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 11:12:24 2025

@author: iwamura
"""

# simulation.py
import numpy as np
import matplotlib.pyplot as plt

# 1. Maximaからの計算結果を引き継ぎ
try:
    from params import E_L_computed
    print(f"Imported V_rest from Maxima: {E_L_computed}")
except ImportError:
    E_L_computed = -70.0  # fallback

def model(V, t, I_ext):
    g_L = 0.3
    # Maximaから引き継いだパラメータを使用
    dVdt = (I_ext - g_L * (V - E_L_computed)) 
    return dVdt

# 2. 数値計算 (Euler法)
dt = 0.01
t = np.arange(0, 10, dt)
V = np.zeros_like(t)
V[0] = E_L_computed
I_ext = 1.0 # 外部刺激

for i in range(1, len(t)):
    V[i] = V[i-1] + model(V[i-1], t[i-1], I_ext) * dt

# 3. 可視化
plt.plot(t, V)
plt.title("Neuron Membrane Potential (Coupled Maxima-Python)")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.grid(True)
plt.show()