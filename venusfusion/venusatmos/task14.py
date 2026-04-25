#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 12:07:48 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Maximaから理論式をインポート
with open("formula_14.txt", "r") as f:
    raw_formula = f.read().strip()
    # Maximaの %e^ を Pythonの 1 * np.exp() 的な構造に解釈させるため置換
    # %e -> (np.exp(1)) または単純に関数として扱うための前処理
    formula_py = raw_formula.replace("%e^", "np.exp").replace("^", "**")

# 2. 力仕事：24時間の霧の濃度ゆらぎを生成
t = np.linspace(0, 24, 1440)
kappa_env = 0.0001 * (1 + np.sin(2 * np.pi * t / 24)) + np.random.normal(0, 0.00002, 1440)
kappa_env = np.maximum(kappa_env, 0)

# 3. 計算実行
# 式が np.exp(-(10000*kappa)) の形になるよう eval を実行
# ※ Maxima出力が %e^-(...) なら、置換後は np.exp(-(10000*kappa)) となる
try:
    efficiency = eval(formula_py, {"np": np, "kappa": kappa_env})
except Exception as e:
    # 万が一のパースエラー対策：直接定義にフォールバック
    print(f"Eval Error: {e}. Switching to direct calculation.")
    efficiency = np.exp(-(10000 * kappa_env))

# 4. 可視化
plt.plot(t, efficiency * 100)
plt.title("24-Hour Transmission Efficiency Simulation")
plt.xlabel("Time (hours)")
plt.ylabel("Efficiency (%)")
plt.grid(True)
plt.show()

print(f"Daily Average Efficiency: {np.mean(efficiency)*100:.2f}%")