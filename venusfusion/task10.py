#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 11:33:22 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# 定数設定
P_v = 9.3e6      # 金星地表圧 (Pa)
A_v = 4.6e14     # 金星表面積 (m2)
g_v = 8.87       # 金星重力 (m/s2)
M_co2 = 0.044    # CO2分子量 (kg/mol)
delta_H = 393.5e3 # 分解エンタルピー (J/mol)

# 1. 大気分解に必要な総エネルギー (Maximaの考え方を適用)
total_energy_needed = (P_v * A_v / (M_co2 * g_v)) * delta_H
print(f"Total Energy for Terraforming: {total_energy_needed:.2e} Joules")

# 2. 地球の氷河期阻止シミュレーション
# 地球が氷河期を避けるために必要な追加エネルギー量（太陽定数の数%と仮定）
years = np.linspace(0, 100, 100)
energy_supply = np.linspace(0, total_energy_needed * 0.01, 100) # 核融合炉の出力向上

# 氷河期を止める閾値 (想定)
threshold = 1.0e18 # 必要な年間追加エネルギー(J)

plt.figure(figsize=(10, 5))
plt.plot(years, energy_supply / 1e18, label="Fusion Artificial Sun Output")
plt.axhline(y=threshold/1e18, color='r', linestyle='--', label="Ice Age Prevention Threshold")
plt.title("Post-Terraforming Energy Strategy: Saving Earth from Ice Age")
plt.xlabel("Years after Terraforming")
plt.ylabel("Energy (Exajoules / Year)")
plt.legend()
plt.grid(True)
plt.show()