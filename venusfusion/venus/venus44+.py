#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 11:39:10 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 物理パラメータ設定 ---
L_total = 556285.39  # km (前回の計算結果：総延長)
P_chimney_gw = 12.5   # GW (案C: 煙突発電の推定値)
P_lenr_gw = 100.0     # GW (課題#41: メインLENR炉の定格)

# 維持コスト係数 (1kmあたりの維持・自己修復電力 MW/km)
# 55万kmという長大さを考慮し、高度(宇宙環境)による変動を模擬
def maintenance_cost_per_km(dist_km):
    # 地表付近は熱、宇宙空間は放射線と微小隕石による劣化を想定
    base_cost = 0.05 # MW/km (基礎維持)
    thermal_stress = 0.15 * np.exp(-dist_km / 50) # 高度50kmまでは熱応力大
    space_debris = 0.02 * (dist_km / 10000) # 宇宙空間では距離に応じて衝突確率増
    return base_cost + thermal_stress + space_debris

# --- 収支計算 ---
dist_axis = np.linspace(0, L_total, 1000)
costs = maintenance_cost_per_km(dist_axis)
total_maint_gw = np.trapz(costs, dist_axis) / 1000 # GW換算

p_supply = P_chimney_gw + P_lenr_gw
p_net = p_supply - total_maint_gw

# --- 可視化 ---
plt.figure(figsize=(10, 6))
plt.plot(dist_axis, costs, color='red', label='Maintenance Load (MW/km)')
plt.fill_between(dist_axis, costs, alpha=0.2, color='red')
plt.title(f"Tether Energy Balance (Total Length: {L_total:.1f} km)")
plt.xlabel("Distance from Venus Surface (km)")
plt.ylabel("Required Maintenance Power (MW/km)")
plt.grid(True)

print(f"--- #44 Extended Balance Report ---")
print(f"Total Supply  : {p_supply:.2f} GW")
print(f"Total Maint   : {total_maint_gw:.2f} GW")
print(f"Net Export    : {p_net:.2f} GW")
print(f"Survival Rate : {'Stable' if p_net > 0 else 'CRITICAL FAILURE'}")

plt.show()