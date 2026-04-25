#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 19:28:04 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy
from sympy import symbols, exp, latex
from IPython.display import display, Math

# --- 1. SymPyによる数式定義 (解析解) ---
T = symbols('T')
delta_H = -178000  # J/mol
delta_S = -160     # J/mol*K
R = 8.314          # J/mol*K

# ギブス自由エネルギー G(T) と 平衡定数 K(T)
G_expr = delta_H - T * delta_S
K_expr = exp(-G_expr / (R * T))

# --- 2. LaTeX形式の数式出力 ---
print("--- SymPyによる解析解の生成 ---")
# LaTeX文字列を生成して表示
display(Math(f"G(T) = {latex(G_expr)} \\quad [J/mol]"))
display(Math(f"K(T) = {latex(K_expr)}"))

# --- 3. 数式を数値計算用に関数化 (Lambdify) ---
# これにより、Maximaの外部ファイルを経由せずに直接NumPy配列を処理できます
K_func = sympy.lambdify(T, K_expr, 'numpy')

# --- 4. 金星大気プロファイルとの連成 ---
alt = np.linspace(0, 60, 200)   # 高度 0 to 60 km
T_v = 735 - 8.5 * alt           # 温度勾配 (K)
P_v = 92 * np.exp(-alt / 15.9)  # 圧力勾配 (atm)

# 平衡定数を高度ごとに算出
K_v = K_func(T_v)

# 抽出ポテンシャル S(h) = (K * P) / (1 + K)
# 単位: atm相当 (抽出に寄与する有効圧)
throughput = (K_v * P_v) / (1 + K_v)

# --- 5. 可視化 (連成グラフ) ---
fig, ax1 = plt.subplots(figsize=(10, 6))

# 抽出ポテンシャルのプロット
ax1.set_xlabel('Altitude (km)')
ax1.set_ylabel('Extraction Potential (atm)', color='blue')
ax1.plot(alt, throughput, color='blue', lw=3, label='Extraction Potential')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, linestyle='--', alpha=0.7)

# 温度プロファイルを重ねる
ax2 = ax1.twinx()
ax2.set_ylabel('Temperature (K)', color='red')
ax2.plot(alt, T_v, color='red', linestyle=':', alpha=0.6, label='Temperature')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Task 28: Venus Carbon Recovery Analysis (SymPy Integrated)')
fig.tight_layout()
plt.show()

# レポート用のLaTeXコードを表示
print("\n--- レポート用LaTeXソース ---")
print(f"K(T) = {latex(K_expr)}")