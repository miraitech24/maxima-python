#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 15:29:55 2025

@author: iwamura
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import kinematics
import importlib
importlib.reload(kinematics)

# パラメータ
m, l, g = 1.0, 1.0, 9.8

# 微分方程式
def system_dynamics(t, y):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = kinematics.get_accel(theta, m, l, g)
    return [dtheta_dt, domega_dt]

# 実行（少し長めに20秒間）
t_eval = np.linspace(0, 20, 1000)
sol = solve_ivp(system_dynamics, [0, 20], [np.radians(170), 0], t_eval=t_eval)

# --- エネルギー計算 ---
# 各時刻の(theta, omega)に対してエネルギーを計算
energies = [kinematics.get_energy(th, om, m, l, g) for th, om in zip(sol.y[0], sol.y[1])]

# --- 可視化 ---
fig, ax1 = plt.subplots(figsize=(10, 5))

# 角度のプロット（左軸）
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Angle [deg]', color='tab:blue')
ax1.plot(sol.t, np.degrees(sol.y[0]), color='tab:blue', label='Angle')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# エネルギーのプロット（右軸）
ax2 = ax1.twinx()
ax2.set_ylabel('Total Energy [J]', color='tab:red')
ax2.plot(sol.t, energies, color='tab:red', linestyle='--', label='Total Energy')
ax2.tick_params(axis='y', labelcolor='tab:red')
# エネルギーの変化を分かりやすくするため、表示範囲を調整
ax2.set_ylim(min(energies)-1, max(energies)+1)

plt.title("Pendulum Dynamics & Energy Conservation")
plt.grid(True)
plt.show()

plt.figure(figsize=(7, 7))
# 横軸：角度(radian), 縦軸：角速度
plt.plot(sol.y[0], sol.y[1])

plt.title("Phase Portrait of Pendulum")
plt.xlabel("Theta [rad]")
plt.ylabel("Omega [rad/s]")
plt.axhline(0, color='black', lw=1)
plt.axvline(0, color='black', lw=1)
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()