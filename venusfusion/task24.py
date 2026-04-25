#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 11:37:48 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. プレーンテキストの数式をインポート
with open("solution.txt", "r") as f:
    # べき乗(^)をPythonの(**)へ変換し、numpyを紐付け
    expr = f.read().strip().replace("^", "**").replace("cos", "np.cos")

# 2. 配列処理 (緯度ごとの繰り返し計算をベクトル演算で代行)
phi = np.linspace(-np.pi/2, np.pi/2, 181) # 1度刻みのラジアン配列
A, u_max, C = 1.0, 10.0, 1.5              # 物理定数

# 解析解を配列に適用
Q_array = eval(expr)

# 3. 数値プロット (単位: deg, W/m^2)
plt.figure(figsize=(8, 4))
plt.plot(np.degrees(phi), Q_array, label="Calculated Transport")
plt.title("Atmospheric Heat Transport Distribution")
plt.xlabel("Latitude (degrees)")
plt.ylabel("Heat Transport Q [W/m^2]")
plt.grid(True)
plt.show()