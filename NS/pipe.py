#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 15:02:12 2025

@author: iwamura
"""

import matplotlib.pyplot as plt
import numpy as np
# %run flow_equations.py  # Maximaから出力された式を読み込む

# グリッド作成
x, y = np.meshgrid(np.linspace(0, 2, 20), np.linspace(0, 1, 10))
u = np.ones_like(x) # 収束計算後の値が入る
v = np.zeros_like(y)

plt.figure(figsize=(10, 5))
plt.quiver(x, y, u, v) # ベクトル図
plt.title("Pipe Flow Velocity Vector")
plt.xlabel("x (Pipe Length)")
plt.ylabel("y (Radius/Width)")
plt.show()