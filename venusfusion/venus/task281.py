#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 18:12:33 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# 自身のスクリプトがあるディレクトリに強制移動
base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)

target = "equilibrium_data.txt"

# ファイル存在確認
if not os.path.exists(target):
    print(f"【エラー】ファイルが {base_path} に見当たりません。")
    sys.exit(1)

# データの読み込み
data = np.loadtxt(target, delimiter=',')
t_theory, k_theory = data[:, 0], data[:, 1]

# 金星大気連成計算 (高度 0-60km)
alt = np.linspace(0, 60, 200)
T_v = 735 - 8.5 * alt
P_v = 92 * np.exp(-alt / 15.9)

# 理論解のマッピング
K_v = np.interp(T_v, t_theory, k_theory)
# 抽出スループット算出
S = (K_v * P_v) / (1 + K_v)

# 結果のプロット
plt.figure(figsize=(8, 5))
plt.plot(alt, S, lw=2)
plt.xlabel('Altitude (km)')
plt.ylabel('Extraction Throughput')
plt.title('Task 28: Venus Carbon Recovery (Path Sync Success)')
plt.grid(True)
plt.show()