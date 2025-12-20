#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 15:06:50 2025

@author: iwamura
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# Maximaが生成したファイルをインポート
try:
    import kinematics
    import importlib
    importlib.reload(kinematics) # ファイルが更新された場合に備えて再読込
    print("Successfully imported kinematics.py")
except ImportError:
    print("Error: kinematics.py not found. Run Maxima script first.")

# パラメータ
params = {'m': 1.0, 'l': 1.0, 'g': 9.8}

def system_dynamics(t, y):
    theta, omega = y
    # Maximaが生成した関数をそのまま使用
    dtheta_dt = omega
    domega_dt = kinematics.get_accel(theta, **params)
    return [dtheta_dt, domega_dt]

# シミュレーション実行
t_eval = np.linspace(0, 10, 500)
sol = solve_ivp(system_dynamics, [0, 10], [np.radians(170), 0], t_eval=t_eval)

# プロット
plt.plot(sol.t, np.degrees(sol.y[0]))
plt.title("Automated Simulation via Maxima Export")
plt.xlabel("Time [s]"); plt.ylabel("Angle [deg]")
plt.grid(True); plt.show()