#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 18:00:38 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# 作業ディレクトリを固定
os.chdir("/home/iwamura/ドキュメント/coupling/venusfusion")
target = "equilibrium_data.txt"

if not os.path.exists(target):
    print(f"【エラー】やはりファイルが見当たりません: {os.getcwd()}")
    sys.exit(1)

# タグが混じっても「数値とカンマ」以外を無視して読み込む
try:
    # comments='<' とすることで XMLタグの開始行をスキップし、
    # 壊れた行を ignore して読み込みます
    data = np.genfromtxt(target, delimiter=',', invalid_raise=False, comments='<')
    
    # 読み込んだデータが空でないか確認
    if data.size == 0:
        raise ValueError("ファイルはありますが、中身が空か読み取れる数値がありません。")
        
    t_theory = data[:, 0]
    k_theory = data[:, 1]
    print(f"成功: {len(data)}件のデータを読み込みました。")
except Exception as e:
    print(f"読み込みエラー: {e}")
    sys.exit(1)

# 金星大気連成（高度 0-60km）
alt = np.linspace(0, 60, 200)
T_v = 735 - 8.5 * alt
P_v = 92 * np.exp(-alt / 15.9)

# 理論解のマッピング
K_v = np.interp(T_v, t_theory, k_theory)
S = (K_v * P_v) / (1 + K_v)

plt.plot(alt, S)
plt.title("Task 28: Venus Carbon Recovery Profile (Strict)")
plt.xlabel("Altitude (km)")
plt.ylabel("Extraction Throughput")
plt.grid(True)
plt.show()