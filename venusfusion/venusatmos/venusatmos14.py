#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 12:46:31 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import re

# MaximaからS_extを読み込み
with open("scattering_slope.txt", "r") as f:
    S_EXT = float(re.search(r"[-+]?\d*\.\d+[eE][-+]?\d+|\d+", f.read()).group())

# 高度に応じた硫酸粒子密度分布
def get_density(z_km):
    # 48-60kmに濃密な雲層を配置
    if 48 <= z_km <= 60:
        return 5.0e8 * np.exp(-(z_km - 54)**2 / 10)
    return 1.0e5

altitudes = np.linspace(0, 100, 1000)
transmission = [1.0]

for i in range(1, len(altitudes)):
    dz = (altitudes[i] - altitudes[i-1]) * 1000
    gamma = get_density(altitudes[i]) * S_EXT
    transmission.append(transmission[-1] * np.exp(-gamma * dz))

print(f"Imported S_EXT: {S_EXT:.2e}")
print(f"Final Transmission at Orbit: {transmission[-1]*100:.2f} %")

# 視覚化
fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.plot(altitudes, np.array(transmission)*100, color='red', label='Transmission Efficiency')
ax1.set_xlabel("Altitude (km)"); ax1.set_ylabel("Efficiency (%)")
ax2 = ax1.twinx()
ax2.fill_between(altitudes, 0, [get_density(a) for a in altitudes], color='yellow', alpha=0.2, label='Cloud Density')
ax2.set_ylabel("Particle Density (n/m^3)")
plt.title("Beam Attenuation through Venusian Sulfuric Clouds")
plt.grid(True); plt.show()