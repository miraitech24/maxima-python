#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:31:46 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# 沼対策：ファイルの存在確認
if not os.path.exists("params_31.py"):
    print("【警告】params_31.py が見当たりません。パスを確認してください。")
    # デバッグ用に最小限の値を手動設定（ファイルがない場合のみ動作）
    P_SURFACE, T_SURFACE, GAMMA, K_DECAY, ALPHA = 92.0, 737.0, 1.28, 0.005, 0.218
else:
    import params_31
    P_SURFACE = params_31.P_SURFACE
    T_SURFACE = params_31.T_SURFACE
    GAMMA = params_31.GAMMA
    K_DECAY = params_31.K_DECAY
    ALPHA = params_31.ALPHA
    print("引数の読み込みに成功しました。")

def simulate_maxwell_pump():
    # スーパーローテーションの風速 (20m/s から 160m/s)
    v_wind = np.linspace(20, 160, 100)
    
    # 1. 流体-圧力連成: ベルヌーイの原理による山頂負圧
    # 密度 60kg/m3 で計算
    rho_venus = 60.0 
    p_dynamic = (0.5 * rho_venus * v_wind**2) / 101325 # Pa to atm
    p_top_static = 45.0 # 標高11kmの静圧
    p_exhaust = p_top_static - p_dynamic # 煙突内の負圧
    
    # 2. 圧力-熱連成: 断熱膨張による到達温度
    # T2 = T1 * (P2/P1)^alpha
    t_exhaust_k = T_SURFACE * (p_exhaust / P_SURFACE)**ALPHA
    t_exhaust_c = t_exhaust_k - 273.15
    
    return v_wind, p_exhaust, t_exhaust_c

# シミュレーション実行
v, p, t = simulate_maxwell_pump()

# 可視化
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel('Super-rotation Speed (m/s)')
ax1.set_ylabel('Internal Pressure (atm)', color='blue')
ax1.plot(v, p, color='blue', label='Pressure in Shaft')
ax1.grid(True, which='both', linestyle='--', alpha=0.5)

ax2 = ax1.twinx()
ax2.set_ylabel('Exhaust Temperature (°C)', color='red')
ax2.plot(v, t, color='red', linestyle='-', linewidth=2, label='Adiabatic Cooling Temp')

plt.title("Coupled Analysis: Pressure-Heat Feedback (Task 31)")
fig.tight_layout()
plt.show()

print(f"風速150m/s時の排熱温度: {t[-1]:.2f} ℃")