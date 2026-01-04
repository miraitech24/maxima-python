#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 17:37:28 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import thermal_module

# 引数取得: python dual_viz.py [T0] [V0]
t0_val = float(sys.argv[1]) if len(sys.argv) > 1 else 2.5   # 温度上昇(K)
v0_val = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0 # 電圧(mV)

# 定数設定
R0, w, k, lam = 0.5, 0.08, 0.5, 0.5
r = np.linspace(R0 + 0.01, 5.0, 200)

# 計算実行
temp_dist = [thermal_module.get_temp(ri, t0_val, R0, w, k) for ri in r]
volt_dist = [v0_val * np.exp(-ri/lam) for ri in r]
t_at_1mm = thermal_module.get_temp(1.0, t0_val, R0, w, k)

# 描画
fig, ax1 = plt.subplots(figsize=(10, 6))

# 左軸: 電圧（刺激）
ax1.set_xlabel('Distance r (mm)')
ax1.set_ylabel('Potential V (mV)', color='cyan')
ax1.plot(r, volt_dist, color='cyan', lw=2, label='Voltage (Stimulus)')
ax1.tick_params(axis='y', labelcolor='cyan')

# 右軸: 温度（リスク）
ax2 = ax1.twinx()
ax2.set_ylabel('Temperature Rise T (K)', color='orangered')
ax2.plot(r, temp_dist, color='orangered', lw=2, label='Heat (Risk)')
ax2.axhline(1.0, color='red', linestyle='--', alpha=0.5) 
ax2.tick_params(axis='y', labelcolor='orangered')

# 1mm地点の判定
marker_color = 'green' if t_at_1mm <= 1.0 else 'red'
ax2.scatter([1.0], [t_at_1mm], color=marker_color, s=120, zorder=5)
ax2.annotate(f'1.0mm: {t_at_1mm:.2f}K', (1.0, t_at_1mm), 
             textcoords="offset points", xytext=(10,10), color=marker_color, weight='bold')

plt.title("Bio-Interface: Balancing Neural Stimulus and Thermal Safety")
plt.grid(True, linestyle=':', alpha=0.4)
plt.show()