#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 11:41:57 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# Maximaからのデータ読み込み
try:
    with open("transfer_params.txt", "r") as f:
        w_density_avg = float(f.readline().strip())
        r_avg = float(f.readline().strip())
except FileNotFoundError:
    print("Error: transfer_params.txt not found. Run maxima first.")
    exit()

# シミュレーション設定
target_power_tw = 10.0  # 金星SR制動目標電力 [TW]
e_mercury = 0.2056      # 水星の軌道離心率
theta = np.linspace(0, 2 * np.pi, 365) # 1公転分

# ケプラー軌道における太陽距離 r(theta) = a(1-e^2) / (1+e*cos(theta))
r_theta = r_avg * (1 - e_mercury**2) / (1 + e_mercury * np.cos(theta))

# 各地点での太陽放射強度 S(theta) は距離の逆二乗に比例
# Maximaで得た w_density_avg (平均距離での値) をスケーリング
w_theta = w_density_avg * (r_avg / r_theta)**2

# 目標電力を維持するために必要な面積 A [km^2]
# Power = Area * w_theta => Area = Power / w_theta
area_km2 = (target_power_tw * 1e12 / w_theta) / 1e6

# 結果の出力
print(f"--- Python Simulation Results (Coupled with Maxima) ---")
print(f"Required Area at Perihelion (近日点): {np.min(area_km2):.2f} km^2")
print(f"Required Area at Aphelion (遠日点): {np.max(area_km2):.2f} km^2")
print(f"Area Variation: {np.max(area_km2) - np.min(area_km2):.2f} km^2")

# グラフ作成
plt.figure(figsize=(10, 5))
plt.plot(np.degrees(theta), area_km2, color='orange', lw=2)
plt.title("Required Solar Panel Area over Mercury Orbit (#901)")
plt.xlabel("Orbital Angle (degrees)")
plt.ylabel("Required Area [km^2]")
plt.grid(True)
plt.savefig("area_simulation.png")
print("Simulation plot saved as 'area_simulation.png'.")