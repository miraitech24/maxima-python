#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 13:12:26 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# 1. 解析解のインポート
with open("solution_p.txt", "r") as f:
    content = f.read().split(":")[-1].replace(";", "").strip()
    expr_py = content.replace("%e**", "np.exp").replace("^", "**").replace("%e", "np.e")

# 2. 空間グリッド設定
grid_size = 25
x = np.linspace(-10, 10, grid_size)
y = np.linspace(-10, 10, grid_size)
X, Y = np.meshgrid(x, y)
R2 = X**2 + Y**2

# 3. 地球 vs 金星 の温度分布モデル
# 地球: 冷却効率が高く、温度差が少ない (1050K ~ 1100K)
T_earth = 1050 + 50 * np.exp(-R2 / 100)
# 金星: 抜熱が困難で、中心に熱がこもる (1000K ~ 1400K)
T_venus = 1000 + 400 * np.exp(-R2 / 40)

# 4. 反応確率 P の計算
T = T_earth
P_earth = eval(expr_py)
T = T_venus
P_venus = eval(expr_py)

# 5. 3次元対比プロット
fig = plt.figure(figsize=(16, 7))

# 地球のグラフ
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, P_earth, cmap=cm.Blues, alpha=0.8)
ax1.set_title("Earth: High Robustness (Uniform P)")
ax1.set_zlim(0, 1)

# 金星のグラフ
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(X, Y, P_venus, cmap=cm.Reds, alpha=0.8)
ax2.set_title("Venus: Low Robustness (P Saturation/Thermal Runaway)")
ax2.set_zlim(0, 1)

plt.show()

print(f"地球平均再現性: {np.mean(P_earth):.4f}")
print(f"金星平均再現性: {np.mean(P_venus):.4f} (中心部偏重)")