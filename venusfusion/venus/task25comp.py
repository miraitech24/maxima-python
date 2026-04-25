#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 13:21:25 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. 解析解のインポート（以前のクレンジング処理を継続）
with open("solution_p.txt", "r") as f:
    expr_raw = f.read().split(":")[-1].replace(";", "").strip()
    expr_py = expr_raw.replace("%e**", "np.exp").replace("^", "**").replace("%e", "np.e")

# 2. 惑星別の環境分布（10,000サイトのサンプリング）
# 地球：抜熱が安定しており、温度ムラが少ない（標準偏差15K）
T_earth = np.random.normal(1100, 15, 10000) 
# 金星：外気温が高く冷却が不安定。温度ムラが大きい（標準偏差60K）
T_venus = np.random.normal(1100, 60, 10000) 

# 3. 反応確率の計算
T = T_earth
P_earth = eval(expr_py)
T = T_venus
P_venus = eval(expr_py)

# 4. ヒストグラム対比プロット
plt.figure(figsize=(10, 6))
plt.hist(P_earth, bins=50, alpha=0.6, label='Earth (Stable/Robust)', color='blue', edgecolor='darkblue')
plt.hist(P_venus, bins=50, alpha=0.6, label='Venus (Unstable/Fragile)', color='red', edgecolor='darkred')

plt.title("Comparison of Reactor Robustness: Earth vs Venus")
plt.xlabel("Reaction Probability (P)")
plt.ylabel("Site Count (Frequency)")
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()

print(f"地球の再現性期待値: {np.mean(P_earth):.4f}")
print(f"金星の再現性期待値: {np.mean(P_venus):.4f}")