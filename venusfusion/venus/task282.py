#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 18:28:26 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# 自身の場所を作業ディレクトリに
os.chdir(os.path.dirname(os.path.abspath(__file__)))

target = "equilibrium_data.txt"

if not os.path.exists(target):
    print(f"【エラー】バッチ実行でファイルが生成されませんでした。")
    sys.exit(1)

# クリーンな数値データをロード
data = np.loadtxt(target, delimiter=',')
t_theory, k_theory = data[:, 0], data[:, 1]

# 金星大気プロファイル (0-60km)
alt = np.linspace(0, 60, 200)
T_v = 735 - 8.5 * alt
P_v = 92 * np.exp(-alt / 15.9)

# 理論解を補間
K_v = np.interp(T_v, t_theory, k_theory)
# スループット算出
S = (K_v * P_v) / (1 + K_v)

# 結果のプロット
plt.figure(figsize=(8, 5))
plt.plot(alt, S, lw=2, color='darkorange')
plt.xlabel('Altitude (km)')
plt.ylabel('Extraction Potential')
plt.title('Task 28: Venus Carbon Recovery (Batch Linked)')
plt.grid(True)
plt.show()