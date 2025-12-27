#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 14:31:09 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# パラメータ設定
f = 1e6
w = 2 * np.pi * f
V_tower = 100
R = 0.5  # 各回路の抵抗
ZL = 10  # 各家庭の負荷

def simulate_multi_user(M_inter):
    """
    M_inter: 家Aと家Bの間の干渉の強さ (相互インダクタンス)
    """
    M_t_a = np.linspace(0, 1e-6, 500) # タワーと家Aの結合
    P_a = []
    P_b = []

    # 固定値: タワーと家Bの結合は「理想的」な位置にあると仮定
    M_t_b = 0.38e-6 

    for m1 in M_t_a:
        # 行列 Z * I = V を解く
        # Z = [[Z11, jwM1, jwM2], [jwM1, Z22, jwM_ab], [jwM2, jwM_ab, Z33]]
        Z = np.array([
            [R, 1j*w*m1, 1j*w*M_t_b],
            [1j*w*m1, R+ZL, 1j*w*M_inter],
            [1j*w*M_t_b, 1j*w*M_inter, R+ZL]
        ])
        V = np.array([V_tower, 0, 0])
        try:
            I = np.linalg.solve(Z, V)
            P_a.append(np.abs(I[1])**2 * ZL)
            P_b.append(np.abs(I[2])**2 * ZL)
        except:
            P_a.append(0)
            P_b.append(0)
            
    return M_t_a * 1e6, np.array(P_a), np.array(P_b)

# --- 可視化 ---
plt.figure(figsize=(12, 6))

# ケース1: 干渉なし (家が遠く離れている)
m, pa1, pb1 = simulate_multi_user(M_inter=0)
plt.plot(m, pa1, label="House A (No Interference)", color='blue', lw=2)
plt.plot(m, pb1, label="House B (Stable)", color='blue', linestyle='--', alpha=0.5)

# ケース2: 干渉あり (家が隣接している)
m, pa2, pb2 = simulate_multi_user(M_inter=0.2e-6)
plt.plot(m, pa2, label="House A (Interfered)", color='red', lw=2)
plt.plot(m, pb2, label="House B (Dropped by A)", color='red', linestyle='--', alpha=0.8)

plt.title("Multi-User Interference Simulation")
plt.xlabel("Tower-to-House A Coupling M [uH]")
plt.ylabel("Power P [W]")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()