#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 13:07:51 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# 1. 解析解のインポートとクレンジング
with open("solution_p.txt", "r") as f:
    content = f.read().split(":")[-1].replace(";", "").strip()
    expr_py = content.replace("%e**", "np.exp").replace("^", "**").replace("%e", "np.e")

# 2. 空間グリッドの設定 (炉内の位置 x, y)
grid_size = 20
x = np.linspace(-10, 10, grid_size)
y = np.linspace(-10, 10, grid_size)
X, Y = np.meshgrid(x, y)

# 3. 炉内の温度分布モデル (中心が1200K, 周辺が800Kの分布を想定)
# 堅牢性の検証：中心部と外周部の温度差をシミュレート
R2 = X**2 + Y**2
T = 800 + 400 * np.exp(-R2 / 50) 

# 4. 各地点の再現性(P)を計算
P_grid = eval(expr_py)

# 5. 3次元プロット
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, P_grid, cmap=cm.viridis, edgecolor='none', alpha=0.8)

ax.set_title("3D Analysis of LENR Reproducibility (P)")
ax.set_xlabel("X [mm]")
ax.set_ylabel("Y [mm]")
ax.set_zlabel("Reaction Probability (P)")
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

print(f"炉内平均再現性: {np.mean(P_grid):.4f}")