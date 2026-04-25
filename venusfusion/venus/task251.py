#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 14:07:51 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# 1. Maxima解析解の読み込みと完全クレンジング
with open("solution_p.txt", "r") as f:
    raw = f.read().split(":")[-1].replace(";", "").strip()
    # Pythonが理解できる形式へ徹底変換（%e沼の完全回避）
    expr_py = raw.replace("%e", "np.e").replace("exp", "np.exp").replace("^", "**")

# --- 設定値 ---
Eb, k, S = 0.5, 8.617e-5, 5.0
n = 10000

# 2. 【解析A】惑星間ヒストグラム比較 (冷却限界に基づく客観的対比)
# 地球: 空冷限界により低温運用(850K付近)
T_earth_hist = 850 + np.random.normal(0, 30, n)
# 金星: 高性能sCO2冷却により高温安定運用(1150K付近)
T_venus_hist = 1150 + np.random.normal(0, 10, n)

delta = np.random.normal(0, 0.1, n) # 材料のムラ

# 地球計算
T, delta = T_earth_hist, delta
P_earth = eval(expr_py)

# 金星計算
T, delta = T_venus_hist, delta
P_venus = eval(expr_py)

# 3. 【解析B】金星炉内部の3次元空間分布
grid_size = 40
x = np.linspace(-10, 10, grid_size)
y = np.linspace(-10, 10, grid_size)
X, Y = np.meshgrid(x, y)
R2 = X**2 + Y**2

# 金星環境での炉内温度分布モデル (中心部が1180K, 周辺が1130K)
T_venus_3d = 1130 + 50 * np.exp(-R2 / 50)
delta_3d = 0 # 空間分布を見るため材料ムラは一旦0固定

T, delta = T_venus_3d, delta_3d
P_venus_3d = eval(expr_py)

# --- 描画 ---
fig = plt.figure(figsize=(15, 6))

# 左：ヒストグラム対比
ax1 = fig.add_subplot(121)
ax1.hist(P_earth, bins=50, alpha=0.6, label='Earth: Air Cooling (Low P)', color='blue')
ax1.hist(P_venus, bins=50, alpha=0.6, label='Venus: sCO2 Cooling (High P)', color='red')
ax1.set_title("Planetary Comparison (Robustness)")
ax1.set_xlabel("Reaction Probability (P)")
ax1.legend()

# 右：金星炉の3次元空間再現性分布
ax2 = fig.add_subplot(122, projection='3d')
surf = ax2.plot_surface(X, Y, P_venus_3d, cmap=cm.magma, edgecolor='none', alpha=0.9)
ax2.set_title("Venus Reactor: Spatial Reproducibility")
ax2.set_xlabel("X [mm]")
ax2.set_ylabel("Y [mm]")
ax2.set_zlabel("P")
fig.colorbar(surf, ax=ax2, shrink=0.5, aspect=10)

plt.tight_layout()
plt.show()

print(f"解析式: {expr_py}")
print(f"金星炉の空間平均再現性: {np.mean(P_venus_3d):.4f}")