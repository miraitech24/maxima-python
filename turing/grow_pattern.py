#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 13:14:30 2025

@author: iwamura
"""

import sys, json, numpy as np
import matplotlib.pyplot as plt

# 1. 設計図の読み込み
with open('params.json', 'r') as f:
    data = json.load(f)
a, b = data['a'], data['b']
u_star = eval(data['u_star'].replace('^', '**'))
v_star = eval(data['v_star'].replace('^', '**'))

# 2. 初期設定
N, dt = 100, 0.1
Du, Dv = 0.2, 1.0
U = u_star + np.random.randn(N, N) * 0.05
V = v_star + np.random.randn(N, N) * 0.05

def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)

# スナップショットを格納するリスト
history = []
labels = ["Phase 1: Chaos", "Phase 2: Budding", "Phase 3: Mature", "Phase 4: Final"]
checkpoints = [0, 500, 2000, 10000] # 各フェーズの計算ステップ数

# 3. 計算実行と記録
print("Calculating growth stages...")
for step in range(10001):
    lu, lv = laplacian(U), laplacian(V)
    U += (a - U + U**2 * V + Du * lu) * dt
    V += (b - U**2 * V + Dv * lv) * dt
    
    if step in checkpoints:
        history.append(U.copy())

# 4. 一覧表示（これが「成長の履歴表」になります）
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, ax in enumerate(axes):
    ax.imshow(history[i], cmap='magma')
    ax.set_title(labels[i])
    ax.axis('off')

plt.tight_layout()
plt.show()