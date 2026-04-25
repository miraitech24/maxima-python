#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 13:44:46 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import re

# Maximaから吸収式を読み込み
with open("formula_12.txt", "r") as f:
    raw = re.sub(r'<[^>]+>', '', f.read()).strip()
    formula_py = raw.replace("%e", "np.exp")

# 設置シミュレーション
# alpha (吸収係数): 金星=0.8, 地球=0.1 と仮定
alpha_val = 0.8
L_range = np.linspace(0, 50000, 100) # 大気層の厚み(m)
P_source = 1e15 # 人工太陽の想定出力(W)

# 大気が吸収してしまうエネルギー量
P_absorbed = eval(formula_py, {"np": np, "alpha": alpha_val, "L": L_range, "P_source": P_source})

plt.plot(L_range/1000, P_absorbed / 1e12)
plt.title("Energy Loss by Atmospheric Absorption (Venus Surface)")
plt.xlabel("Atmospheric Thickness (km)")
plt.ylabel("Absorbed Heat (Terawatts)")
plt.grid(True)
plt.show()