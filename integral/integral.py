#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 11:05:43 2025

@author: iwamura
"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import importlib

# 1. Maximaが出力したファイルをインポート（修正ポイント）
try:
    import data_bridge
    importlib.reload(data_bridge) # ファイル更新を反映
    formula_str = data_bridge.maxima_expr
    print(f"Maximaから受け取った数式: {formula_str}")
except ImportError:
    print("エラー: data_bridge.py が見つかりません。先にMaximaを実行してください。")

# 2. 文字列としての数式を数値計算用に変換 (不足分の補完)
# Maximaのべき乗 '^' を Pythonの '**' に変換してパース
x_sym = sp.symbols('x')
clean_formula = formula_str.replace('^', '**')
func_np = sp.lambdify(x_sym, sp.sympify(clean_formula), 'numpy')

# 3. グラフ描画
x_vals = np.linspace(-10, 10, 400)
y_vals = func_np(x_vals)

plt.figure(figsize=(8, 4))
plt.plot(x_vals, y_vals, label=f"Integral: ${formula_str}$")
plt.title("Coupling Result: Maxima Expression in Python Plot")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()