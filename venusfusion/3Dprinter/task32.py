#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 12:14:13 2026

@author: iwamura
"""

# Python Code: 修正された params.py を読み込む
import numpy as np
import matplotlib.pyplot as plt
import os

# params.py が存在し、中身が正しいかチェック
try:
    import params
    # 読み込んだ値を確認
    print(f"Imported Parameters: ALPHA={params.ALPHA}, N0={params.N0}")
except SyntaxError as e:
    print(f"SyntaxError発生！ファイルの中身が壊れています: {e}")
except ImportError:
    print("params.py が見つかりません。")

# --- 以降、シミュレーション処理 ---
t = np.linspace(0, 100, 1000)
N = np.zeros_like(t)
N[0] = params.N0
dt = t[1] - t[0]

# 40日目で補給停止（アルファが負に転じる）
for i in range(1, len(t)):
    current_alpha = params.ALPHA if t[i] < 40 else -0.1
    N[i] = N[i-1] + (current_alpha * N[i-1]) * dt

plt.figure(figsize=(10, 6))
plt.plot(t, N, label="Colony Population (Self-Replication)")
plt.axvline(x=40, color='red', linestyle='--', label="Supply Cut-off")
plt.xlabel("Time (Days)")
plt.ylabel("Units")
plt.title("Venus 3D Printer Colony Resilience")
plt.legend()
plt.grid(True)
plt.show()